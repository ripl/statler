import argparse
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
from pathlib import Path
from textwrap import dedent
from typing import List

import cv2
import matplotlib.pyplot as plt
from moviepy.editor import ImageSequenceClip
from PIL import Image

from cap.helpers import call_api, rootdir
from cap.helpers.prompt import cleanup_preprompt, load_prompts
from cap.helpers import logger

from typing import Union

DEFAULT_MODEL_NAME = 'gpt-3.5-turbo-instruct'
prompts = load_prompts(rootdir / 'experiments' / 'prompts')


def normalize(text):
    """replace double quoted string to single quoted string"""
    return re.sub(r'"([^"]*)"', r"'\1'", text)


def compare(gen_code: str, gold_code: str, ignore: List = []):
    """Compare two pieces of code, ignoring certain lines that start with a string specified by `ignore`."""
    gen_lines = []
    for line in gen_code.split('\n'):
        line = normalize(line.strip())
        if not any([line.startswith(ig) for ig in ignore]) and len(line) > 0:
            gen_lines.append(line)

    gold_lines = []
    for line in gold_code.split('\n'):
        line = normalize(line.strip())
        if not any([line.startswith(ig) for ig in ignore]) and len(line) > 0:
            gold_lines.append(line)

    return_str = 'gen line vs. gold line\n'
    exist_not_equal = False
    for i, (gen_line, gold_line) in enumerate(zip(gen_lines, gold_lines)):
        if gen_line == gold_line:
            return_str += '{} == {}\n'.format(gen_line, gold_line)
        elif gen_line != gold_line:
            return_str += '{} != {} <---- not equal!!\n'.format(gen_line, gold_line)
            exist_not_equal = True

    if len(gen_lines) != len(gold_lines):
        exist_not_equal = True

    if not exist_not_equal:
        return 'All Equal!'
    return return_str


class AbstractAgent:
    def __init__(self, task_description, model_name, prompt_dir) -> None:
        self.model_name = model_name
        self.task_description = task_description
        self.separator = '==='
        self.first_time = True

        self._trajectory = []

    def reset(self, state):
        raise NotImplementedError()

    def step(self, user_query, report_usage=False, gold_code=None):
        raise NotImplementedError()

    def update_wm(self, user_query):
        self.update(user_query, verbose=True)

    def save_history(self, fname, code_ignore_list=[]):
        """Save the history to a file."""

        out = '========= step 0 =========\n'
        if 'prev_state' in self._trajectory[0]:
            out += self._trajectory[0]['prev_state']
        for i, step in enumerate(self._trajectory):
            out += f'\n========= step {i + 1} =========\n'
            out += '\n'.join((
                f"# query: {step['query']}",
                f"```generated:\n{step['code']}\n```",
                f"```gold:\n{step['gold_code']}\n```",
            ))
            if 'next_state' in step:
                out += '\n' + step['next_state']

        logger.info(f'Writing the history to {fname}')
        with open(fname, 'w') as f:
            f.write(out)

        # Compare generated vs gold code
        failure_steps = []
        code = '========= step 0 =========\n'
        for i, step in enumerate(self._trajectory):
            compared_result_str = compare(step['code'], step['gold_code'], ignore=code_ignore_list)
            if compared_result_str == 'All Equal!':
                continue

            # If not "All Equal", add the step to failure_steps
            failure_steps.append(step)

            code += f'========= step {i + 1} =========\n'
            code += '\n'.join((
                f">> generated\n{step['code']}",
                "---------",
                f">> gold\n{step['gold_code']}",
                "---------",
                # f">> diff\n{compared_result_str}",
            )) + '\n'
        fpath = Path(fname)
        code_fname = str(fpath.parent / fpath.stem) + '-code' + fpath.suffix
        logger.info(f'Writing the code history to {code_fname}')
        with open(code_fname, 'w') as f:
            f.write(code)


class BaselineAgent(AbstractAgent):
    def __init__(self, task_description, prompt_dir, model_name: str = DEFAULT_MODEL_NAME, keep_history: bool = True) -> None:
        super().__init__(task_description, model_name, prompt_dir)
        self.task_description = task_description.format(list_of_functions='`put_first_on_second` and `say`')

        if prompt_dir != '.':
            self.prompt_name = '.'.join((prompt_dir, 'cap_baseline'))
        else:
            self.prompt_name = 'cap_baseline'

        self._keep_history = keep_history

    def reset(self, simple_state):
        self.first_time = True
        self.simple_state = simple_state
        logger.info('====== BaselineAgent -- Initial simple state ======')
        logger.info(self.simple_state)
        logger.info('===========================')
        self._trajectory = []

    def step(self, user_query, report_usage=False, verbose=False, gold_code=None):
        assert self.simple_state is not None
        if verbose:
            logger.info('========= current simple state =========')
            logger.info(self.simple_state)
            logger.info('===========================')
        # logger.info('Type your command starting with `read: <your-query>` or `update: <your-query>`\n> ', end='')

        preprompt = prompts[self.prompt_name]

        query_str = f'# query: {user_query}'
        prompt = '\n'.join((preprompt, self.task_description, self.separator, self.simple_state, query_str + '\n'))

        generated = call_api(
            self.model_name,
            prompt,
            report_usage=report_usage and self.first_time,
        )

        if verbose:
            logger.info('This is the prompt fed into the baseline model')
            logger.info('*********************************')
            logger.info(prompt)
            logger.info('*********************************')
            logger.info('========= BaselineAgent =========')
            logger.info('user query:', user_query)
            logger.info(f'generated:\n{generated}')
            logger.info('==================')

        # Simply concat histories
        if self._keep_history:
            self.simple_state = '\n'.join((self.simple_state, query_str, generated))

        self.first_time = False

        self._trajectory.append(
            {'query': user_query,
             'code': generated,
             'gold_code': gold_code}
        )
        return generated


class UnifiedStateAugAgent(AbstractAgent):
    """A variant of StateAugAgent that has a unified model for code generation and next state generation.

    Naturally, we don't have `update` method anymore.
    """

    def __init__(self, task_description, model_name, prompt_dir):
        super().__init__(task_description, model_name, prompt_dir)
        self.task_description = task_description.format(list_of_functions='`put_first_on_second`, `say` and `update_wm`')
        self.prompt_name = 'cap_wm_reader'
        if prompt_dir != '.':
            self.prompt_name = '.'.join((prompt_dir, self.prompt_name))

    def reset(self, world_state):
        self.first_time = True
        self.world_state = world_state
        logger.info('====== UnifiedStateAugAgent -- initial world state ======')
        logger.info(self.world_state)
        logger.info('==================================================')
        self._trajectory = []

    def step(self, user_query, report_usage=False, verbose=False, gold_code=None):
        assert self.world_state is not None
        if verbose:
            logger.info('====== UnifiedStateAugAgent -- current world state ======')
            logger.info(self.world_state)
            logger.info('==================================================')

        prev_state = deepcopy(self.world_state)

        # Construct a prompt
        preprompt = prompts[self.prompt_name]
        query_str = f'# query: {user_query}'

        prompt = '\n'.join((preprompt, self.task_description, self.separator,
                            self.world_state + '\n', query_str + '\n'))

        # Call the api
        generated = call_api(
            self.model_name,
            prompt,
            stop=['# query: '],  # Generate until the next query is about to be generated!
            report_usage=report_usage and self.first_time,
        )

        # Extract and update the self.world_state
        state_prefix = '\n# state = {'
        if state_prefix not in generated:
            self.world_state = state_prefix + '}'
        else:
            self.world_state = state_prefix + generated.split(state_prefix)[-1]

        logger.info('====== UnifiedStateAugAgent ======')
        logger.info('user query:', user_query)
        logger.info(f'generated:\n{generated}')
        logger.info('===========================')
        self.first_time = False

        self._trajectory.append(
            {'prev_state': prev_state,
             'query': user_query,
             'code': generated.split(state_prefix)[0],
             'next_state': deepcopy(self.world_state),
             'gold_code': gold_code}
        )
        return generated

    @staticmethod
    def _extract_string(line):
        """Extract a string from a line like 'update_wm("foo bar")'"""
        match = re.search(r'\(([\'|"])(.*)\1\)', line)
        if match:
            return match[2]


class CoTAugAgent(AbstractAgent):
    """
    CoT Augmented Agent
    """

    def __init__(self, task_description, model_name, prompt_dir):
        super().__init__(task_description, model_name, prompt_dir)
        self.task_description = task_description.format(list_of_functions='`put_first_on_second`, `say` and `update_wm`')
        self.prompt_name = 'cap_wm_reader'
        if prompt_dir != '.':
            self.prompt_name = '.'.join((prompt_dir, self.prompt_name))

    def reset(self, world_state):
        self.first_time = True
        self.world_state = world_state
        logger.info('====== CoTAugAgent -- initial world state ======')
        logger.info(self.world_state)
        logger.info('==================================================')
        self._trajectory = []
        self.history_str = self.world_state

    def step(self, user_query, report_usage=False, verbose=False, gold_code=None):
        assert self.world_state is not None
        if verbose:
            logger.info('====== CoTAugAgent -- current world state ======')
            logger.info(self.world_state)
            logger.info('==================================================')

        prev_state = deepcopy(self.world_state)

        # Construct a prompt
        preprompt = prompts[self.prompt_name]
        query_str = f'# query: {user_query}'

        prompt = '\n'.join((preprompt, self.task_description,
                            self.separator, self.history_str + '\n', query_str + '\n'))

        # Call the api
        try:
            generated = call_api(
                self.model_name,
                prompt,
                stop=['# query: '],  # Generate until the next query is about to be generated!
                report_usage=report_usage and self.first_time,
            )
        except BaseException:
            generated = 'extend context window.'

        # Extract and update the self.world_state
        state_prefix = '\n# state = {'
        if state_prefix not in generated:
            self.world_state = state_prefix + '}'
        else:
            self.world_state = state_prefix + generated.split(state_prefix)[-1]

        # Simply concat histories
        self.history_str = '\n'.join((self.history_str + '\n', query_str, generated))

        logger.info('====== CoTStateAugAgent ======')
        logger.info('user query:', user_query)
        logger.info(f'generated:\n{generated}')
        logger.info('===========================')
        self.first_time = False

        self._trajectory.append(
            {'prev_state': prev_state,
             'query': user_query,
             'code': generated.split(state_prefix)[0],
             'next_state': deepcopy(self.world_state),
             'gold_code': gold_code}
        )
        return generated

    @staticmethod
    def _extract_string(line):
        """Extract a string from a line like 'update_wm("foo bar")'"""
        match = re.search(r'\(([\'|"])(.*)\1\)', line)
        if match:
            return match[2]


class StateAugAgent(AbstractAgent):
    def __init__(self, task_description, prompt_dir='disinfection', model_name: str = DEFAULT_MODEL_NAME):
        super().__init__(task_description, model_name, prompt_dir)
        self.task_description = task_description.format(list_of_functions='`put_first_on_second`, `say` and `update_wm`')
        self.world_state = None
        self.prompt_name_reader = 'cap_wm_reader'
        self.prompt_name_updater = 'cap_wm_updater'
        if prompt_dir != '.':
            self.prompt_name_reader = '.'.join((prompt_dir, self.prompt_name_reader))
        if prompt_dir != '.':
            self.prompt_name_updater = '.'.join((prompt_dir, self.prompt_name_updater))

    def reset(self, world_state):
        self.first_time = True
        self.world_state = world_state
        logger.info('====== StateAugAgent -- initial world state ======')
        logger.info(self.world_state)
        logger.info('==================================================')
        self._trajectory = []

    def step(self, user_query, report_usage=False, verbose=False, gold_code=None):
        assert self.world_state is not None
        if verbose:
            logger.info('====== StateAugAgent -- current world state ======')
            logger.info(self.world_state)
            logger.info('==================================================')

        prev_state = deepcopy(self.world_state)

        # Construct a prompt
        preprompt = prompts[self.prompt_name_reader]
        query_str = f'# query: {user_query}'

        prompt = '\n'.join((preprompt, self.task_description, self.separator, self.world_state, query_str + '\n'))

        if verbose:
            logger.info('This is the prompt fed into the StateAug model')
            logger.info('*********************************')
            logger.info(prompt)
            logger.info('*********************************')
        # Call the api
        generated = call_api(
            self.model_name,
            prompt,
            stop=['# state = {'],
            report_usage=report_usage and self.first_time,
        )

        # If `update_wm(query)` is in the generated text, then call self.update(query)
        for line in generated.split('\n'):
            if line.startswith('update_wm('):
                query = self._extract_string(line)
                logger.info('🆕 updating the state with generated query:', query)
                self.update(query, verbose=verbose)

        logger.info('====== StateAugAgent ======')
        logger.info('user query:', user_query)
        logger.info(f'generated:\n{generated}')
        logger.info('===========================')
        self.first_time = False

        self._trajectory.append(
            {'prev_state': prev_state,
             'query': user_query,
             'code': generated,
             'next_state': deepcopy(self.world_state),
             'gold_code': gold_code}
        )
        return generated

    @staticmethod
    def _extract_string(line):
        """Extract a string from a line like 'update_wm("foo bar")'"""
        match = re.search(r'\(([\'|"])(.*)\1\)', line)
        if match:
            return match[2]

    def update(self, update_query, report_usage=False, verbose=False):
        preprompt = prompts[self.prompt_name_updater]
        state_prefix = '\n# state = {\n#     '

        query_str = f'# query: {update_query}'
        prompt = '\n'.join((preprompt, self.task_description, self.separator, self.world_state, query_str + state_prefix))
        generated = call_api(
            self.model_name,
            prompt,
            stop=['# query: '],
            report_usage=report_usage,
        )

        # Update the state
        self.world_state = state_prefix + generated

        if verbose:
            logger.info('====== StateAugAgent -- current world state ======')
            logger.info(self.world_state)
            logger.info('==================================================')


class AutoStateAugAgent(AbstractAgent):
    def __init__(self, task_description, prompt_dir, model_name: str = DEFAULT_MODEL_NAME):
        super().__init__(task_description, model_name, prompt_dir)
        self.task_description = task_description.format(list_of_functions='`put_first_on_second`, `say` and `update_wm`')
        self.world_state = None
        self.prompt_name_reader = 'cap_auto_wm_reader'
        self.prompt_name_updater = 'cap_auto_wm_updater'
        if prompt_dir != '.':
            self.prompt_name_reader = '.'.join((prompt_dir, self.prompt_name_reader))
        if prompt_dir != '.':
            self.prompt_name_updater = '.'.join((prompt_dir, self.prompt_name_updater))

    def reset(self, world_state):
        self.first_time = True
        self.world_state = world_state
        logger.info('====== AutoStateAugAgent -- initial world state ======')
        logger.info(self.world_state)
        logger.info('==================================================')
        self._trajectory = []

    def step(self, user_query, report_usage=False, verbose=False, gold_code=None):
        assert self.world_state is not None
        if verbose:
            logger.info('====== AutoStateAugAgent -- current world state ======')
            logger.info(self.world_state)
            logger.info('==================================================')

        prev_state = deepcopy(self.world_state)

        # Construct a prompt
        preprompt = prompts[self.prompt_name_reader]
        query_str = f'# query: {user_query}'

        prompt = '\n'.join((preprompt, self.world_state, query_str + '\n'))

        # Call the api
        generated = call_api(
            self.model_name,
            prompt,
            stop=['# query: '],
            report_usage=report_usage and self.first_time,
        )

        # If `update_wm(query)` is in the generated text, then call self.update(query)
        for line in generated.split('\n'):
            if line.startswith('update_wm('):
                query = self._extract_string(line)
                logger.info('🆕 updating the state with generated query:', query)
                self.update(query, verbose=verbose)

        if verbose:
            logger.info('====== AutoStateAugAgent ======')
            logger.info('user query:', user_query)
            logger.info(f'generated:\n{generated}')
            logger.info('===========================')

        self.first_time = False

        self._trajectory.append(
            {'prev_state': prev_state,
             'query': user_query,
             'code': generated,
             'next_state': deepcopy(self.world_state),
             'gold_code': gold_code}
        )
        return generated

    @staticmethod
    def _extract_string(line):
        """Extract a string from a line like 'update_wm("foo bar")'"""
        match = re.search(r'\(([\'|"])(.*)\1\)', line)
        if match:
            return match[2]

    def update(self, update_query, report_usage=False, verbose=False):
        preprompt = prompts[self.prompt_name_updater]
        state_prefix = '\n# state = {\n#     '

        query_str = f'# query: {update_query}'
        prompt = '\n'.join((preprompt, self.world_state, query_str + state_prefix))
        generated = call_api(
            self.model_name,
            prompt,
            stop=['# query: '],
            report_usage=report_usage,
        )

        # Update the state
        self.world_state = state_prefix + generated

        if verbose:
            logger.info('====== AutoStateAugAgent -- current world state ======')
            logger.info(self.world_state)
            logger.info('==================================================')


def run_episode(task_name, ep_idx, episode, make_auto_state_aug_agent,
                make_state_aug_agent, make_cot_agent,
                make_unified_state_aug_agent,
                make_baseline_agent,
                agents,
                results_dir: Union[str, Path] = 'results'):
    # Fetch and cleanup evaluation data
    init_state = cleanup_preprompt(episode['init_state'])
    init_simple_state = cleanup_preprompt(episode['init_simple_state'])
    auto_init_state = """
# state = {}
""".format(init_state.strip().lstrip('# state = '))

    episode = episode['episode']

    baseline_agent = make_baseline_agent()
    unified_state_aug_agent = make_unified_state_aug_agent()
    cot_aug_agent = make_cot_agent()
    state_aug_agent = make_state_aug_agent()
    auto_state_aug_agent = make_auto_state_aug_agent()

    # Reset the agents with initial states
    auto_state_aug_agent.reset(auto_init_state)
    state_aug_agent.reset(init_state)
    cot_aug_agent.reset(init_state)
    unified_state_aug_agent.reset(init_state)
    baseline_agent.reset(init_simple_state)

    generated_ep = []
    for step in episode:
        # Feed the user query to each agent
        user_query = cleanup_preprompt(step['user_query'])
        gold_code = cleanup_preprompt(step['gold_code'])
        # gold_next_state = cleanup_preprompt(step['gold_next_state'])
        if agents == 'all':
            generated = {
                'auto': auto_state_aug_agent.step(user_query, gold_code=gold_code),
                'state_aug': state_aug_agent.step(user_query, gold_code=gold_code),
                'unified_state_aug': unified_state_aug_agent.step(user_query, gold_code=gold_code),
                'cot': cot_aug_agent.step(user_query, gold_code=gold_code),
                'baseline': baseline_agent.step(user_query, gold_code=gold_code),
            }
        elif agents == 'baseline':
            generated = {'baseline': baseline_agent.step(user_query, gold_code=gold_code)}
        elif agents == 'unified_state_aug':
            generated = {'unified_state_aug': unified_state_aug_agent.step(user_query, gold_code=gold_code)}
        elif agents == 'cot':
            generated = {'cot': cot_aug_agent.step(user_query, gold_code=gold_code)}
        elif agents == 'state_aug':
            generated = {'state_aug': state_aug_agent.step(user_query, gold_code=gold_code)}
        elif agents == 'auto':
            generated = {'auto': auto_state_aug_agent.step(user_query, gold_code=gold_code)}
        generated_ep.append(generated)

    # Save the generated_eps
    results_dir = Path(results_dir) / task_name
    results_dir.mkdir(parents=True, exist_ok=True)
    if agents == 'all':
        baseline_agent.save_history(results_dir / f'baseline-episode{ep_idx:02d}.txt', code_ignore_list=['# ', 'update_wm', 'noop'])
        unified_state_aug_agent.save_history(results_dir / f'unified-state-aug-episode{ep_idx:02d}.txt', code_ignore_list=['# ', 'update_wm', 'noop'])
        cot_aug_agent.save_history(results_dir / f'cot-aug-episode{ep_idx:02d}.txt', code_ignore_list=['# ', 'update_wm', 'noop'])
        state_aug_agent.save_history(results_dir / f'state-aug-episode{ep_idx:02d}.txt', code_ignore_list=['# ', 'update_wm', 'noop'])
        auto_state_aug_agent.save_history(results_dir / f'auto-state-aug-episode{ep_idx:02d}.txt', code_ignore_list=['# ', 'update_wm', 'noop', '  ', 'if', 'def', 'while', 'say'])
    elif agents == 'baseline':
        baseline_agent.save_history(results_dir / f'baseline-episode{ep_idx:02d}.txt', code_ignore_list=['# ', 'update_wm', 'noop', 'say'])
    elif agents == 'unified_state_aug':
        unified_state_aug_agent.save_history(results_dir / f'unified-state-aug-episode{ep_idx:02d}.txt', code_ignore_list=['# ', 'update_wm', 'noop'])
    elif agents == 'cot':
        cot_aug_agent.save_history(results_dir / f'cot-aug-episode{ep_idx:02d}.txt', code_ignore_list=['# ', 'update_wm', 'noop'])
    elif agents == 'state_aug':
        state_aug_agent.save_history(results_dir / f'state-aug-episode{ep_idx:02d}.txt', code_ignore_list=['# ', 'update_wm', 'noop', 'say'])
    elif agents == 'auto':
        auto_state_aug_agent.save_history(results_dir / f'auto-state-aug-episode{ep_idx:02d}.txt', code_ignore_list=['# ', 'update_wm', 'noop', '  ', 'if', 'def', 'while', 'say'])
    return generated_ep


def run_episode_with_simulation(task_name, ep_idx, episode, make_state_aug_agent, make_baseline_agent, use_aug_agent: bool = False):

    # dependencies for the simulator
    from cap.world_model import setup_LMP

    # Fetch and cleanup evaluation data
    init_state = cleanup_preprompt(episode['init_state'])
    init_simple_state = cleanup_preprompt(episode['init_simple_state'])

    env = Env(
        render=False,
        high_res=False,
        high_frame_rate=False,
        use_mdetr=False,
    )

    # convert the init_simple_state to a list of objects
    object_list = init_simple_state
    object_list = object_list.strip().replace('# ', '').replace('objects = ', '').rstrip(',')
    object_list = json.loads(object_list)
    env.reset(object_list)

    # domain specific setup
    if task_name == 'disinfection' and 'dirty_object_list' in episode.keys():
        env.dirty_object_list = episode['dirty_object_list']
        env.update_dirty()
    elif task_name == 'weight' and 'obj_name_to_weight' in episode.keys():
        env.obj_name_to_weight = episode['obj_name_to_weight']
        env.update_weight_circles()

    lmp_tabletop_ui, lmp_wm = setup_LMP(env, init_state)

    baseline_agent = make_baseline_agent()
    state_aug_agent = make_state_aug_agent()

    # Reset the agents with initial states
    state_aug_agent.reset(init_state)
    baseline_agent.reset(init_simple_state)

    results_dir = Path('figures') / task_name
    results_dir.mkdir(parents=True, exist_ok=True)

    generated_ep = []
    for t in range(len(episode['episode'])):
        # Feed the user query to each agent
        user_query = cleanup_preprompt(episode['episode'][t]['user_query'])
        gold_code = cleanup_preprompt(episode['episode'][t]['gold_code'])
        # gold_next_state = cleanup_preprompt(step['gold_next_state'])
        generated = {
            'state_aug': state_aug_agent.step(user_query, gold_code=gold_code),
            'baseline': baseline_agent.step(user_query, gold_code=gold_code),
        }
        generated_ep.append(generated)

        user_query = cleanup_preprompt(user_query)
        lmp_tabletop_ui.execute_code_string(user_query, generated['state_aug'] if use_aug_agent else generated['baseline'])

        # Save the image
        demo_img = cv2.cvtColor(env.get_camera_image(), cv2.COLOR_BGR2RGB)
        cv2.imwrite(str(results_dir) + f"/{args.eval_task}_demo_{ep_idx:02d}_{t}_{use_aug_agent}.png", demo_img)

    rendered_clip = ImageSequenceClip(env.cache_video, fps=25)
    rendered_clip.write_videofile(str(results_dir) + f"/{args.eval_task}_demo_{t}_{use_aug_agent}.mp4")
    env.cache_video = []

    # Save the generated_eps
    baseline_agent.save_history(results_dir / f'baseline-episode{ep_idx:02d}.txt', code_ignore_list=['# ', 'update_wm', 'noop'])
    state_aug_agent.save_history(results_dir / f'state-aug-episode{ep_idx:02d}.txt', code_ignore_list=['# ', 'update_wm', 'noop'])

    env.exit()

    return generated_ep


def evaluate(prompt_dir, eval_task_name, agents, eval_episodes, task_description, model_name: str = DEFAULT_MODEL_NAME, concurrent: bool = False, results_dir: Union[str, Path] = 'results'):
    """
    If concurrent is True, the evaluation loop runs in parallel (many more calls to the API at the same time)
    """

    def make_auto_state_aug_agent(): return AutoStateAugAgent(task_description, model_name=model_name, prompt_dir=prompt_dir)
    def make_state_aug_agent(): return StateAugAgent(task_description, model_name=model_name, prompt_dir=prompt_dir)
    def make_cot_agent(): return CoTAugAgent(task_description, model_name=model_name, prompt_dir=prompt_dir)
    def make_unified_state_aug_agent(): return UnifiedStateAugAgent(task_description, model_name=model_name, prompt_dir=prompt_dir)
    def make_baseline_agent(): return BaselineAgent(task_description, model_name=model_name, prompt_dir=prompt_dir)

    # For every evaluation episode, feed user query to each agent
    num_workers = 12
    episodes_and_indices = [(ep_idx, episode) for ep_idx, episode in enumerate(eval_episodes)]

    generated_eps = []
    if concurrent:
        executor = ThreadPoolExecutor(max_workers=num_workers)
        all_tasks = [
            executor.submit(
                run_episode,
                *(eval_task_name, ep_idx, episode, make_auto_state_aug_agent, make_state_aug_agent, make_cot_agent,
                  make_unified_state_aug_agent, make_baseline_agent,
                  agents, results_dir)
            ) for ep_idx, episode in episodes_and_indices
        ]

        for task in as_completed(all_tasks):
            _ = task.result()
    else:
        for ep_idx, episode in episodes_and_indices[:2]:
            generated_ep = run_episode(eval_task_name, ep_idx, episode, make_auto_state_aug_agent, make_state_aug_agent, make_cot_agent,
                                       make_unified_state_aug_agent, make_baseline_agent, agents, results_dir=results_dir)
            generated_eps.append(generated_ep)

    # TODO: check for perfect match (generated code vs gold_code) and report the accuracy
    # List up and save the cases where the generated code is different from the gold code
    # baseline_success, unified_stateaug_success, stateaug_success = 0, 0, 0
    # for generated_ep, gold_ep in zip(generated_eps, eval_episodes):
    #     gold_ep = gold_ep['episode']
    #
    #     last_step = generated_ep[-1]
    #     gold_last_step = gold_ep[-1]
    #
    #     gold_code = cleanup_preprompt(gold_last_step['gold_code'])
    #     stateaug_generated_code = cleanup_preprompt(last_step['state_aug'])
    #     unified_stateaug_generated_code = cleanup_preprompt(last_step['unified_state_aug'])
    #     baseline_generated_code = cleanup_preprompt(last_step['baseline'])
    #
    #     baseline_success += compare(gold_code, baseline_generated_code)
    #     unified_stateaug_success += compare(gold_code, unified_stateaug_generated_code, ignore=['update_wm'])
    #     stateaug_success += compare(gold_code, stateaug_generated_code, ignore=['update_wm'])
    #     logger.info ('****** Gold Code ******')
    #     logger.info(gold_code)
    #     logger.info ('****** baseline LLM ******')
    #     logger.info(baseline_generated_code)
    #     logger.info ('****** Unified State Aug LLM ******')
    #     logger.info(unified_stateaug_generated_code)
    #     logger.info ('****** State Aug LLM (ours) ******')
    #     logger.info(stateaug_generated_code)
    #     logger.info ('*' * 20)
    #
    # logger.info(f'acc baseline: {baseline_success / len(generated_eps):.2f}, '
    #       f'acc unified stateaug: {unified_stateaug_success / len(generated_eps):.2f}'
    #       f'acc stateaug: {stateaug_success / len(generated_eps):.2f}')


def evaluate_with_simulator(prompt_dir, eval_task_name, ep_idx, episode, task_description, model_name: str = DEFAULT_MODEL_NAME):

    def make_state_aug_agent(): return StateAugAgent(task_description, model_name=model_name, prompt_dir=prompt_dir)
    def make_baseline_agent(): return BaselineAgent(task_description, model_name=model_name, prompt_dir=prompt_dir)
    run_episode_with_simulation(eval_task_name, ep_idx, episode, make_state_aug_agent, make_baseline_agent)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('eval_task', choices=['disinfection', 'weight', 'trivial_stacking', 'rebuttal_huanyu', 'real_robot'])
    parser.add_argument('--agents', default='all', choices=['all', 'baseline', 'unified_state_aug',
                                                            'cot', 'state_aug', 'auto'])
    parser.add_argument('--results-dir', default='results', type=str)
    args = parser.parse_args()
    logger.info(f'args: {args}')

    # In-context training prompt
    prompt_dir = args.eval_task

    if args.eval_task == 'disinfection':
        from cap.experiments.eval_prompts.disinfection import eval_episodes, task_description
        from cap.pybullet_demos.pybullet_disinfection_env import DisinfectionEnv as Env
    elif args.eval_task == 'weight':
        from cap.experiments.eval_prompts.weight import eval_episodes, task_description
        from cap.pybullet_demos.pybullet_weight_env import WeightEnv as Env
    elif args.eval_task == 'real_robot':
        from cap.experiments.eval_prompts.real_robot import eval_episodes, task_description
    elif args.eval_task == 'trivial_stacking':
        from cap.experiments.eval_prompts.pick_and_place import eval_episodes, task_description
        from cap.pybullet_demos.pybullet_weight_env import PickPlaceEnv as Env
    else:
        raise ValueError(f'Unknown eval_task: {args.eval_task}')

    task_description = dedent(task_description)
    evaluate(prompt_dir, args.eval_task, args.agents, eval_episodes, task_description, results_dir=args.results_dir)

    # NOTE: Run a specific episode in simulation (visualization purpose)
    # episode_idx = 0
    # use_aug_agent = False
    # evaluate_with_simulator(prompt_dir, args.eval_task, episode_idx, eval_episodes[args.i], task_description, use_aug_agent=use_aug_agent)
