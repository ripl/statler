from textwrap import dedent

from cap.experiments.evaluate_models import StateAugAgent

prompt_dir = 'real_robot'
task_descriptions = '''
    In this task, the robot is presented with a tabletop of objects, some of which are used as cover.
    The robot is asked to perform pick and place operations, and must act according to the following rules:
    * The robot can pick up one object at a time.
    * The robot can place an object on another object or empty space.
    * The robot cannot place anything on a cover.
    * Once an object is under another object, the robot must first put away the top object before interacting with the bottom one.
    The robot can only call the following functions: `put_first_on_second`, `update_wm` and `say`.
    '''

init_world_states = '''
    # state = {
    #     "objects": ("rubiks cube", "toy duckie", "toy wheel", "yellow block"),
    #     "covers": ("red cup", "green cup", "blue cup", "black cup"),
    #     "rubiks cube": {"under": "blue cup"},
    #     "toy wheel": {"on": "yellow block"},
    #     "yellow block": {"under": "toy wheel"},
    #     "blue cup": {"on": "rubiks cube"},
    # }
    '''

state_aug_agent = StateAugAgent(dedent(task_descriptions), prompt_dir=prompt_dir)
state_aug_agent.reset(dedent(init_world_states))

user_query = "Put the toy wheel on the Rubik's cube."
state_aug_agent.step(user_query)

print('== resulting state ==')
print(state_aug_agent.world_state)
