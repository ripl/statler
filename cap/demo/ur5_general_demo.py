"""A general demo for Code-as-Policies"""

from __future__ import annotations
import os

from cap.helpers.listener import Listener, DummyListener
from cap.helpers.speaker import Speaker
from cap.envs.ur5_env import UR5Env
from cap.envs.ur5_env_config import USE_MDETR

from cap.experiments.eval_prompts.real_robot import task_description
from cap.experiments.evaluate_models import StateAugAgent, BaselineAgent, AbstractAgent
from cap.helpers.prompt import cleanup_preprompt
from cap.world_model import setup_LMP
from cap.envs.dummy_env import DummyEnv
from typing import List
from cap.helpers import logger


class UR5DemoFactory:
    @staticmethod
    def create_statler_demo(task_description, prompt_dir, init_state: dict, obj_list: List[str] | None = None, dummy: bool = False) -> UR5Demo:
        agent = StateAugAgent(task_description, prompt_dir)
        if dummy:
            env = DummyEnv()
        else:
            env = UR5Env(use_mdetr=USE_MDETR)
        return UR5Demo(agent, env, init_state, obj_list)

    @staticmethod
    def create_cap_demo(task_description, prompt_dir, init_state: dict, obj_list: List[str] | None = None, dummy: bool = False) -> UR5Demo:
        agent = BaselineAgent(task_description, prompt_dir, keep_history=False)
        if dummy:
            env = DummyEnv()
        else:
            env = UR5Env(use_mdetr=USE_MDETR)
        return UR5Demo(agent, env, init_state, obj_list)


class UR5Demo:
    def __init__(self, agent: AbstractAgent, env: UR5Env, init_state: dict, obj_list: List[str] | None = None) -> None:
        self.env = env
        self.env.reset()
        self.obj_list = obj_list or self.env.object_list
        self.agent = agent
        self.agent.reset(init_state)
        self.lmp_tabletop_ui = setup_LMP(env, agent)

    def post_to_flask(self, data):
        # Post the generated code string
        """The callback passed to LMP.__call__

        Args:
            data (dict): keys are `query`, `code_str`, `context`
        """
        import json
        import time

        import requests
        server_url = 'http://localhost:5000'
        code_data = json.dumps({'code': data['code_str']})
        query_data = json.dumps({'text': data['query']})

        started = time.time()
        try:
            logger.info('>>>>>>>>>>>>>>> Sending code and text prompt')
            response = requests.post(os.path.join(server_url, 'generated_code'), data=code_data)
            logger.info(response)
            response = requests.post(os.path.join(server_url, 'text_prompt'), data=query_data)
            logger.info(response)
        except Exception as e:
            logger.info('!!!!!!!!!!! request post failed')
            import traceback
            traceback.print_exc()

        elapsed = time.time() - started
        logger.info(f'posting code and text prompt took {elapsed}')

    def execute(self, user_input):
        try:
            # self.lmp_tabletop_ui(user_input, f'objects = {self.env.object_list}', callback=self.post_to_flask)
            user_input = cleanup_preprompt(user_input)
            generated_code = self.agent.step(user_input)
            self.lmp_tabletop_ui.execute_code_string(user_input, generated_code, callback=self.post_to_flask)
        except Exception:
            import traceback
            traceback.print_exc()
            Speaker.say("Sorry, something\'s wrong. Please try again.")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--dummy-arm', action='store_true', help='Use dummy arm')
    parser.add_argument('--observe', action='store_true', help='Simply move to the observe pose and exit. Helpful to figure out the observable region')
    args = parser.parse_args()

    def quote(e): return f"'{e}'"
    obj_list = ['toy wheel', 'toy duckie', 'yellow block', 'rubiks cube', 'toy banana', 'toy bread', 'toy butter', 'toy milk', 'toy fish', 'hand']
    init_state = f"objects = [{','.join([quote(e) for e in obj_list])}]"
    prompt_dir = 'real_robot_demo'

    ur5_demo = UR5DemoFactory.create_cap_demo(task_description, prompt_dir, init_state, obj_list, dummy=args.dummy_arm)

    if args.observe:
        assert not args.dummy_arm
        ur5_demo.env.arm.moveto_xyz(ur5_demo.env.arm.viewing_pos)
        import sys; sys.exit(0)

    ## Test MDetr ###
    if args.debug:
        assert not args.dummy_arm
        from pathlib import Path
        ur5_demo.env.arm.moveto_xyz(ur5_demo.env.arm.viewing_pos)
        input('press enter')
        rgb, depth, position, orientation, intrinsics = ur5_demo.env.render_image()
        for obj_name in obj_list:
            masks, plt = ur5_demo.env.get_text_mask(rgb, obj_name, return_plt=True)
            directory = Path('mdetr_init')
            directory.mkdir(parents=True, exist_ok=True)
            plt.savefig(directory / f'{obj_name.replace(" ", "_")}.png')

        print('saved images under', directory.resolve())

    if args.debug:
        queries = [
            # 'put the toy wheel on the rubiks cube',
            'put the rubiks cube at the north of the toy butter'
        ]
        listen = DummyListener().listen(queries)
    else:
        listen = Listener().listen()

    while True:
        user_input = next(listen)
        print('user_input:', user_input)
        if user_input:
            ur5_demo.execute(user_input)
            if ur5_demo.env.success is not None:
                if ur5_demo.env.success:
                    Speaker.say("Job finished.")
                else:
                    Speaker.say("Sorry, something went wrong")
                ur5_demo.env.success = None
        else:
            Speaker.say(f'Sorry, I can\'t hear you.')
