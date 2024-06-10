#!/usr/bin/env python3

task_description = '''
In the following, the robot performs a sequence of pick and place.
Remember that only objects the robot can interact are those in the "objects" list.
Aside from the built-in python functions and statements, the robot can only run the following functions:
{list_of_functions}
Each code is carefully designed by professionals.
'''

# NOTE:
# - Let's avoid picking a block that is under another block
# - --> Always pick the top block (thus "trivial" stacking)
# - Let's try to create a scenario that vision module won't easily handle
#   - "what's in the silver bowl" when nothing is stacked can be easily solved if we have a vision model
#   - We prefer to show cases that only our model can solve the task

eval_episode1 = {
    "init_state": '''
    # state = {
    #     "objects": ["green block", "orange block", "white block", "black block", "golden bowl", "silver bowl"],
    #     "relations": [],
    #     “green block": {},
    #     “orange block": {},
    #     “white block": {},
    #     “black block": {},
    #     “golden bowl”: {},
    #     "silver bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["green block", "orange block", "white block", "black block", "golden bowl", "silver bowl"],
    ''',
    "episode": [
        {
            "user_query": "Put the green block on the orange block",
            # orange block is under green block
            "gold_code": '''put_first_on_second("green block", "orange block")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "place the black block in the golden bowl",
            # orange block is under green block
            # golden bowl contains black block
            "gold_code": '''put_first_on_second("black block", "golden bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the white block in the silver bowl",
            # orange block is under green block
            # golden bowl contains black block
            # silver bowl contains white block
            "gold_code": '''put_first_on_second("white block", "silver bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "place the block in the golden bowl on the green block",
            # orange block is under green block is under black block
            # silver bowl contains white block
            "gold_code": '''put_first_on_second("black block", "green block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "what is the color of the block right above the orange block",
            # silver bowl contains white block, black block
            # golden bowl contains orange block
            "gold_code": '''say("green block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "is the white block in a higher position than the black block",
            "gold_code": '''say("no")''',
            "gold_next_state": '''''',
        },
    ]
}

eval_episode2 = {
    "init_state": '''
    # state = {
    #     "objects": ["green block", "orange block", "white block", "black block", "golden bowl", "silver bowl"],
    #     "relations": [],
    #     “green block": {},
    #     “orange block": {},
    #     “white block": {},
    #     “black block": {},
    #     “golden bowl”: {},
    #     "silver bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["green block", "orange block", "white block", "black block", "golden bowl", "silver bowl"],
    ''',
    "episode": [
        {
            "user_query": "put the white block in the golden bowl",
            # golden bowl contains white block
            "gold_code": '''put_first_on_second("white block", "golden bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "put the black block on the green block",
            # black block is under green block
            # golden bowl contains white block
            "gold_code": '''put_first_on_second("black block", "green block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the orange block in the empty bowl",
            # black block is under green block
            # golden bowl contains white block
            # silver bowl contains orange block
            "gold_code": '''put_first_on_second("orange block", "silver bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the block in the golden bowl on the block in the silver bowl",
            # black block is under green block
            # orange block is under white block
            # silver bowl contains white block, orange block
            "gold_code": '''put_first_on_second("white block", "orange block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "is the white block in a bowl",
            # black block is under green block
            # orange block is under white block
            # silver bowl contains white block, orange block
            "gold_code": '''say("yes")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "what is under the green block",
            "gold_code": '''say("black block")''',
            "gold_next_state": '''''',
        },
    ]
}

eval_episode3 = {
    "init_state": '''
    # state = {
    #     "objects": ["green block", "blue block", "red block", "black block", "golden bowl", "silver bowl"],
    #     "relations": [],
    #     “green block": {},
    #     “blue block": {},
    #     “red block": {},
    #     “black block": {},
    #     “golden bowl”: {},
    #     "silver bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["green block", "blue block", "red block", "black block", "golden bowl", "silver bowl"],
    ''',
    "episode": [
        {
            "user_query": "put the red block in the silver bowl",
            # silver bowl contains red block
            "gold_code": '''put_first_on_second("red block", "silver bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "place the black block in the golden bowl",
            # silver bowl contains red block
            # golden bowl contains black block
            "gold_code": '''put_first_on_second("black block", "golden bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "Put the blue block on the green block",
            # silver bowl contains red block
            # golden bowl contains black block
            # green block is under blue block
            "gold_code": '''put_first_on_second("blue block", "green block")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "place the block in the silver bowl on the blue block",
            # green block is under blue block is under red block
            # golden bowl contains black block
            "gold_code": '''put_first_on_second("red block", "blue block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "what is the color of the block right above the blue block",
            # green block is under blue block is under red block
            # golden bowl contains black block
            "gold_code": '''say("red)''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "is the red block in a higher position than the black block",
            "gold_code": '''say("yes")''',
            "gold_next_state": '''''',
        },
    ]
}

eval_episode4 = {
    "init_state": '''
    # state = {
    #     "objects": ["purple block", "blue block", "red block", "black block", "golden bowl", "bronze bowl"],
    #     "relations": [],
    #     “purple block": {},
    #     “blue block": {},
    #     “red block": {},
    #     “black block": {},
    #     “golden bowl”: {},
    #     "bronze bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["purple block", "blue block", "red block", "black block", "golden bowl", "bronze bowl"],
    ''',
    "episode": [
        {
            "user_query": "place the black block in the golden bowl",
            # golden bowl contains black block
            "gold_code": '''put_first_on_second("black block", "golden bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "Put the blue block on the purple block",
            # golden bowl contains black block
            # purple block is under blue block
            "gold_code": '''put_first_on_second("blue block", "purple block")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "put the red block in the bronze bowl",
            # golden bowl contains black block
            # purple block is under blue block
            # bronze bowl contains red block
            "gold_code": '''put_first_on_second("red block", "bronze bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "place the block in the bronze bowl on the blue block",
            # purple block is under blue block is under red block
            # golden bowl contains black block
            "gold_code": '''put_first_on_second("red block", "blue block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "what is the color of the block right above the purple block",
            # purple block is under blue block is under red block
            # golden bowl contains black block
            "gold_code": '''say("blue")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "is the purple block in a higher position than the black block",
            "gold_code": '''say("no (black block is in the golden bowl, purple block is on the table)")''',
            "gold_next_state": '''''',
        },
    ]
}

eval_episode5 = {
    "init_state": '''
    # state = {
    #     "objects": ["green block", "blue block", "red block", "black block", "golden bowl", "silver bowl"],
    #     "relations": [],
    #     “green block": {},
    #     “blue block": {},
    #     “red block": {},
    #     “black block": {},
    #     “golden bowl”: {},
    #     "silver bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["green block", "blue block", "red block", "black block", "golden bowl", "silver bowl"],
    ''',
    "episode": [
        {
            "user_query": "Put the blue block on the green block",
            # green block is under blue block
            "gold_code": '''put_first_on_second("blue block", "green block")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "place the black block in the golden bowl",
            # green block is under blue block
            # golden bowl contains black block
            "gold_code": '''put_first_on_second("black block", "golden bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the red block in the silver bowl",
            # green block is under blue block
            # golden bowl contains black block
            # silver bowl contains red block
            "gold_code": '''put_first_on_second("red block", "silver bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "place the block in the silver bowl on the blue block",
            # green block is under blue block is under red block
            # golden bowl contains black block
            "gold_code": '''put_first_on_second("red block", "blue block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "is the red block in a higher position than the green block",
            # green block is under blue block is under red block
            # golden bowl contains black block
            "gold_code": '''say("yes")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "is the red block in a higher position than the blue block",
            "gold_code": '''say("yes")''',
            "gold_next_state": '''''',
        },
    ]
}

eval_episode6 = {
    "init_state": '''
    # state = {
    #     "objects": ["brown block", "blue block", "red block", "white block", "golden bowl", "silver bowl"],
    #     "relations": [],
    #     “brown block": {},
    #     “blue block": {},
    #     “red block": {},
    #     “white block": {},
    #     “golden bowl”: {},
    #     "silver bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["brown block", "blue block", "red block", "white block", "golden bowl", "silver bowl"],
    ''',
    "episode": [
        {
            "user_query": "place the white block in the golden bowl",
            # silver bowl contains red block
            # golden bowl contains white block
            "gold_code": '''put_first_on_second("white block", "golden bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the red block in the silver bowl",
            # silver bowl contains red block
            "gold_code": '''put_first_on_second("red block", "silver bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "Put the blue block on the brown block",
            # silver bowl contains red block
            # golden bowl contains white block
            # brown block is under blue block
            "gold_code": '''put_first_on_second("blue block", "brown bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "place the block in the silver bowl on the blue block",
            # brown block is under blue block is under red block
            # golden bowl contains white block
            "gold_code": '''put_first_on_second("red block", "blue block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "what is the color of the block right beneath the blue block",
            # brown block is under blue block is under red block
            # golden bowl contains white block
            "gold_code": '''say("brown")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "is the white block in a higher position than the blue block",
            "gold_code": '''say("no")''',
            "gold_next_state": '''''',
        },
    ]
}

eval_episode7 = {
    "init_state": '''
    # state = {
    #     "objects": ["brown block", "blue block", "red block", "white block", "golden bowl", "silver bowl"],
    #     "relations": [],
    #     “brown block": {},
    #     “blue block": {},
    #     “red block": {},
    #     “white block": {},
    #     “golden bowl”: {},
    #     "silver bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["brown block", "blue block", "red block", "white block", "golden bowl", "silver bowl"],
    ''',
    "episode": [
        {
            "user_query": "place the white block in the golden bowl",
            # silver bowl contains red block
            # golden bowl contains white block
            "gold_code": '''put_first_on_second("white block", "golden bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the red block in the silver bowl",
            # silver bowl contains red block
            "gold_code": '''put_first_on_second("red block", "silver bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "Put the blue block on the brown block",
            # silver bowl contains red block
            # golden bowl contains white block
            # brown block is under blue block
            "gold_code": '''put_first_on_second("blue block", "brown block")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "place the block in the silver bowl on the blue block",
            # brown block is under blue block is under red block
            # golden bowl contains white block
            "gold_code": '''put_first_on_second("red block", "blue block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "what is the color of the block right beneath the red block",
            # brown block is under blue block is under red block
            # golden bowl contains white block
            "gold_code": '''say("blue")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "which block is in the highest position",
            "gold_code": '''say("red block")''',
            "gold_next_state": '''''',
        },
    ]
}

eval_episode8 = {
    "init_state": '''
    # state = {
    #     "objects": ["green block", "orange block", "white block", " cyan block", "golden bowl", "silver bowl"],
    #     "relations": [],
    #     “green block": {},
    #     “orange block": {},
    #     “white block": {},
    #     “ cyan block": {},
    #     “golden bowl”: {},
    #     "silver bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["green block", "orange block", "white block", " cyan block", "golden bowl", "silver bowl"],
    ''',
    "episode": [
        {
            "user_query": "put the white block in the golden bowl",
            # golden bowl contains white block
            "gold_code": '''put_first_on_second("white block", "golden bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "put the cyan block on the green block",
            # green block is under cyan block
            # golden bowl contains white block
            "gold_code": '''put_first_on_second("cyan block", "green block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the orange block in the empty bowl",
            # green block is under cyan block
            # golden bowl contains white block
            # silver bowl contains orange block
            "gold_code": '''put_first_on_second("orange block", "silver bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the block in the golden bowl on the block in the silver bowl",
            # cyan block is under green block
            # orange block is under white block
            # silver bowl contains white block, orange block
            "gold_code": '''put_first_on_second("white block", "orange block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "is the white block in a higher position than the cyan block",
            # cyan block is under green block
            # orange block is under white block
            # silver bowl contains white block, orange block
            "gold_code": '''say("yes")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "what is above the cyan block",
            "gold_code": '''say("green block")''',
            "gold_next_state": '''''',
        },
    ]
}

eval_episode9 = {
    "init_state": '''
    # state = {
    #     "objects": ["green block", "orange block", "white block", " cyan block", "golden bowl", "red bowl"],
    #     "relations": [],
    #     “green block": {},
    #     “orange block": {},
    #     “white block": {},
    #     “ cyan block": {},
    #     “golden bowl”: {},
    #     "red bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["green block", "orange block", "white block", " cyan block", "golden bowl", "red bowl"],
    ''',
    "episode": [
        {
            "user_query": "put the white block in the golden bowl",
            # golden bowl contains white block
            "gold_code": '''put_first_on_second("white block", "golden bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "put the cyan block on the green block",
            # green block is under cyan block
            # golden bowl contains white block
            "gold_code": '''put_first_on_second("cyan block", "green block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the orange block in the empty bowl",
            # cyan block is under green block
            # golden bowl contains white block
            # red bowl contains orange block
            "gold_code": '''put_first_on_second("orange block", "red bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the block in the golden bowl on the block in the red bowl",
            # green block is under cyan block
            # orange block is under white block
            # red bowl contains white block, orange block
            "gold_code": '''put_first_on_second("white block", "orange block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "is the green block in a higher position than the white block",
            # cyan block is under green block
            # orange block is under white block
            # red bowl contains white block, orange block
            "gold_code": '''say("no")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "is the green block right above the orange block",
            "gold_code": '''say("no")''',
            "gold_next_state": '''''',
        },
    ]
}

eval_episode10 = {
    "init_state": '''
    # state = {
    #     "objects": ["red block", "blue block", "white block", "purple block", "golden bowl", "silver bowl"],
    #     "relations": [],
    #     “red block": {},
    #     “blue block": {},
    #     “white block": {},
    #     “purple block": {},
    #     “golden bowl”: {},
    #     "silver bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["red block", "blue block", "white block", "purple block", "golden bowl", "silver bowl"],
    ''',
    "episode": [
        {
            "user_query": "put the white block in the golden bowl",
            # golden bowl contains white block
            "gold_code": '''put_first_on_second("white block", "golden bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "put the purple block on the white block",
            # white block is under purple block
            # golden bowl contains white block, purple block
            "gold_code": '''put_first_on_second("purple block", "white block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the blue block in the empty bowl",
            # white block is under purple block
            # golden bowl contains white block, purple block
            # silver bowl contains blue block
            "gold_code": '''put_first_on_second("blue block", "silver bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the red block on the blue block",
            # white block is under purple block
            # blue block is under red block
            # golden bowl contains white block, purple block
            # silver bowl contains blue block, red block
            "gold_code": '''put_first_on_second("red block", "blue block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "is the white block in a higher position than the purple block",
            # white block is under purple block
            # blue block is under red block
            # golden bowl contains white block, purple block
            # silver bowl contains blue block, red block
            "gold_code": '''say("no")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "what is in the golden bowl",
            "gold_code": '''say("white block", "purple block")''',
            "gold_next_state": '''''',
        },
    ]
}

eval_episode11 = {
    "init_state": '''
    # state = {
    #     "objects": ["green block", "orange block", "white block", "black block", "bronze bowl", "plastic bowl"],
    #     "relations": [],
    #     “green block": {},
    #     “orange block": {},
    #     “white block": {},
    #     “black block": {},
    #     “bronze bowl”: {},
    #     "plastic bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["green block", "orange block", "white block", "black block", "bronze bowl", "plastic bowl"],
    ''',
    "episode": [
        {
            "user_query": "put the white block in the bronze bowl",
            # bronze bowl contains white block
            "gold_code": '''put_first_on_second("white block", "bronze bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "put the black block on the white block",
            # white block is under black block
            # bronze bowl contains white block, black block
            "gold_code": '''put_first_on_second("black block", "white block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the orange block in the empty bowl",
            # white block is under black block
            # bronze bowl contains white block, black block
            # plastic bowl contains orange block
            "gold_code": '''put_first_on_second("orange block", "plastic bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the green block on the orange block",
            # white block is under black block
            # orange block is under green block
            # bronze bowl contains white block, black block
            # plastic bowl contains orange block, green block
            "gold_code": '''put_first_on_second("green block", "orange block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "what is in the plastic bowl",
            "gold_code": '''say("orange block", "green block")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "is the white block in a higher position than the orange block",
            # white block is under black block
            # orange block is under green block
            # bronze bowl contains white block, black block
            # plastic bowl contains orange block, green block
            "gold_code": '''say("no")''',
            "gold_next_state": ''' ''',
        },
    ]
}

eval_episode11 = {
    "init_state": '''
    # state = {
    #     "objects": ["green block", "orange block", "white block", "black block", "bronze bowl", "plastic bowl"],
    #     "relations": [],
    #     “green block": {},
    #     “orange block": {},
    #     “white block": {},
    #     “black block": {},
    #     “bronze bowl”: {},
    #     "plastic bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["green block", "orange block", "white block", "black block", "bronze bowl", "plastic bowl"],
    ''',
    "episode": [
        {
            "user_query": "put the white block in the bronze bowl",
            # bronze bowl contains white block
            "gold_code": '''put_first_on_second("white block", "bronze bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "put the black block on the white block",
            # white block is under black block
            # bronze bowl contains white block, black block
            "gold_code": '''put_first_on_second("black block", "white block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the orange block in the empty bowl",
            # white block is under black block
            # bronze bowl contains white block, black block
            # plastic bowl contains orange block
            "gold_code": '''put_first_on_second("orange block", "plastic bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the green block on the orange block",
            # white block is under black block
            # orange block is under green block
            # bronze bowl contains white block, black block
            # plastic bowl contains orange block, green block
            "gold_code": '''put_first_on_second("green block", "orange block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "what is in the plastic bowl",
            "gold_code": '''say("orange block", "green block")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "is the orange block in a bowl",
            # white block is under black block
            # orange block is under green block
            # bronze bowl contains white block, black block
            # plastic bowl contains orange block, green block
            "gold_code": '''say("yes")''',
            "gold_next_state": ''' ''',
        },
    ]
}

eval_episode12 = {
    "init_state": '''
    # state = {
    #     "objects": ["green block", "orange block", "white block", "black block", "bronze bowl", "plastic bowl"],
    #     "relations": [],
    #     “green block": {},
    #     “orange block": {},
    #     “white block": {},
    #     “black block": {},
    #     “bronze bowl”: {},
    #     "plastic bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["green block", "orange block", "white block", "black block", "bronze bowl", "plastic bowl"],
    ''',
    "episode": [
        {
            "user_query": "put the white block in the bronze bowl",
            # bronze bowl contains white block
            "gold_code": '''put_first_on_second("white block", "bronze bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "put the black block on the white block",
            # white block is under black block
            # bronze bowl contains white block, black block
            "gold_code": '''put_first_on_second("black block", "white block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the orange block in the empty bowl",
            # white block is under black block
            # bronze bowl contains white block, black block
            # plastic bowl contains orange block
            "gold_code": '''put_first_on_second("orange block", "plastic bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the green block on the orange block",
            # white block is under black block
            # orange block is under green block
            # bronze bowl contains white block, black block
            # plastic bowl contains orange block, green block
            "gold_code": '''put_first_on_second("green block", "orange block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "are there any blocks that are not in a bowl",
            "gold_code": '''say("no")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "how many blocks are there in the plastic bowl",
            # white block is under black block
            # orange block is under green block
            # bronze bowl contains white block, black block
            # plastic bowl contains orange block, green block
            "gold_code": '''say("there are two blocks in the plastic bowl")''',
            "gold_next_state": ''' ''',
        },
    ]
}

eval_episode13 = {
    "init_state": '''
    # state = {
    #     "objects": ["brown block", "yellow block", "red block", "green block", "golden bowl", "silver bowl"],
    #     "relations": [],
    #     “brown block": {},
    #     “yellow block": {},
    #     “red block": {},
    #     “green block": {},
    #     “golden bowl”: {},
    #     "silver bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["brown block", "yellow block", "red block", "green block", "golden bowl", "silver bowl"],
    ''',
    "episode": [
        {
            "user_query": "place the green block in the golden bowl",
            # silver bowl contains red block
            # golden bowl contains green block
            "gold_code": '''put_first_on_second("green block", "golden bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the red block in the silver bowl",
            # silver bowl contains red block
            "gold_code": '''put_first_on_second("red block", "silver bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "Put the yellow block on the brown block",
            # silver bowl contains red block
            # golden bowl contains green block
            # brown block is under yellow block
            "gold_code": '''put_first_on_second("yellow block", "brown block")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "place the block in the silver bowl on the yellow block",
            # brown block is under yellow block is under red block
            # golden bowl contains green block
            "gold_code": '''put_first_on_second("red block", "yellow block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "what color is the block in a bowl",
            # brown block is under yellow block is under red block
            # golden bowl contains green block
            "gold_code": '''say("green block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "how many blocks are not in the bowls",
            "gold_code": '''say("three blocks are not in the bowls")''',
            "gold_next_state": '''''',
        },
    ]
}

eval_episode14 = {
    "init_state": '''
    # state = {
    #     "objects": ["brown block", "yellow block", "red block", "green block", "golden bowl", "silver bowl"],
    #     "relations": [],
    #     “brown block": {},
    #     “yellow block": {},
    #     “red block": {},
    #     “green block": {},
    #     “golden bowl”: {},
    #     "silver bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["brown block", "yellow block", "red block", "green block", "golden bowl", "silver bowl"],
    ''',
    "episode": [
        {
            "user_query": "place the green block in the golden bowl",
            # silver bowl contains red block
            # golden bowl contains green block
            "gold_code": '''put_first_on_second("green block", "golden bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the red block in the silver bowl",
            # silver bowl contains red block
            "gold_code": '''put_first_on_second("red block", "silver bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "Put the yellow block on the brown block",
            # silver bowl contains red block
            # golden bowl contains green block
            # brown block is under yellow block
            "gold_code": '''put_first_on_second("yellow block", "brown block")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "place the block in the silver bowl on the yellow block",
            # brown block is under yellow block is under red block
            # golden bowl contains green block
            "gold_code": '''put_first_on_second("red block", "yellow block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "how many blocks are in positions higher than the brown block",
            "gold_code": '''say("two blocks are in positions higher than the brown block")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "which blocks (if there's any) are in positions higher than the brown block",
            # brown block is under yellow block is under red block
            # golden bowl contains green block
            "gold_code": '''say("yellow block", "red block")''',
            "gold_next_state": ''' ''',
        },
    ]
}

eval_episode15 = {
    "init_state": '''
    # state = {
    #     "objects": ["red block", "orange block", "white block", "gray block", "orange bowl", "plastic bowl"],
    #     "relations": [],
    #     “red block": {},
    #     “orange block": {},
    #     “white block": {},
    #     “gray block": {},
    #     “orange bowl”: {},
    #     "plastic bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["red block", "orange block", "white block", "gray block", "orange bowl", "plastic bowl"],
    ''',
    "episode": [
        {
            "user_query": "put the white block in the orange bowl",
            # orange bowl contains white block
            "gold_code": '''put_first_on_second("white block", "orange bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "put the gray block on the white block",
            # white block is under gray block
            # orange bowl contains white block, gray block
            "gold_code": '''put_first_on_second("gray block", "white block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the orange block in the empty bowl",
            # white block is under gray block
            # orange bowl contains white block, gray block
            # plastic bowl contains orange block
            "gold_code": '''put_first_on_second("orange block", "plastic bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the red block on the orange block",
            # white block is under gray block
            # orange block is under red block
            # orange bowl contains white block, gray block
            # plastic bowl contains orange block, red block
            "gold_code": '''put_first_on_second("red block", "orange block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "how many blocks are in positions lower than the gray block",
            "gold_code": '''say("two blocks")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "how many blocks (if there is any) are in positions higher than the gray block",
            # white block is under gray block
            # orange block is under red blockgit s
            # orange bowl contains white block, gray block
            # plastic bowl contains orange block, red block
            "gold_code": '''say("no blocks are in positions higher than the gray block")''',
            "gold_next_state": ''' ''',
        },
    ]
}

eval_episode16 = {
    "init_state": '''
    # state = {
    #     "objects": ["red block", "orange block", "white block", "gray block", "yellow block", "orange bowl", "plastic bowl"],
    #     "relations": [],
    #     “red block": {},  
    #     “orange block": {},
    #     “white block": {},
    #     “gray block": {},
    #     "yellow block": {},
    #     “orange bowl”: {},
    #     "plastic bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["red block", "orange block", "white block", "gray block", "yellow block", "orange bowl", "plastic bowl"],
    ''',
    "episode": [
        {
            "user_query": "put the white block in the orange bowl",
            # orange bowl contains white block
            "gold_code": '''put_first_on_second("white block", "orange bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "put the white block on the table",
            "gold_code": '''put_first_on_second("white block", "table")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "put the gray block on the white block",
            # white block is under gray block
            "gold_code": '''put_first_on_second("gray block", "white block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the orange block in the plastic bowl",
            # white block is under gray block
            # plastic bowl contains orange block
            "gold_code": '''put_first_on_second("orange block", "plastic bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the yellow block in the empty bowl",
            # white block is under gray block
            # plastic bowl contains orange block
            # orange bowl contains yellow block
            "gold_code": '''put_first_on_second("yellow block", "orange bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the red block on the orange block",
            # white block is under gray block
            # orange block is under red block
            # plastic bowl contains orange block, red block
            # orange bowl contains yellow block
            "gold_code": '''put_first_on_second("red block", "orange block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "is orange block placed in the plastic bowl",
            "gold_code": '''say("yes")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "is the white block placed in a bowl",
            # white block is under gray block
            # orange block is under red block
            # plastic bowl contains orange block, red block
            # orange bowl contains yellow block
            "gold_code": '''say("no")''',
            "gold_next_state": ''' ''',
        },
    ]
}

eval_episode17 = {
    "init_state": '''
    # state = {
    #     "objects": ["green block", "bronze block", "black block", "gray block", "yellow block", "bronze bowl", "plastic bowl"],
    #     "relations": [],
    #     “green block": {},  
    #     “bronze block": {},
    #     “black block": {},
    #     “gray block": {},
    #     "yellow block": {},
    #     “bronze bowl”: {},
    #     "plastic bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["green block", "bronze block", "black block", "gray block", "yellow block", "bronze bowl", "plastic bowl"],
    ''',
    "episode": [
        {
            "user_query": "put the black block in the bronze bowl",
            # bronze bowl contains black block
            "gold_code": '''put_first_on_second("black block", "bronze bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "put the black block on the table",
            "gold_code": '''put_first_on_second("black block", "table")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "put the gray block on the black block",
            # black block is under gray block
            "gold_code": '''put_first_on_second("gray block", "black block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the bronze block in the plastic bowl",
            # black block is under gray block
            # plastic bowl contains bronze block
            "gold_code": '''put_first_on_second("bronze block", "plastic bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the yellow block in the empty bowl",
            # black block is under gray block
            # plastic bowl contains bronze block
            # bronze bowl contains yellow block
            "gold_code": '''put_first_on_second("yellow block", "bronze bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the green block on the bronze block",
            # black block is under gray block
            # bronze block is under green block
            # plastic bowl contains bronze block, green block
            # bronze bowl contains yellow block
            "gold_code": '''put_first_on_second("green block", "bronze block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "what is under the green block",
            "gold_code": '''say("bronze block")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "how many blocks are in a position higher than the black block",
            # black block is under gray block
            # bronze block is under green block
            # plastic bowl contains bronze block, green block
            # bronze bowl contains yellow block
            "gold_code": '''say("there are two blocks")''',
            "gold_next_state": ''' ''',
        },
    ]
}

eval_episode18 = {
    "init_state": '''
    # state = {
    #     "objects": ["green block", "bronze block", "black block", "gray block", "yellow block", "bronze bowl", "plastic bowl"],
    #     "relations": [],
    #     “green block": {},  
    #     “bronze block": {},
    #     “black block": {},
    #     “gray block": {},
    #     "yellow block": {},
    #     “bronze bowl”: {},
    #     "plastic bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["green block", "bronze block", "black block", "gray block", "yellow block", "bronze bowl", "plastic bowl"],
    ''',
    "episode": [
        {
            "user_query": "put the black block in the bronze bowl",
            # bronze bowl contains black block
            "gold_code": '''put_first_on_second("black block", "bronze bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "put the black block on the table",
            "gold_code": '''put_first_on_second("black block", "table")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "put the gray block on the black block",
            # black block is under gray block
            "gold_code": '''put_first_on_second("gray block", "black block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the bronze block in the plastic bowl",
            # black block is under gray block
            # plastic bowl contains bronze block
            "gold_code": '''put_first_on_second("bronze block", "plastic bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the yellow block in the empty bowl",
            # black block is under gray block
            # plastic bowl contains bronze block
            # bronze bowl contains yellow block
            "gold_code": '''put_first_on_second("yellow block", "bronze bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the green block on the bronze block",
            # black block is under gray block
            # bronze block is under green block
            # plastic bowl contains bronze block, green block
            # bronze bowl contains yellow block
            "gold_code": '''put_first_on_second("green block", "bronze block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "how many blocks are in a position lower than the gray block",
            # black block is under gray block
            # bronze block is under green block
            # plastic bowl contains bronze block, green block
            # bronze bowl contains yellow block
            "gold_code": '''say("there are three blocks")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "is bronze block in the bronze bowl",
            "gold_code": '''say("no")''',
            "gold_next_state": '''''',
        },
    ]
}

eval_episode19 = {
    "init_state": '''
    # state = {
    #     "objects": ["white block", "silver block", "black block", "gray block", "yellow block", "silver bowl", "golden bowl"],
    #     "relations": [],
    #     “white block": {},  
    #     “silver block": {},
    #     “black block": {},
    #     “gray block": {},
    #     "yellow block": {},
    #     “silver bowl”: {},
    #     "golden bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["white block", "silver block", "black block", "gray block", "yellow block", "silver bowl", "golden bowl"],
    ''',
    "episode": [
        {
            "user_query": "put the black block in the silver bowl",
            # silver bowl contains black block
            "gold_code": '''put_first_on_second("black block", "silver bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "put the black block on the table",
            "gold_code": '''put_first_on_second("black block", "table")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "put the gray block on the black block",
            # black block is under gray block
            "gold_code": '''put_first_on_second("gray block", "black block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the silver block in the golden bowl",
            # black block is under gray block
            # golden bowl contains silver block
            "gold_code": '''put_first_on_second("silver block", "golden bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the yellow block in the empty bowl",
            # black block is under gray block
            # golden bowl contains silver block
            # silver bowl contains yellow block
            "gold_code": '''put_first_on_second("yellow block", "silver bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the white block on the silver block",
            # black block is under gray block
            # silver block is under white block
            # golden bowl contains silver block, white block
            # silver bowl contains yellow block
            "gold_code": '''put_first_on_second("white block", "silver block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the yellow block on the white block",
            # black block is under gray block
            # silver block is under white block is under yellow block
            # golden bowl contains silver block, white block, yellow block
            "gold_code": '''put_first_on_second("yellow block", "white block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "which block is at the bottom of the stack in the golden bowl",
            # black block is under gray block
            # silver block is under white block
            # golden bowl contains silver block, white block
            # silver bowl contains yellow block
            "gold_code": '''say("silver block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "which block is under the gray block",
            "gold_code": '''say("black block")''',
            "gold_next_state": '''''',
        },
    ]
}

eval_episode20 = {
    "init_state": '''
    # state = {
    #     "objects": ["white block", "silver block", "black block", "gray block", "yellow block", "silver bowl", "golden bowl"],
    #     "relations": [],
    #     “white block": {},
    #     “silver block": {},
    #     “black block": {},
    #     “gray block": {},
    #     "yellow block": {},
    #     “silver bowl”: {},
    #     "golden bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["white block", "silver block", "black block", "gray block", "yellow block", "silver bowl", "golden bowl"],
    ''',
    "episode": [
        {
            "user_query": "put the black block in the silver bowl",
            # silver bowl contains black block
            "gold_code": '''put_first_on_second("black block", "silver bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "put the black block on the table",
            "gold_code": '''put_first_on_second("black block", "table")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "put the gray block on the black block",
            # black block is under gray block
            "gold_code": '''put_first_on_second("gray block", "black block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the silver block in the golden bowl",
            # black block is under gray block
            # golden bowl contains silver block
            "gold_code": '''put_first_on_second("silver block", "golden bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the yellow block in the empty bowl",
            # black block is under gray block
            # golden bowl contains silver block
            # silver bowl contains yellow block
            "gold_code": '''put_first_on_second("yellow block", "silver bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the white block on the silver block",
            # black block is under gray block
            # silver block is under white block
            # golden bowl contains silver block, white block
            # silver bowl contains yellow block
            "gold_code": '''put_first_on_second("white block", "silver block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "put the yellow block on the white block",
            # black block is under gray block
            # silver block is under white block is under yellow block
            # golden bowl contains silver block, white block, yellow block
            "gold_code": '''put_first_on_second("yellow block", "white block")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "is the black block in the silver bowl",
            "gold_code": '''say("no")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "which block is in the middle of the stack in the golden bowl",
            # black block is under gray block
            # silver block is under white block is under yellow block
            # golden bowl contains silver block, white block, yellow blocku
            "gold_code": '''say("white block")''',
            "gold_next_state": ''' ''',
        },
    ]
}

eval_episodes = [eval_episode1, eval_episode2, eval_episode3, eval_episode4, eval_episode5, eval_episode6, eval_episode7, eval_episode8, eval_episode9, eval_episode10, eval_episode11, eval_episode12, eval_episode13, eval_episode14, eval_episode15, eval_episode16, eval_episode17, eval_episode18, eval_episode19, eval_episode20]
