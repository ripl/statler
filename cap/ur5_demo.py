import os

from cap.helpers.listener import Listener
from cap.helpers.speaker import Speaker
from cap.envs.ur5_env import UR5Env
from cap.envs.ur5_env_config import USE_MDETR

from cap.experiments.eval_prompts.real_robot import task_description
from cap.experiments.evaluate_models import StateAugAgent, BaselineAgent
from cap.helpers.prompt import cleanup_preprompt
from cap.world_model import setup_LMP


class UR5Demo:
    def __init__(self) -> None:
        # setup env and LMP
        default_pose = [0.1, -0.4, 0.4, 0.928, -0.371, 0., 0.]
        self.env = UR5Env(default_pose, use_mdetr=USE_MDETR)
        # self.env = DummyEnv(default_pose)
        self.env.reset()
        self.obj_lst = self.env.object_list
        init_states = (
            '''
            # state = {
            #     "items": ("rubiks cube", "toy duckie", "toy wheel", "yellow block"),
            #     "covers": ("red cup", "white cup", "blue cup", "black cup"),
            # }
            ''',
            '''
            # items = ("rubiks cube", "toy duckie", "toy wheel", "yellow block")
            # covers = ("red cup", "white cup", "blue cup", "black cup")
            ''',
        )
        # Statler
        # self.agent = StateAugAgent(task_description, engine='text-davinci-003', prompt_dir='real_robot')
        # self.agent.reset(init_states[0])

        # Code-as-Policies
        self.agent = BaselineAgent(task_description, engine='text-davinci-003', prompt_dir='real_robot')
        self.agent.reset(init_states[1])


        self.lmp_tabletop_ui = setup_LMP(self.env, self.agent)

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
            print('>>>>>>>>>>>>>>> Sending code and text prompt')
            response = requests.post(os.path.join(server_url, 'generated_code'), data=code_data)
            print(response)
            response = requests.post(os.path.join(server_url, 'text_prompt'), data=query_data)
            print(response)
        except Exception as e:
            print('!!!!!!!!!!! request post failed')
            import traceback
            traceback.print_exc()

        elapsed = time.time() - started
        print(f'posting code and text prompt took {elapsed}')

    def execute(self, user_input):
        try:
            user_input = cleanup_preprompt(user_input)
            generated_code = self.agent.step(user_input)
            self.lmp_tabletop_ui.execute_code_string(user_input, generated_code)
        except Exception:
            import traceback
            print('exception is captured!')
            traceback.print_exc()
            Speaker.say("Sorry, something\'s wrong. Please try again.")


if __name__ == '__main__':
    ur5_demo = UR5Demo()

    user_inputs = [
# Episode 1
[
'put the blue cup on the toy duckie',
'put the rubiks cube on the yellow block',
'put the blue cup on the toy wheel',
'put the blue cup on the yellow block',
'put the blue cup on the rubiks cube',
],
# Episode 2
[
'put the blue cup on the rubiks cube',
'put the black cup on the rubiks cube',
'put the red cup on the toy wheel',
'put the toy duckie on the rubiks cube',
'put the rubiks cube on the toy wheel',
],
# Episode 3
[
'put the white cup on the toy wheel',
'put the white cup on the yellow block',
'put the white cup on the toy wheel',
'put the black cup on the toy wheel',
'put the black cup on the rubiks cube',
],
# Episode 4
[
'put the black cup on the toy wheel',
'put the white cup on the toy duckie',
'put the red cup on the yellow block',
'put the blue cup on the toy wheel',
'put the blue cup on the toy duckie',
],
# Episode 5
[
'put the white cup on the yellow block',
'put the toy wheel on the rubiks cube',
'put the red cup on the toy duckie',
'put the yellow block on the rubiks cube',
'put the red cup on the toy wheel',
],
# Episode 6
[
'put the red cup on the yellow block',
'put the yellow block on the rubiks cube',
'put the black cup on the rubiks cube',
'put the toy wheel on the yellow block',
'put the white cup on the yellow block',
],
# Episode 7
[
'put the red cup on the rubiks cube',
'put the toy duckie on the toy wheel',
'put the blue cup on the toy duckie',
'put the white cup on the rubiks cube',
'put the white cup on the yellow block',
],
# Episode 8
[
'put the blue cup on the toy wheel',
'put the black cup on the yellow block',
'put the black cup on the toy duckie',
'put the blue cup on the rubiks cube',
'put the white cup on the toy wheel',
],
# Episode 9
[
'put the blue cup on the rubiks cube',
'put the red cup on the yellow block',
'put the black cup on the yellow block',
'put the red cup on the rubiks cube',
'put the black cup on the toy duckie',
],
# Episode 10
[
'put the red cup on the toy duckie',
'put the black cup on the rubiks cube',
'put the toy duckie on the yellow block',
'put the black cup on the yellow block',
'put the white cup on the toy wheel',
],
# Episode 11
[
'put the white cup on the toy wheel',
'put the red cup on the rubiks cube',
'put the toy wheel on the yellow block',
'put the toy wheel on the rubiks cube',
'put the black cup on the yellow block',
],
# Episode 12
[
'put the yellow block on the toy duckie',
'put the yellow block on the toy wheel',
'put the white cup on the yellow block',
'put the black cup on the yellow block',
'put the toy duckie on the rubiks cube',
],
# Episode 13
[
'put the yellow block on the rubiks cube',
'put the rubiks cube on the yellow block',
'put the blue cup on the yellow block',
'put the black cup on the toy duckie',
'put the white cup on the toy duckie',
],
# Episode 14
[
'put the black cup on the toy wheel',
'put the black cup on the rubiks cube',
'put the blue cup on the rubiks cube',
'put the toy duckie on the yellow block',
'put the black cup on the rubiks cube',
],
# Episode 15
[
'put the black cup on the toy duckie',
'put the red cup on the rubiks cube',
'put the red cup on the toy duckie',
'put the toy wheel on the yellow block',
'put the blue cup on the yellow block',
],
# Episode 16
[
'put the red cup on the toy duckie',
'put the red cup on the yellow block',
'put the red cup on the toy duckie',
'put the toy wheel on the yellow block',
'put the red cup on the toy wheel',
],
# Episode 17
[
'put the blue cup on the yellow block',
'put the red cup on the rubiks cube',
'put the white cup on the yellow block',
'put the blue cup on the yellow block',
'put the black cup on the toy wheel',
],
# Episode 18
[
'put the black cup on the rubiks cube',
'put the rubiks cube on the toy wheel',
'put the black cup on the rubiks cube',
'put the black cup on the yellow block',
'put the blue cup on the toy wheel',
],
# Episode 19
[
'put the yellow block on the toy wheel',
'put the white cup on the rubiks cube',
'put the red cup on the toy wheel',
'put the toy wheel on the yellow block',
'put the blue cup on the toy wheel',
],
# Episode 20
[
'put the black cup on the rubiks cube',
'put the blue cup on the rubiks cube',
'put the black cup on the toy wheel',
'put the red cup on the rubiks cube',
'put the blue cup on the toy wheel',
],
]


    episodes_to_try = [3]
    start_ep = 9
    i = start_ep - 1
    num_episodes = start_ep


    # import numpy as np
    from pathlib import Path
    # ur5_demo.env.reset()
    ur5_demo.env.arm.moveto_xyz(ur5_demo.env.arm.viewing_pos)
    input('press enter')
    # rgb, depth, position, orientation, intrinsics = ur5_demo.env.render_image()
    # obj_names = ['toy wheel', 'toy duckie', 'yellow block', 'white cup', 'black cup', 'red cup']
    # for obj_name in obj_names:
    #     masks, plt = ur5_demo.env.get_text_mask(rgb, obj_name, return_plt=True)
    #     directory = Path('mdetr_init')
    #     directory.mkdir(parents=True, exist_ok=True)
    #     plt.savefig(directory / f'{obj_name.replace(" ", "_")}.png')
    # mean_img = np.asarray(imgs).mean(axis=0)
    # from PIL import Image
    # im = Image.fromarray(mean_img.astype(np.uint8))
    # im.save("mdetr_init.png")

    # import sys; sys.exit(0)


    for ep in episodes_to_try:
    # while i<num_episodes:
        # input(f'press any key to start episode {ep+1}')
        episode = user_inputs[ep]
        for user_input in episode:
            ur5_demo.execute(user_input)
        i+=1

    # while True:
    #     print('> ', end='')
    #     user_query = input()
    #     if user_query == 'exit':
    #         break
    #     ur5_demo.execute(user_query)

    # listen = Listener().listen()
    # while True:
    #     user_input = next(listen)
    #     print('user_input:', user_input)
    #     if user_input:
    #         ur5_demo.execute(user_input)
    #         if ur5_demo.env.success is not None:
    #             if ur5_demo.env.success:
    #                 Speaker.say("Job finished.")
    #             else:
    #                 Speaker.say("Sorry, something went wrong")
    #             ur5_demo.env.success = None
    #     else:
    #         Speaker.say(f'Sorry, I can\'t hear you.')
