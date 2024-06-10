import numpy as np

task_description = '''
In this task, the robot sees objects on a table. Some are used for cover, others are regular items. A human user asks the robot to pick up and put down objects, following these rules:
* The robot can grab one object at a time.
* The robot can place an object on a regular item or empty space.
* The robot should put away the top object before dealing with the bottom one.
* The robot can call these functions: {list_of_functions}.
'''

eval_episodes = [
    {
        'init_state': '''
        # state = {
        #     "items": ("rubiks cube", "toy duckie", "toy wheel", "yellow block"),
        #     "covers": ("red cup", "green cup", "blue cup", "black cup"),
        # }
        ''',
        'init_simple_state': '''
        # items = ("rubiks cube", "toy duckie", "toy wheel", "yellow block")
        # covers = ("red cup", "green cup", "blue cup", "black cup")
        ''',
        'episode': [
            {
                'user_query': 'put the blue cup on the toy duckie',
                'gold_code': '''
                put_first_on_second("blue cup", "toy duckie")
                update_wm("Put the blue cup on the toy duckie.")
                '''
            },
            {
                'user_query': 'put the rubiks cube on the yellow block',
                'gold_code': '''
                put_first_on_second("rubiks cube", "yellow block")
                update_wm("Put the rubiks cube on the yellow block.")
                '''
            },
            {
                'user_query': 'put the blue cup on the toy wheel',
                'gold_code': '''
                put_first_on_second("blue cup", "toy wheel")
                update_wm("Put the blue cup on the toy wheel.")
                '''
            },
            {
                'user_query': 'put the blue cup on the yellow block',
                'gold_code': '''
                put_first_on_second("rubiks cube", "empty space")
                update_wm("Put the rubiks cube on the empty space.")
                put_first_on_second("blue cup", "yellow block")
                update_wm("Put the blue cup on the yellow block.")
                '''
            },
            {
                'user_query': 'put the blue cup on the rubiks cube',
                'gold_code': '''
                put_first_on_second("blue cup", "rubiks cube")
                update_wm("Put the blue cup on the rubiks cube.")
                '''
            },
        ]
    },
    {
        'init_state': '''
        # state = {
        #     "items": ("rubiks cube", "toy duckie", "toy wheel", "yellow block"),
        #     "covers": ("red cup", "green cup", "blue cup", "black cup"),
        # }
        ''',
        'init_simple_state': '''
        # items = ("rubiks cube", "toy duckie", "toy wheel", "yellow block")
        # covers = ("red cup", "green cup", "blue cup", "black cup")
        ''',
        'episode': [
            {
                'user_query': 'put the blue cup on the rubiks cube',
                'gold_code': '''
                put_first_on_second("blue cup", "rubiks cube")
                update_wm("Put the blue cup on the rubiks cube.")
                '''
            },
            {
                'user_query': 'put the black cup on the rubiks cube',
                'gold_code': '''
                put_first_on_second("blue cup", "empty space")
                update_wm("Put the blue cup on the empty space.")
                put_first_on_second("black cup", "rubiks cube")
                update_wm("Put the black cup on the rubiks cube.")
                '''
            },
            {
                'user_query': 'put the red cup on the toy wheel',
                'gold_code': '''
                put_first_on_second("red cup", "toy wheel")
                update_wm("Put the red cup on the toy wheel.")
                '''
            },
            {
                'user_query': 'put the toy duckie on the rubiks cube',
                'gold_code': '''
                put_first_on_second("black cup", "empty space")
                update_wm("Put the black cup on the empty space.")
                put_first_on_second("toy duckie", "rubiks cube")
                update_wm("Put the toy duckie on the rubiks cube.")
                '''
            },
            {
                'user_query': 'put the rubiks cube on the toy wheel',
                'gold_code': '''
                put_first_on_second("toy duckie", "empty space")
                update_wm("Put the toy duckie on the empty space.")
                put_first_on_second("red cup", "empty space")
                update_wm("Put the red cup on the empty space.")
                put_first_on_second("rubiks cube", "toy wheel")
                update_wm("Put the rubiks cube on the toy wheel.")
                '''
            },
        ]
    },
    {
        'init_state': '''
        # state = {
        #     "items": ("rubiks cube", "toy duckie", "toy wheel", "yellow block"),
        #     "covers": ("red cup", "green cup", "blue cup", "black cup"),
        # }
        ''',
        'init_simple_state': '''
        # items = ("rubiks cube", "toy duckie", "toy wheel", "yellow block")
        # covers = ("red cup", "green cup", "blue cup", "black cup")
        ''',
        'episode': [
            {
                'user_query': 'put the green cup on the toy wheel',
                'gold_code': '''
                put_first_on_second("green cup", "toy wheel")
                update_wm("Put the green cup on the toy wheel.")
                '''
            },
            {
                'user_query': 'put the green cup on the yellow block',
                'gold_code': '''
                put_first_on_second("green cup", "yellow block")
                update_wm("Put the green cup on the yellow block.")
                '''
            },
            {
                'user_query': 'put the green cup on the toy wheel',
                'gold_code': '''
                put_first_on_second("green cup", "toy wheel")
                update_wm("Put the green cup on the toy wheel.")
                '''
            },
            {
                'user_query': 'put the black cup on the toy wheel',
                'gold_code': '''
                put_first_on_second("green cup", "empty space")
                update_wm("Put the green cup on the empty space.")
                put_first_on_second("black cup", "toy wheel")
                update_wm("Put the black cup on the toy wheel.")
                '''
            },
            {
                'user_query': 'put the black cup on the rubiks cube',
                'gold_code': '''
                put_first_on_second("black cup", "rubiks cube")
                update_wm("Put the black cup on the rubiks cube.")
                '''
            },
        ]
    },
    {
        'init_state': '''
        # state = {
        #     "items": ("rubiks cube", "toy duckie", "toy wheel", "yellow block"),
        #     "covers": ("red cup", "green cup", "blue cup", "black cup"),
        # }
        ''',
        'init_simple_state': '''
        # items = ("rubiks cube", "toy duckie", "toy wheel", "yellow block")
        # covers = ("red cup", "green cup", "blue cup", "black cup")
        ''',
        'episode': [
            {
                'user_query': 'put the black cup on the toy wheel',
                'gold_code': '''
                put_first_on_second("black cup", "toy wheel")
                update_wm("Put the black cup on the toy wheel.")
                '''
            },
            {
                'user_query': 'put the green cup on the toy duckie',
                'gold_code': '''
                put_first_on_second("green cup", "toy duckie")
                update_wm("Put the green cup on the toy duckie.")
                '''
            },
            {
                'user_query': 'put the red cup on the yellow block',
                'gold_code': '''
                put_first_on_second("red cup", "yellow block")
                update_wm("Put the red cup on the yellow block.")
                '''
            },
            {
                'user_query': 'put the blue cup on the toy wheel',
                'gold_code': '''
                put_first_on_second("black cup", "empty space")
                update_wm("Put the black cup on the empty space.")
                put_first_on_second("blue cup", "toy wheel")
                update_wm("Put the blue cup on the toy wheel.")
                '''
            },
            {
                'user_query': 'put the blue cup on the toy duckie',
                'gold_code': '''
                put_first_on_second("green cup", "empty space")
                update_wm("Put the green cup on the empty space.")
                put_first_on_second("blue cup", "toy duckie")
                update_wm("Put the blue cup on the toy duckie.")
                '''
            },
        ]
    },
    {
        'init_state': '''
        # state = {
        #     "items": ("rubiks cube", "toy duckie", "toy wheel", "yellow block"),
        #     "covers": ("red cup", "green cup", "blue cup", "black cup"),
        # }
        ''',
        'init_simple_state': '''
        # items = ("rubiks cube", "toy duckie", "toy wheel", "yellow block")
        # covers = ("red cup", "green cup", "blue cup", "black cup")
        ''',
        'episode': [
            {
                'user_query': 'put the green cup on the yellow block',
                'gold_code': '''
                put_first_on_second("green cup", "yellow block")
                update_wm("Put the green cup on the yellow block.")
                '''
            },
            {
                'user_query': 'put the toy wheel on the rubiks cube',
                'gold_code': '''
                put_first_on_second("toy wheel", "rubiks cube")
                update_wm("Put the toy wheel on the rubiks cube.")
                '''
            },
            {
                'user_query': 'put the red cup on the toy duckie',
                'gold_code': '''
                put_first_on_second("red cup", "toy duckie")
                update_wm("Put the red cup on the toy duckie.")
                '''
            },
            {
                'user_query': 'put the yellow block on the rubiks cube',
                'gold_code': '''
                put_first_on_second("green cup", "empty space")
                update_wm("Put the green cup on the empty space.")
                put_first_on_second("toy wheel", "empty space")
                update_wm("Put the toy wheel on the empty space.")
                put_first_on_second("yellow block", "rubiks cube")
                update_wm("Put the yellow block on the rubiks cube.")
                '''
            },
            {
                'user_query': 'put the red cup on the toy wheel',
                'gold_code': '''
                put_first_on_second("red cup", "toy wheel")
                update_wm("Put the red cup on the toy wheel.")
                '''
            },
        ]
    },
    {
        'init_state': '''
        # state = {
        #     "items": ("rubiks cube", "toy duckie", "toy wheel", "yellow block"),
        #     "covers": ("red cup", "green cup", "blue cup", "black cup"),
        # }
        ''',
        'init_simple_state': '''
        # items = ("rubiks cube", "toy duckie", "toy wheel", "yellow block")
        # covers = ("red cup", "green cup", "blue cup", "black cup")
        ''',
        'episode': [
            {
                'user_query': 'put the red cup on the yellow block',
                'gold_code': '''
                put_first_on_second("red cup", "yellow block")
                update_wm("Put the red cup on the yellow block.")
                '''
            },
            {
                'user_query': 'put the yellow block on the rubiks cube',
                'gold_code': '''
                put_first_on_second("red cup", "empty space")
                update_wm("Put the red cup on the empty space.")
                put_first_on_second("yellow block", "rubiks cube")
                update_wm("Put the yellow block on the rubiks cube.")
                '''
            },
            {
                'user_query': 'put the black cup on the rubiks cube',
                'gold_code': '''
                put_first_on_second("yellow block", "empty space")
                update_wm("Put the yellow block on the empty space.")
                put_first_on_second("black cup", "rubiks cube")
                update_wm("Put the black cup on the rubiks cube.")
                '''
            },
            {
                'user_query': 'put the toy wheel on the yellow block',
                'gold_code': '''
                put_first_on_second("toy wheel", "yellow block")
                update_wm("Put the toy wheel on the yellow block.")
                '''
            },
            {
                'user_query': 'put the green cup on the yellow block',
                'gold_code': '''
                put_first_on_second("toy wheel", "empty space")
                update_wm("Put the toy wheel on the empty space.")
                put_first_on_second("green cup", "yellow block")
                update_wm("Put the green cup on the yellow block.")
                '''
            },
        ]
    },
    {
        'init_state': '''
        # state = {
        #     "items": ("rubiks cube", "toy duckie", "toy wheel", "yellow block"),
        #     "covers": ("red cup", "green cup", "blue cup", "black cup"),
        # }
        ''',
        'init_simple_state': '''
        # items = ("rubiks cube", "toy duckie", "toy wheel", "yellow block")
        # covers = ("red cup", "green cup", "blue cup", "black cup")
        ''',
        'episode': [
            {
                'user_query': 'put the red cup on the rubiks cube',
                'gold_code': '''
                put_first_on_second("red cup", "rubiks cube")
                update_wm("Put the red cup on the rubiks cube.")
                '''
            },
            {
                'user_query': 'put the toy duckie on the toy wheel',
                'gold_code': '''
                put_first_on_second("toy duckie", "toy wheel")
                update_wm("Put the toy duckie on the toy wheel.")
                '''
            },
            {
                'user_query': 'put the blue cup on the toy duckie',
                'gold_code': '''
                put_first_on_second("toy duckie", "empty space")
                update_wm("Put the toy duckie on the empty space.")
                put_first_on_second("blue cup", "toy duckie")
                update_wm("Put the blue cup on the toy duckie.")
                '''
            },
            {
                'user_query': 'put the green cup on the rubiks cube',
                'gold_code': '''
                put_first_on_second("red cup", "empty space")
                update_wm("Put the red cup on the empty space.")
                put_first_on_second("green cup", "rubiks cube")
                update_wm("Put the green cup on the rubiks cube.")
                '''
            },
            {
                'user_query': 'put the green cup on the yellow block',
                'gold_code': '''
                put_first_on_second("green cup", "yellow block")
                update_wm("Put the green cup on the yellow block.")
                '''
            },
        ]
    },
    {
        'init_state': '''
        # state = {
        #     "items": ("rubiks cube", "toy duckie", "toy wheel", "yellow block"),
        #     "covers": ("red cup", "green cup", "blue cup", "black cup"),
        # }
        ''',
        'init_simple_state': '''
        # items = ("rubiks cube", "toy duckie", "toy wheel", "yellow block")
        # covers = ("red cup", "green cup", "blue cup", "black cup")
        ''',
        'episode': [
            {
                'user_query': 'put the blue cup on the toy wheel',
                'gold_code': '''
                put_first_on_second("blue cup", "toy wheel")
                update_wm("Put the blue cup on the toy wheel.")
                '''
            },
            {
                'user_query': 'put the black cup on the yellow block',
                'gold_code': '''
                put_first_on_second("black cup", "yellow block")
                update_wm("Put the black cup on the yellow block.")
                '''
            },
            {
                'user_query': 'put the black cup on the toy duckie',
                'gold_code': '''
                put_first_on_second("black cup", "toy duckie")
                update_wm("Put the black cup on the toy duckie.")
                '''
            },
            {
                'user_query': 'put the blue cup on the rubiks cube',
                'gold_code': '''
                put_first_on_second("blue cup", "rubiks cube")
                update_wm("Put the blue cup on the rubiks cube.")
                '''
            },
            {
                'user_query': 'put the green cup on the toy wheel',
                'gold_code': '''
                put_first_on_second("green cup", "toy wheel")
                update_wm("Put the green cup on the toy wheel.")
                '''
            },
        ]
    },
    {
        'init_state': '''
        # state = {
        #     "items": ("rubiks cube", "toy duckie", "toy wheel", "yellow block"),
        #     "covers": ("red cup", "green cup", "blue cup", "black cup"),
        # }
        ''',
        'init_simple_state': '''
        # items = ("rubiks cube", "toy duckie", "toy wheel", "yellow block")
        # covers = ("red cup", "green cup", "blue cup", "black cup")
        ''',
        'episode': [
            {
                'user_query': 'put the blue cup on the rubiks cube',
                'gold_code': '''
                put_first_on_second("blue cup", "rubiks cube")
                update_wm("Put the blue cup on the rubiks cube.")
                '''
            },
            {
                'user_query': 'put the red cup on the yellow block',
                'gold_code': '''
                put_first_on_second("red cup", "yellow block")
                update_wm("Put the red cup on the yellow block.")
                '''
            },
            {
                'user_query': 'put the black cup on the yellow block',
                'gold_code': '''
                put_first_on_second("red cup", "empty space")
                update_wm("Put the red cup on the empty space.")
                put_first_on_second("black cup", "yellow block")
                update_wm("Put the black cup on the yellow block.")
                '''
            },
            {
                'user_query': 'put the red cup on the rubiks cube',
                'gold_code': '''
                put_first_on_second("blue cup", "empty space")
                update_wm("Put the blue cup on the empty space.")
                put_first_on_second("red cup", "rubiks cube")
                update_wm("Put the red cup on the rubiks cube.")
                '''
            },
            {
                'user_query': 'put the black cup on the toy duckie',
                'gold_code': '''
                put_first_on_second("black cup", "toy duckie")
                update_wm("Put the black cup on the toy duckie.")
                '''
            },
        ]
    },
    {
        'init_state': '''
        # state = {
        #     "items": ("rubiks cube", "toy duckie", "toy wheel", "yellow block"),
        #     "covers": ("red cup", "green cup", "blue cup", "black cup"),
        # }
        ''',
        'init_simple_state': '''
        # items = ("rubiks cube", "toy duckie", "toy wheel", "yellow block")
        # covers = ("red cup", "green cup", "blue cup", "black cup")
        ''',
        'episode': [
            {
                'user_query': 'put the red cup on the toy duckie',
                'gold_code': '''
                put_first_on_second("red cup", "toy duckie")
                update_wm("Put the red cup on the toy duckie.")
                '''
            },
            {
                'user_query': 'put the black cup on the rubiks cube',
                'gold_code': '''
                put_first_on_second("black cup", "rubiks cube")
                update_wm("Put the black cup on the rubiks cube.")
                '''
            },
            {
                'user_query': 'put the toy duckie on the yellow block',
                'gold_code': '''
                put_first_on_second("red cup", "empty space")
                update_wm("Put the red cup on the empty space.")
                put_first_on_second("toy duckie", "yellow block")
                update_wm("Put the toy duckie on the yellow block.")
                '''
            },
            {
                'user_query': 'put the black cup on the yellow block',
                'gold_code': '''
                put_first_on_second("toy duckie", "empty space")
                update_wm("Put the toy duckie on the empty space.")
                put_first_on_second("black cup", "yellow block")
                update_wm("Put the black cup on the yellow block.")
                '''
            },
            {
                'user_query': 'put the green cup on the toy wheel',
                'gold_code': '''
                put_first_on_second("green cup", "toy wheel")
                update_wm("Put the green cup on the toy wheel.")
                '''
            },
        ]
    },
    {
        'init_state': '''
        # state = {
        #     "items": ("rubiks cube", "toy duckie", "toy wheel", "yellow block"),
        #     "covers": ("red cup", "green cup", "blue cup", "black cup"),
        # }
        ''',
        'init_simple_state': '''
        # items = ("rubiks cube", "toy duckie", "toy wheel", "yellow block")
        # covers = ("red cup", "green cup", "blue cup", "black cup")
        ''',
        'episode': [
            {
                'user_query': 'put the green cup on the toy wheel',
                'gold_code': '''
                put_first_on_second("green cup", "toy wheel")
                update_wm("Put the green cup on the toy wheel.")
                '''
            },
            {
                'user_query': 'put the red cup on the rubiks cube',
                'gold_code': '''
                put_first_on_second("red cup", "rubiks cube")
                update_wm("Put the red cup on the rubiks cube.")
                '''
            },
            {
                'user_query': 'put the toy wheel on the yellow block',
                'gold_code': '''
                put_first_on_second("green cup", "empty space")
                update_wm("Put the green cup on the empty space.")
                put_first_on_second("toy wheel", "yellow block")
                update_wm("Put the toy wheel on the yellow block.")
                '''
            },
            {
                'user_query': 'put the toy wheel on the rubiks cube',
                'gold_code': '''
                put_first_on_second("red cup", "empty space")
                update_wm("Put the red cup on the empty space.")
                put_first_on_second("toy wheel", "rubiks cube")
                update_wm("Put the toy wheel on the rubiks cube.")
                '''
            },
            {
                'user_query': 'put the black cup on the yellow block',
                'gold_code': '''
                put_first_on_second("black cup", "yellow block")
                update_wm("Put the black cup on the yellow block.")
                '''
            },
        ]
    },
    {
        'init_state': '''
        # state = {
        #     "items": ("rubiks cube", "toy duckie", "toy wheel", "yellow block"),
        #     "covers": ("red cup", "green cup", "blue cup", "black cup"),
        # }
        ''',
        'init_simple_state': '''
        # items = ("rubiks cube", "toy duckie", "toy wheel", "yellow block")
        # covers = ("red cup", "green cup", "blue cup", "black cup")
        ''',
        'episode': [
            {
                'user_query': 'put the yellow block on the toy duckie',
                'gold_code': '''
                put_first_on_second("yellow block", "toy duckie")
                update_wm("Put the yellow block on the toy duckie.")
                '''
            },
            {
                'user_query': 'put the yellow block on the toy wheel',
                'gold_code': '''
                put_first_on_second("yellow block", "toy wheel")
                update_wm("Put the yellow block on the toy wheel.")
                '''
            },
            {
                'user_query': 'put the green cup on the yellow block',
                'gold_code': '''
                put_first_on_second("yellow block", "empty space")
                update_wm("Put the yellow block on the empty space.")
                put_first_on_second("green cup", "yellow block")
                update_wm("Put the green cup on the yellow block.")
                '''
            },
            {
                'user_query': 'put the black cup on the yellow block',
                'gold_code': '''
                put_first_on_second("green cup", "empty space")
                update_wm("Put the green cup on the empty space.")
                put_first_on_second("black cup", "yellow block")
                update_wm("Put the black cup on the yellow block.")
                '''
            },
            {
                'user_query': 'put the toy duckie on the rubiks cube',
                'gold_code': '''
                put_first_on_second("toy duckie", "rubiks cube")
                update_wm("Put the toy duckie on the rubiks cube.")
                '''
            },
        ]
    },
    {
        'init_state': '''
        # state = {
        #     "items": ("rubiks cube", "toy duckie", "toy wheel", "yellow block"),
        #     "covers": ("red cup", "green cup", "blue cup", "black cup"),
        # }
        ''',
        'init_simple_state': '''
        # items = ("rubiks cube", "toy duckie", "toy wheel", "yellow block")
        # covers = ("red cup", "green cup", "blue cup", "black cup")
        ''',
        'episode': [
            {
                'user_query': 'put the yellow block on the rubiks cube',
                'gold_code': '''
                put_first_on_second("yellow block", "rubiks cube")
                update_wm("Put the yellow block on the rubiks cube.")
                '''
            },
            {
                'user_query': 'put the rubiks cube on the yellow block',
                'gold_code': '''
                put_first_on_second("yellow block", "empty space")
                update_wm("Put the yellow block on the empty space.")
                put_first_on_second("rubiks cube", "yellow block")
                update_wm("Put the rubiks cube on the yellow block.")
                '''
            },
            {
                'user_query': 'put the blue cup on the yellow block',
                'gold_code': '''
                put_first_on_second("rubiks cube", "empty space")
                update_wm("Put the rubiks cube on the empty space.")
                put_first_on_second("blue cup", "yellow block")
                update_wm("Put the blue cup on the yellow block.")
                '''
            },
            {
                'user_query': 'put the black cup on the toy duckie',
                'gold_code': '''
                put_first_on_second("black cup", "toy duckie")
                update_wm("Put the black cup on the toy duckie.")
                '''
            },
            {
                'user_query': 'put the green cup on the toy duckie',
                'gold_code': '''
                put_first_on_second("black cup", "empty space")
                update_wm("Put the black cup on the empty space.")
                put_first_on_second("green cup", "toy duckie")
                update_wm("Put the green cup on the toy duckie.")
                '''
            },
        ]
    },
    {
        'init_state': '''
        # state = {
        #     "items": ("rubiks cube", "toy duckie", "toy wheel", "yellow block"),
        #     "covers": ("red cup", "green cup", "blue cup", "black cup"),
        # }
        ''',
        'init_simple_state': '''
        # items = ("rubiks cube", "toy duckie", "toy wheel", "yellow block")
        # covers = ("red cup", "green cup", "blue cup", "black cup")
        ''',
        'episode': [
            {
                'user_query': 'put the black cup on the toy wheel',
                'gold_code': '''
                put_first_on_second("black cup", "toy wheel")
                update_wm("Put the black cup on the toy wheel.")
                '''
            },
            {
                'user_query': 'put the black cup on the rubiks cube',
                'gold_code': '''
                put_first_on_second("black cup", "rubiks cube")
                update_wm("Put the black cup on the rubiks cube.")
                '''
            },
            {
                'user_query': 'put the blue cup on the rubiks cube',
                'gold_code': '''
                put_first_on_second("black cup", "empty space")
                update_wm("Put the black cup on the empty space.")
                put_first_on_second("blue cup", "rubiks cube")
                update_wm("Put the blue cup on the rubiks cube.")
                '''
            },
            {
                'user_query': 'put the yellow block on the toy duckie',
                'gold_code': '''
                put_first_on_second("yellow block", "toy duckie")
                update_wm("Put the yellow block on the toy duckie.")
                '''
            },
            {
                'user_query': 'put the black cup on the rubiks cube',
                'gold_code': '''
                put_first_on_second("blue cup", "empty space")
                update_wm("Put the blue cup on the empty space.")
                put_first_on_second("black cup", "rubiks cube")
                update_wm("Put the black cup on the rubiks cube.")
                '''
            },
        ]
    },
    {
        'init_state': '''
        # state = {
        #     "items": ("rubiks cube", "toy duckie", "toy wheel", "yellow block"),
        #     "covers": ("red cup", "green cup", "blue cup", "black cup"),
        # }
        ''',
        'init_simple_state': '''
        # items = ("rubiks cube", "toy duckie", "toy wheel", "yellow block")
        # covers = ("red cup", "green cup", "blue cup", "black cup")
        ''',
        'episode': [
            {
                'user_query': 'put the black cup on the toy duckie',
                'gold_code': '''
                put_first_on_second("black cup", "toy duckie")
                update_wm("Put the black cup on the toy duckie.")
                '''
            },
            {
                'user_query': 'put the red cup on the rubiks cube',
                'gold_code': '''
                put_first_on_second("red cup", "rubiks cube")
                update_wm("Put the red cup on the rubiks cube.")
                '''
            },
            {
                'user_query': 'put the red cup on the toy duckie',
                'gold_code': '''
                put_first_on_second("black cup", "empty space")
                update_wm("Put the black cup on the empty space.")
                put_first_on_second("red cup", "toy duckie")
                update_wm("Put the red cup on the toy duckie.")
                '''
            },
            {
                'user_query': 'put the toy wheel on the yellow block',
                'gold_code': '''
                put_first_on_second("toy wheel", "yellow block")
                update_wm("Put the toy wheel on the yellow block.")
                '''
            },
            {
                'user_query': 'put the blue cup on the yellow block',
                'gold_code': '''
                put_first_on_second("toy wheel", "empty space")
                update_wm("Put the toy wheel on the empty space.")
                put_first_on_second("blue cup", "yellow block")
                update_wm("Put the blue cup on the yellow block.")
                '''
            },
        ]
    },
    {
        'init_state': '''
        # state = {
        #     "items": ("rubiks cube", "toy duckie", "toy wheel", "yellow block"),
        #     "covers": ("red cup", "green cup", "blue cup", "black cup"),
        # }
        ''',
        'init_simple_state': '''
        # items = ("rubiks cube", "toy duckie", "toy wheel", "yellow block")
        # covers = ("red cup", "green cup", "blue cup", "black cup")
        ''',
        'episode': [
            {
                'user_query': 'put the red cup on the toy duckie',
                'gold_code': '''
                put_first_on_second("red cup", "toy duckie")
                update_wm("Put the red cup on the toy duckie.")
                '''
            },
            {
                'user_query': 'put the red cup on the yellow block',
                'gold_code': '''
                put_first_on_second("red cup", "yellow block")
                update_wm("Put the red cup on the yellow block.")
                '''
            },
            {
                'user_query': 'put the red cup on the toy duckie',
                'gold_code': '''
                put_first_on_second("red cup", "toy duckie")
                update_wm("Put the red cup on the toy duckie.")
                '''
            },
            {
                'user_query': 'put the toy wheel on the yellow block',
                'gold_code': '''
                put_first_on_second("toy wheel", "yellow block")
                update_wm("Put the toy wheel on the yellow block.")
                '''
            },
            {
                'user_query': 'put the red cup on the toy wheel',
                'gold_code': '''
                put_first_on_second("toy wheel", "empty space")
                update_wm("Put the toy wheel on the empty space.")
                put_first_on_second("red cup", "toy wheel")
                update_wm("Put the red cup on the toy wheel.")
                '''
            },
        ]
    },
    {
        'init_state': '''
        # state = {
        #     "items": ("rubiks cube", "toy duckie", "toy wheel", "yellow block"),
        #     "covers": ("red cup", "green cup", "blue cup", "black cup"),
        # }
        ''',
        'init_simple_state': '''
        # items = ("rubiks cube", "toy duckie", "toy wheel", "yellow block")
        # covers = ("red cup", "green cup", "blue cup", "black cup")
        ''',
        'episode': [
            {
                'user_query': 'put the blue cup on the yellow block',
                'gold_code': '''
                put_first_on_second("blue cup", "yellow block")
                update_wm("Put the blue cup on the yellow block.")
                '''
            },
            {
                'user_query': 'put the red cup on the rubiks cube',
                'gold_code': '''
                put_first_on_second("red cup", "rubiks cube")
                update_wm("Put the red cup on the rubiks cube.")
                '''
            },
            {
                'user_query': 'put the green cup on the yellow block',
                'gold_code': '''
                put_first_on_second("blue cup", "empty space")
                update_wm("Put the blue cup on the empty space.")
                put_first_on_second("green cup", "yellow block")
                update_wm("Put the green cup on the yellow block.")
                '''
            },
            {
                'user_query': 'put the blue cup on the yellow block',
                'gold_code': '''
                put_first_on_second("green cup", "empty space")
                update_wm("Put the green cup on the empty space.")
                put_first_on_second("blue cup", "yellow block")
                update_wm("Put the blue cup on the yellow block.")
                '''
            },
            {
                'user_query': 'put the black cup on the toy wheel',
                'gold_code': '''
                put_first_on_second("black cup", "toy wheel")
                update_wm("Put the black cup on the toy wheel.")
                '''
            },
        ]
    },
    {
        'init_state': '''
        # state = {
        #     "items": ("rubiks cube", "toy duckie", "toy wheel", "yellow block"),
        #     "covers": ("red cup", "green cup", "blue cup", "black cup"),
        # }
        ''',
        'init_simple_state': '''
        # items = ("rubiks cube", "toy duckie", "toy wheel", "yellow block")
        # covers = ("red cup", "green cup", "blue cup", "black cup")
        ''',
        'episode': [
            {
                'user_query': 'put the black cup on the rubiks cube',
                'gold_code': '''
                put_first_on_second("black cup", "rubiks cube")
                update_wm("Put the black cup on the rubiks cube.")
                '''
            },
            {
                'user_query': 'put the rubiks cube on the toy wheel',
                'gold_code': '''
                put_first_on_second("black cup", "empty space")
                update_wm("Put the black cup on the empty space.")
                put_first_on_second("rubiks cube", "toy wheel")
                update_wm("Put the rubiks cube on the toy wheel.")
                '''
            },
            {
                'user_query': 'put the black cup on the rubiks cube',
                'gold_code': '''
                put_first_on_second("rubiks cube", "empty space")
                update_wm("Put the rubiks cube on the empty space.")
                put_first_on_second("black cup", "rubiks cube")
                update_wm("Put the black cup on the rubiks cube.")
                '''
            },
            {
                'user_query': 'put the black cup on the yellow block',
                'gold_code': '''
                put_first_on_second("black cup", "yellow block")
                update_wm("Put the black cup on the yellow block.")
                '''
            },
            {
                'user_query': 'put the blue cup on the toy wheel',
                'gold_code': '''
                put_first_on_second("blue cup", "toy wheel")
                update_wm("Put the blue cup on the toy wheel.")
                '''
            },
        ]
    },
    {
        'init_state': '''
        # state = {
        #     "items": ("rubiks cube", "toy duckie", "toy wheel", "yellow block"),
        #     "covers": ("red cup", "green cup", "blue cup", "black cup"),
        # }
        ''',
        'init_simple_state': '''
        # items = ("rubiks cube", "toy duckie", "toy wheel", "yellow block")
        # covers = ("red cup", "green cup", "blue cup", "black cup")
        ''',
        'episode': [
            {
                'user_query': 'put the yellow block on the toy wheel',
                'gold_code': '''
                put_first_on_second("yellow block", "toy wheel")
                update_wm("Put the yellow block on the toy wheel.")
                '''
            },
            {
                'user_query': 'put the green cup on the rubiks cube',
                'gold_code': '''
                put_first_on_second("green cup", "rubiks cube")
                update_wm("Put the green cup on the rubiks cube.")
                '''
            },
            {
                'user_query': 'put the red cup on the toy wheel',
                'gold_code': '''
                put_first_on_second("yellow block", "empty space")
                update_wm("Put the yellow block on the empty space.")
                put_first_on_second("red cup", "toy wheel")
                update_wm("Put the red cup on the toy wheel.")
                '''
            },
            {
                'user_query': 'put the toy wheel on the yellow block',
                'gold_code': '''
                put_first_on_second("red cup", "empty space")
                update_wm("Put the red cup on the empty space.")
                put_first_on_second("toy wheel", "yellow block")
                update_wm("Put the toy wheel on the yellow block.")
                '''
            },
            {
                'user_query': 'put the blue cup on the toy wheel',
                'gold_code': '''
                put_first_on_second("toy wheel", "empty space")
                update_wm("Put the toy wheel on the empty space.")
                put_first_on_second("blue cup", "toy wheel")
                update_wm("Put the blue cup on the toy wheel.")
                '''
            },
        ]
    },
    {
        'init_state': '''
        # state = {
        #     "items": ("rubiks cube", "toy duckie", "toy wheel", "yellow block"),
        #     "covers": ("red cup", "green cup", "blue cup", "black cup"),
        # }
        ''',
        'init_simple_state': '''
        # items = ("rubiks cube", "toy duckie", "toy wheel", "yellow block")
        # covers = ("red cup", "green cup", "blue cup", "black cup")
        ''',
        'episode': [
            {
                'user_query': 'put the black cup on the rubiks cube',
                'gold_code': '''
                put_first_on_second("black cup", "rubiks cube")
                update_wm("Put the black cup on the rubiks cube.")
                '''
            },
            {
                'user_query': 'put the blue cup on the rubiks cube',
                'gold_code': '''
                put_first_on_second("black cup", "empty space")
                update_wm("Put the black cup on the empty space.")
                put_first_on_second("blue cup", "rubiks cube")
                update_wm("Put the blue cup on the rubiks cube.")
                '''
            },
            {
                'user_query': 'put the black cup on the toy wheel',
                'gold_code': '''
                put_first_on_second("black cup", "toy wheel")
                update_wm("Put the black cup on the toy wheel.")
                '''
            },
            {
                'user_query': 'put the red cup on the rubiks cube',
                'gold_code': '''
                put_first_on_second("blue cup", "empty space")
                update_wm("Put the blue cup on the empty space.")
                put_first_on_second("red cup", "rubiks cube")
                update_wm("Put the red cup on the rubiks cube.")
                '''
            },
            {
                'user_query': 'put the blue cup on the toy wheel',
                'gold_code': '''
                put_first_on_second("black cup", "empty space")
                update_wm("Put the black cup on the empty space.")
                put_first_on_second("blue cup", "toy wheel")
                update_wm("Put the blue cup on the toy wheel.")
                '''
            },
        ]
    },
]

items = ("rubiks cube", "toy duckie", "toy wheel", "yellow block")
covers = ("red cup", "green cup", "blue cup", "black cup")

if __name__ == '__main__':
    rng = np.random.default_rng(0)
    print('[')
    for i_episode in range(20):
        last_pick = last_place = None
        print(f'# Episode {i_episode+1}')
        # print('========================')
        print('[')
        for j_step in range(5):
            pick = rng.choice(items if rng.random() < 0.3 else covers)
            while True:
                place = rng.choice(items)
                if place != pick and (pick != last_pick or place != last_place):
                    break
            # print(f"'user_query': 'put the {pick} on the {place}',")
            print(f"'put the {pick} on the {place}',")
            last_pick = pick
            last_place = place
        print('],')
    print(']')
    
