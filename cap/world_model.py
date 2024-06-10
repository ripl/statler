#!/usr/bin/env python3
import numpy as np
import shapely
from shapely.affinity import *
from shapely.geometry import *
from cap.helpers.speaker import Speaker

from cap.envs.dummy_env import DummyEnv
from cap.helpers import call_api
from cap.lmp import LMP, LMPFGen
from cap.helpers.prompt import cleanup_preprompt, load_prompts

base_conf = {
    'engine': 'text-davinci-003',
    'max_tokens': 256,
    'temperature': 0,
    'query_prefix': '# ',
    'query_suffix': '.',
    'stop': ['# '],
    'maintain_session': False,
    'debug_mode': False,
    'include_context': True,
    'has_return': True,
    'return_val_name': 'ret_val',
}

prompts = load_prompts()
cfg_tabletop_lmps = {
    'tabletop_ui': {
        **base_conf,
        'prompt_text': prompts['prompts.wm_reader'],
        'has_return': False,
    },
    'parse_obj_name': {
        **base_conf,
        'prompt_text': prompts['prompts.functions.parse_obj_name'],
    },
    'parse_position': {
        **base_conf,
        'prompt_text': prompts['prompts.functions.parse_position'],
    },
    'parse_question': {
        **base_conf,
        'prompt_text': prompts['prompts.functions.parse_question'],
    },
    'transform_shape_pts': {
        **base_conf,
        'prompt_text': prompts['prompts.functions.transform_shape_pts'],
        'return_val_name': 'new_shape_pts',
    },
    'fgen': {
        **base_conf,
        'prompt_text': prompts['prompts.functions.fgen'],
        'query_prefix': '# define function: ',
        'stop': ['# define', '# example'],
    },
    'update_wm': {
        **base_conf,
        'prompt_text': prompts['prompts.wm_updater'],
        'return_val_name': 'world_state'
    }
}


gpt_config = {
    'stop': ['# '],
    'temperature': 0,
    'max_tokens': 256
}


def run_wm_separately(engine, world_state):
    """Interactively run WM reader and WM updater separately.

    Args:
        engine (str): _description_
        world_state (str): _description_
    """
    first_time = True
    prompts = load_prompts()

    while True:
        print('========= current world state =========')
        print(world_state)
        print('===========================')
        # print('Type your command starting with `read: <your-query>` or `update: <your-query>`\n> ', end='')
        print('> ', end='')
        command = input()
        needs_update = False
        if command.startswith("read: "):
            preprompt = prompts['wm_reader']
            _prompt = command[len("read: "):]
            prompt = f'# {_prompt}\n'
        elif command.startswith("update: "):
            needs_update = True
            preprompt = prompts['wm_updater']
            preprompt += '\n# reset'
            _prompt = command[len("update: "):]
            prompt = f'# {_prompt}\nworld_state = '
        else:
            print('Make sure to start your command with `read: ` or `update: `')
            print('Doing nothing...')
            continue

        prompt = '\n'.join((preprompt, world_state, prompt))

        generated = call_api(
            engine,
            prompt,
            report_usage=first_time,
        )

        if needs_update:
            world_state = generated
        else:
            lines = generated.split('\n')
            print('[generated]:')
            for line in lines:
                print(f'  {line}')

        first_time = False


def run_wm(lmp, lmp_wm):
    while True:
        print('========= current world state =========')
        print(lmp_wm.state)
        print('===========================')
        # print('Type your command starting with `read: <your-query>` or `update: <your-query>`\n> ', end='')
        print('> ', end='')
        command = input()

        lmp(command, context=lmp_wm.commented_state)


def noop(fname, *args, **kwargs):
    print(f"==> Dry-running {fname}\targs: {args}\tkwargs: {kwargs}")


def setup_LMP(env, lmp_wm, dry_run: bool = False):
    import functools

    from cap.lmp_warpper import LMP_wrapper

    lmp_tabletop_coords = {
        'top_left': (-0.3 + 0.05, -0.2 - 0.05),
        'top_side': (0, -0.2 - 0.05),
        'top_right': (0.3 - 0.05, -0.2 - 0.05),
        'left_side': (-0.3 + 0.05, -0.5,),
        'middle': (0, -0.5,),
        'right_side': (0.3 - 0.05, -0.5,),
        'bottom_left': (-0.3 + 0.05, -0.8 + 0.05),
        'bottom_side': (0, -0.8 + 0.05),
        'bottom_right': (0.3 - 0.05, -0.8 + 0.05),
        'table_z': 0.0,
    }

    # LMP env wrapper
    cfg_env = {'env': {'init_objs': env.object_list, 'coords': lmp_tabletop_coords}}
    lmp_env = LMP_wrapper(env, cfg_env)

    # creating APIs that the LMPs can call directly
    fixed_vars = {'np': np}
    fixed_vars.update({name: eval(name) if not dry_run else functools.partial(noop, name)
                       for name in shapely.geometry.__all__ + shapely.affinity.__all__})

    env_fns = ['get_bbox', 'get_obj_pos', 'get_obj_pose', 'pick', 'place', 'get_color',
               'is_obj_visible', 'denormalize_xy', 'put_first_on_second',
               'get_obj_names', 'get_corner_name', 'get_side_name', 'open_object', 'close_object']
    wm_fns = ['update_wm']

    variable_vars = {}
    for fname in env_fns:
        variable_vars[fname] = getattr(lmp_env, fname)

    # This is a duplicator world model updator
    # However, if we comment it out, the model will attempt to write an updator
    for fname in wm_fns:
        variable_vars[fname] = getattr(lmp_wm, fname)

    variable_vars['say'] = lambda msg: Speaker.say(msg)
    # variable_vars['say'] = lambda msg: print('robot speaking:', msg)

    # creating the function-generating LMP
    lmp_fgen = LMPFGen(cfg_tabletop_lmps['fgen'], fixed_vars, variable_vars)

    # creating other low-level LMPs
    variable_vars.update({
        k: LMP(k, cfg_tabletop_lmps[k], lmp_fgen, fixed_vars, variable_vars)
        for k in ['parse_obj_name', 'parse_position', 'parse_question', 'transform_shape_pts']
    })

    if dry_run:
        # Overwrite every function with noop
        for fname in variable_vars:
            if fname in ['update_wm']:
                continue
            variable_vars[fname] = functools.partial(noop, fname)

    # creating the LMP that deals w/ high-level language commands
    lmp_tabletop_ui = LMP('tabletop_ui', cfg_tabletop_lmps['tabletop_ui'], lmp_fgen, fixed_vars, variable_vars)
    return lmp_tabletop_ui


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--engine', type=str, choices=['text-davinci-003', 'gpt-4'], default='gpt-4')
    parser.add_argument('--unified', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    # Minimal example to read from and update the world model
    init_world_state = '''
    world_state = {
        "object_list":  ["red block", "rainbow block", "wallet", "toy dinosaur"],
        "object_state": {
            "drawer": {"is": "open"},
            "contains": {"wallet"},
            "stacked": [
                ["red block" is under "rainbow block" is under "toy dinosaur"],
                ["wallet"]
            ],
            "red block": {"is": "flammable", "has": "a face drawn on it"}
        }
    }
    '''
    world_state = cleanup_preprompt(init_world_state)
    engine = args.engine

    if args.unified:
        # setup env and LMP
        default_pose = [0.1, -0.4, 0.4, 0.928, -0.371, 0., 0.]
        # self.env = UR5Env(default_pose, use_mdetr=USE_MDETR)
        env = DummyEnv(default_pose)
        env.reset()
        lmp, lmp_wm = setup_LMP(env, init_state=world_state, dry_run=args.dry_run)
        run_wm(lmp, lmp_wm)
    else:
        run_wm_separately(engine, world_state)
