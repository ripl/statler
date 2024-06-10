#!/usr/bin/env python3

task_description = '''
In the following, the robot picks and places blocks with different weights.
A query will describe the relative weights of some of the blocks.
Aside from the built-in python functions and statements, the robot can only run the following functions:
{list_of_functions}
Each code is carefully designed by professionals to meet all of these requirements.
'''

eval_episode1 = {
    "obj_name_to_weight": {"green block": 4.,
                           "white block": 4.,
                           "black block": 2.,
                           "orange block": 2.,},
    "init_state": '''
    # state = {
    #     "objects": ["green block", "orange block", "white block", "black block", "transparent bowl", "green bowl"],
    #     "relations": [],
    #     “green block": {},
    #     “orange block": {},
    #     “white block": {},
    #     “black block": {},
    #     “transparent bowl”: {},
    #     "green bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["green block", "orange block", "white block", "black block", "transparent bowl", "green bowl"],
    ''',
    "episode": [
        {
            "user_query": "The green block has the same weight as the white block",
            # weight: green block == white block
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The white block is twice the weight of the black block",
            # weight:
            # - green block == white block
            # - white block == black block x 2
            "gold_code": ''' ''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "The orange block is half the weight of the green block",
            # weight:
            # - green block == white block
            # - white block == black block x 2
            # - orange block == white block / 2 == black block
            "gold_code": ''' ''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "Put the orange block in the transparent bowl",
            "gold_code": '''put_first_on_second("orange block", "transparent bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "Put the blocks in the green bowl so that their total weight becomes identical to what is in the transparent bowl",
            "gold_code": '''put_first_on_second("black block", "green bowl")''',
            "gold_next_state": ''' ''',
        },
    ]
}

eval_episode2 = {
    "init_state": '''
    # state = {
    #     "objects": ["purple block", "bronze block", green block", "red block", "transparent bowl", "blue bowl"],
    #     "relations": [],
    #     “purple block": {},
    #     “bronze block": {},
    #     “green block": {},
    #     “red block": {},
    #     “transparent bowl”: {},
    #     “blue bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["purple block", "bronze block", green block", "red block", "transparent bowl", "blue bowl"],
    ''',
    "episode": [
        {
            "user_query": "The purple block is twice the weight of the green block",
            # weight:
            # - purple block == green block x 2
            "gold_code": ''' ''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The bronze block is half the weight of the red block",
            # weight:
            # - purple block == green block x 2
            # - bronze block x 2 == red block
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put the bronze block in the blue bowl",
            "gold_code": '''put_first_on_second("bronze block", "blue bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The red block has the same weight of the purple block",
            # weight:
            # - purple block == green block x 2
            # - bronze block x 2 == red block
            # - purple block == red block
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put the red block in the transparent bowl",
            "gold_code": '''put_first_on_second("red block", "transparent bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put blocks in the blue bowl so that their total weight becomes identical to what is in the transparent bowl",
            "gold_code": '''put_first_on_second("green block", "blue bowl")''',
            "gold_next_state": ''' ''',
        },
    ]
}

eval_episode3 = {
    "init_state": '''
    # state = {
    #     "objects": ["black block", "orange block", green block", "red block", "gray bowl", "blue bowl"],
    #     "relations": [],
    #     “black block": {},
    #     “orange block": {},
    #     “green block": {},
    #     “red block": {},
    #     “gray bowl”: {},
    #     “blue bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["black block", "orange block", green block", "red block", "gray bowl", "blue bowl"],
    ''',
    "episode": [
        {
            "user_query": "The black block is twice the weight of the green block",
            # weight:
            # - black block == green block x 2
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put the orange block in the gray bowl",
            "gold_code": '''put_first_on_second("orange block", "gray bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The red block is twice the weight of the orange block",
            # weight:
            # - black block == green block x 2
            # - orange block x 2 == red block
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The red block has the same weight of the black block",
            # weight:
            # - black block == green block x 2
            # - orange block x 2 == red block
            # - black block == red block
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put the red block in the gray bowl",
            "gold_code": '''put_first_on_second("red block", "gray bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put blocks in the blue bowl so that their total weight becomes identical to what is in the gray bowl",
            "gold_code": '''
            put_first_on_second("black block", "blue bowl")
            put_first_on_second("green block", "blue bowl")
            ''',
            "gold_next_state": ''' ''',
        },
    ]
}

eval_episode4 = {
    "init_state": '''
    # state = {
    #     "objects": ["transparent block", "orange block", blue block", "red block", "gray bowl", "yellow bowl"],
    #     "relations": [],
    #     “transparent block": {},
    #     “orange block": {},
    #     “blue block": {},
    #     “red block": {},
    #     “gray bowl”: {},
    #     “yellow bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["transparent block", "orange block", blue block", "red block", "gray bowl", "yellow bowl"],
    ''',
    "episode": [
        {
            "user_query": "The transparent block is twice the weight of the blue block",
            # weight:
            # - transparent block == blue block x 2
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put the orange block in the gray bowl",
            # weight:
            # - transparent block == blue block x 2
            # gray bowl: orange block
            "gold_code": '''put_first_on_second("orange block", "gray bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The red block is twice the weight of the orange block",
            # weight:
            # - transparent block == blue block x 2
            # - orange block x 2 == red block
            # gray bowl: orange block
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put the orange block in the yellow bowl",
            # weight:
            # - transparent block == blue block x 2
            # - orange block x 2 == red block
            # yellow bowl: orange block
            "gold_code": '''put_first_on_second("orange block", "yellow bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put the red block in the gray bowl",
            # weight:
            # - transparent block == blue block x 2
            # - orange block x 2 == red block
            # yellow bowl: orange block
            # gray bowl: red block
            "gold_code": '''put_first_on_second("red block", "gray bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The blue block has the same weight of the orange block",
            # weight:
            # - transparent block == blue block x 2
            # - orange block x 2 == red block
            # - blue block == orange block
            # yellow bowl: orange block
            # gray bowl: red block
            "gold_code": ''' ''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put blocks in the yellow bowl so that their total weight becomes identical to what is in the gray bowl",
            "gold_code": '''
            put_first_on_second("blue block", "yellow bowl")
            ''',
            "gold_next_state": '''''',
        },
    ]
}

eval_episode5 = {
    "init_state": '''
    # state = {
    #     "objects": ["transparent block", "orange block", green block", "red block", "gray bowl", "white bowl"],
    #     "relations": [],
    #     “transparent block": {},
    #     “orange block": {},
    #     “green block": {},
    #     “red block": {},
    #     “gray bowl”: {},
    #     “white bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["transparent block", "orange block", green block", "red block", "gray bowl", "white bowl", table"],
    ''',
    "episode": [
        {
            "user_query": "The transparent block is twice the weight of the green block",
            # weight:
            # - transparent block == green block x 2
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put the orange block in the gray bowl",
            "gold_code": '''put_first_on_second("orange block", "gray bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The red block is twice the weight of the orange block",
            # weight:
            # - transparent block == green block x 2
            # - orange block x 2 == red block
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put the orange block in the white bowl",
            "gold_code": '''put_first_on_second("orange block", "white bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put the red block in the gray bowl",
            "gold_code": '''put_first_on_second("red block", "gray bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put the transparent block in the gray bowl",
            "gold_code": '''put_first_on_second("transparent block", "gray bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The green block has the same weight of the orange block",
            # weight:
            # - transparent block == green block x 2
            # - orange block x 2 == red block
            # - green block == orange block
            "gold_code": ''' ''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put the green block in the white bowl",
            "gold_code": '''put_first_on_second("green block", "white bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Remove blocks from the gray bowl so that their total weight becomes identical to what is in the white bowl. The removed blocks should be put on the table",
            "gold_code": '''put_first_on_second("transparent block", "table")''',
            "gold_next_state": '''''',
        },
    ]
}

eval_episode6 = {
    "init_state": '''
    # state = {
    #     "objects" = ["silver block", "yellow block", green block", "red block", "gray bowl", "white bowl", table"],
    #     "relations": [],
    #     “silver block": {},
    #     “yellow block": {},
    #     “green block": {},
    #     “red block": {},
    #     “gray bowl”: {},
    #     “white bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["silver block", "yellow block", green block", "red block", "gray bowl", "white bowl", table"],
    ''',
    "episode": [
        {
            "user_query": "Put the yellow block in the gray bowl",
            "gold_code": '''put_first_on_second("yellow block", "gray bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The silver block is twice the weight of the green block",
            # weight:
            # - silver block == green block x 2
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The red block is twice the weight of the yellow block",
            # weight:
            # - silver block == green block x 2
            # - yellow block x 2 == red block
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put the yellow block in the white bowl",
            "gold_code": '''put_first_on_second("yellow block", "white bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put the red block in the gray bowl",
            "gold_code": '''put_first_on_second("red block", "gray bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The green block is twice the weight of the yellow block",
            # weight:
            # - silver block == green block x 2
            # - yellow block x 2 == red block
            # - green block == yellow block x 2
            "gold_code": ''' ''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put the green block in the white bowl",
            "gold_code": '''put_first_on_second("green block", "white bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Remove blocks from the white bowl so that their total weight becomes identical to what is in the gray bowl. The removed blocks should be put on the table",
            # This is wrong, the correct one should be put_first_on_second(yellow block, table) Huanyu
            "gold_code": '''put_first_on_second("green block", "table")''',
            "gold_next_state": '''''',
        },
    ]
}

eval_episode7 = {
    "init_state": '''
    # state = {
    #     "objects" = ["silver block", "yellow block", blue block", "red block", "black bowl", "white bowl", table"],
    #     "relations": [],
    #     “silver block": {},
    #     “yellow block": {},
    #     “blue block": {},
    #     “red block": {},
    #     “black bowl”: {},
    #     “white bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["silver block", "yellow block", blue block", "red block", "black bowl", "white bowl", table"],
    ''',
    "episode": [
        {
            "user_query": "The silver block is twice the weight of the blue block",
            # weight:
            # - silver block == blue block x 2
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The red block is twice the weight of the yellow block",
            # weight:
            # - silver block == blue block x 2
            # - yellow block x 2 == red block
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put the yellow block in the white bowl",
            "gold_code": '''put_first_on_second("yellow block", "white bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put the red block in the black bowl",
            "gold_code": '''put_first_on_second("red block", "black bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The blue block is half the weight of the yellow block",
            # weight:
            # - silver block == blue block x 2
            # - yellow block x 2 == red block
            # - blue block x 2 == yellow block
            "gold_code": ''' ''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put the blue block in the white bowl",
            "gold_code": '''put_first_on_second("blue block", "white bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put blocks in and remove blocks from the white bowl so that their total weight becomes identical to what is in the black bowl. The removed blocks should be put on the table",
            "gold_code": '''put_first_on_second("blue block", "table")
            put_first_on_second("silver block", "white bowl")
            ''',
            "gold_next_state": '''''',
        },
    ]
}

eval_episode8 = {
    "obj_name_to_weight": {"green block": 1.,
                           "red block": 6.,
                           "bronze block": 3.,
                           "silver block": 2,},
    "init_state": '''
    # state = {
    #     "objects" = ["silver block", "bronze block", "green block", "red block", "gray bowl", "purple bowl", "table"],
    #     "relations": [],
    #     “silver block": {},
    #     “bronze block": {},
    #     “green block": {},
    #     “red block": {},
    #     “gray bowl”: {},
    #     “purple bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["silver block", "bronze block", "green block", "red block", "gray bowl", "purple bowl", "table"],
    ''',
    "episode": [
        {
            "user_query": "Put the bronze block in the purple bowl",
            "gold_code": '''put_first_on_second("bronze block", "purple bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The silver block is twice the weight of the green block",
            # weight:
            # - silver block == green block x 2
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The red block is twice the weight of the bronze block",
            # weight:
            # - silver block == green block x 2
            # - bronze block x 2 == red block
            "gold_code": '''''',
            "gold_next_state": '''''',
        },

        {
            "user_query": "Put the red block in the gray bowl",
            "gold_code": '''put_first_on_second("red block", "gray bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The green block is one-thrid the weight of the bronze block",
            # weight:
            # - silver block == green block x 2
            # - bronze block x 2 == red block
            # - green block x 3 == bronze block
            "gold_code": ''' ''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put the green block in the purple bowl",
            "gold_code": '''put_first_on_second("green block", "purple bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put blocks in the purple bowl so that their total weight becomes identical to what is in the gray bowl",
            "gold_code": '''put_first_on_second("silver block", "purple bowl")
            ''',
            "gold_next_state": '''''',
        },
    ]
}

eval_episode9 = {
    "init_state": '''
    # state = {
    #     "objects" = ["rainbow block", "pink block", green block", "red block", "gray bowl", "white bowl", table"],
    #     "relations": [],
    #     “rainbow block": {},
    #     “pink block": {},
    #     “green block": {},
    #     “red block": {},
    #     “gray bowl”: {},
    #     “white bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["rainbow block", "pink block", green block", "red block", "gray bowl", "white bowl", table"],
    ''',
    "episode": [
        {
            "user_query": "Put the pink block in the white bowl",
            "gold_code": '''put_first_on_second("pink block", "white bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The rainbow block is four times the weight of the green block",
            # weight:
            # - rainbow block == green block x 4
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The red block is twice the weight of the pink block",
            # weight:
            # - rainbow block == green block x 4
            # - pink block x 2 == red block
            "gold_code": '''''',
            "gold_next_state": '''''',
        },

        {
            "user_query": "Put the rainbow block in the gray bowl",
            "gold_code": '''put_first_on_second("rainbow block", "gray bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The green block is one-thrid the weight of the pink block",
            # weight:
            # - rainbow block == green block x 4
            # - pink block x 2 == red block
            # - green block x 3 == pink block
            "gold_code": ''' ''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put blocks in the white bowl so that their total weight becomes identical to what is in the gray bowl",
            "gold_code": '''put_first_on_second("green block", "white bowl")
            ''',
            "gold_next_state": '''''',
        },
    ]
}

eval_episode10 = {
    "init_state": '''
    # state = {
    #     "objects" = ["silver block", "yellow block", green block", "pink block", "gray bowl", "red bowl", table"],
    #     "relations": [],
    #     “silver block": {},
    #     “yellow block": {},
    #     “green block": {},
    #     “pink block": {},
    #     “gray bowl”: {},
    #     “red bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["silver block", "yellow block", green block", "pink block", "gray bowl", "red bowl", table"],
    ''',
    "episode": [
        {
            "user_query": "The silver block is four times the weight of the green block",
            # weight:
            # - silver block == green block x 4
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The pink block is twice the weight of the yellow block",
            # weight:
            # - silver block == green block x 4
            # - yellow block x 2 == pink block
            "gold_code": '''''',
            "gold_next_state": '''''',
        },

        {
            "user_query": "Put the silver block in the gray bowl",
            "gold_code": '''put_first_on_second("silver block", "gray bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The green block is one-thrid the weight of the yellow block",
            # weight:
            # - silver block == green block x 4
            # - yellow block x 2 == pink block
            # - green block x 3 == yellow block
            "gold_code": ''' ''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put blocks in the red bowl so that their total weight becomes identical to what is in the gray bowl",
            "gold_code": '''put_first_on_second("green block", "red bowl"),
            put_first_on_second("yellow block", "red bowl")
            ''',
            "gold_next_state": '''''',
        },
    ]
}

eval_episode11 = {
    "init_state": '''
    # state = {
    #     "objects" = ["gray block", "yellow block", black block", "red block", "gray bowl", "white bowl", table"],
    #     "relations": [],
    #     “gray block": {},
    #     “yellow block": {},
    #     “black block": {},
    #     “red block": {},
    #     “gray bowl”: {},
    #     “white bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["gray block", "yellow block", black block", "red block", "gray bowl", "white bowl", table"],
    ''',
    "episode": [
        {
            "user_query": "The gray block has the same weight as the black block",
            # weight:
            # - gray block == black block
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put the gray block in the white bowl",
            "gold_code": '''put_first_on_second("gray block", "white bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The red block has the weight as the yellow block",
            # weight:
            # - gray block == black block
            # - red block == yellow block
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put the gray block in the gray bowl",
            "gold_code": '''put_first_on_second("gray block", "gray bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put the red block in the white bowl",
            "gold_code": '''put_first_on_second("red block", "white bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put blocks in both bowls so that the sums of the weights of blocks in each of the two bowls becomes identical",
            "gold_code": '''put_first_on_second("yellow block", "gray bowl"),
            put_first_on_second("black block", "white bowl")
            ''',
            "gold_next_state": '''''',
        },
    ]
}

eval_episode12 = {
    "init_state": '''
    # state = {
    #     "objects" = ["silver block", "yellow block", green block", "red block", "gray bowl", "gold block", "bronze block", white bowl", table"],
    #     "relations": [],
    #     “silver block": {},
    #     “yellow block": {},
    #     “green block": {},
    #     “red block": {},
    #     “gray bowl”: {},
    #     “white bowl": {},
    #     "gold block": {},
    #     "bronze block":{}
    # }
    ''',
    "init_simple_state": '''
    # objects = ["silver block", "yellow block", green block", "red block", "gray bowl", "gold block", "bronze block", white bowl", table"],
    ''',
    "episode": [
        {
            "user_query": "The silver block has the same weight as the green block",
            # weight:
            # - silver block == green block
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put the silver block in the white bowl",
            "gold_code": '''put_first_on_second("silver block", "white bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The red block has the weight as the yellow block",
            # weight:
            # - silver block == green block
            # - yellow block == red block
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put the silver block in the gray bowl",
            "gold_code": '''put_first_on_second("silver block", "gray bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The gold block is one-tenth the weight of the silver block",
            # weight:
            # - silver block == green block
            # - yellow block == red block
            # - gold block x 10 == silver block
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The bronze block is one-tenth the weight of the gold block",
            # weight:
            # - silver block == green block
            # - yellow block == red block
            # - gold block x 10 == silver block
            # - bronze block x 10 == gold block
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put the red block in the white bowl",
            "gold_code": '''put_first_on_second("red block", "white bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put blocks in both bowls so that the sums of the weights of blocks in two bowls becomes identical",
            "gold_code": '''put_first_on_second("yellow block", "gray bowl"),
            put_first_on_second("green block", "white bowl")
            ''',
            "gold_next_state": '''''',
        },
    ]
}

eval_episode13 = {
    "init_state": '''
    # state = {
    #     "objects" = ["silver block", "yellow block", green block", "red block", "gray bowl", "gold block", "bronze block", white bowl", table"],
    #     "relations": [],
    #     “silver block": {},
    #     “yellow block": {},
    #     “green block": {},
    #     “red block": {},
    #     “gray bowl”: {},
    #     “white bowl": {},
    #     "gold block": {},
    #     "bronze block":{}
    # }
    ''',
    "init_simple_state": '''
    # objects = ["silver block", "yellow block", green block", "red block", "gray bowl", "gold block", "bronze block", white bowl", table"],
    ''',
    "episode": [
        {
            "user_query": "The silver block has the same weight as the green block",
            # weight:
            # - silver block == green block
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The red block has the weight as the yellow block",
            # weight:
            # - silver block == green block
            # - yellow block == red block
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put the silver block in the white bowl",
            "gold_code": '''put_first_on_second("silver block", "white bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The gold block is one-tenth the weight of the silver block",
            # weight:
            # - silver block == green block
            # - yellow block == red block
            # - gold block x 10 == silver block
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The gold block is one-ninth the weight of the bronze block",
            # weight:
            # - silver block == green block
            # - yellow block == red block
            # - gold block x 10 == silver block
            # - bronze block == gold block x 9
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put blocks in the gray bowl so that their total weight becomes identical to what is in the white bowl",
            "gold_code": '''put_first_on_second("gold block", "gray bowl"),
            put_first_on_second("bronze block", "gray bowl")
            ''',
            "gold_next_state": '''''',
        },
    ]
}

eval_episode14 = {
    "init_state": '''
    # state = {
    #     "objects" = ["black block", "orange block", green block", "red block", "gray bowl", "blue bowl", table"],
    #     "relations": [],
    #     “black block": {},
    #     “orange block": {},
    #     “green block": {},
    #     “red block": {},
    #     “gray bowl”: {},
    #     “blue bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["black block", "orange block", green block", "red block", "gray bowl", "blue bowl", table"],
    ''',
    "episode": [
        {
            "user_query": "The weight of the black block is three times that of the green block.",
            # weight:
            # - black block == green block x 3
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The red block is twice the weight of the orange block",
            # weight:
            # - black block == green block x 3
            # - orange block x 2 == red block
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put the red block in the gray bowl",
            "gold_code": '''put_first_on_second("red block", "gray bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The red block has the same weight of the black block",
            # weight:
            # - black block == green block x 3
            # - orange block x 2 == red block
            # - black block == red block
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put blocks in the blue bowl so that their total weight becomes identical to what is in the gray bowl",
            "gold_code": '''
            put_first_on_second("black block", "blue bowl")
            ''',
            "gold_next_state": ''' ''',
        },
    ]
}

eval_episode15 = {
    "init_state": '''
    # state = {
    #     "objects" = ["black block", "orange block", green block", "red block", "gray bowl", "blue bowl", table"],
    #     "relations": [],
    #     “black block": {},
    #     “orange block": {},
    #     “green block": {},
    #     “red block": {},
    #     “gray bowl”: {},
    #     “blue bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["black block", "orange block", green block", "red block", "gray bowl", "blue bowl", table"],
    ''',
    "episode": [
        {
            "user_query": "Put the orange block in the gray bowl",
            "gold_code": '''put_first_on_second("orange block", "gray bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The weight of the black block is three times that of the green block.",
            # weight:
            # - black block == green block x 3
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The red block is twice the weight of the orange block",
            # weight:
            # - black block == green block x 3
            # - orange block x 2 == red block
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The red block has the same weight of the black block",
            # weight:
            # - black block == green block x 3
            # - orange block x 2 == red block
            # - black block == red block
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put a block in the blue bowl so that the total weight of blocks in the blue bowl is less than what is in the gray bowl",
            "gold_code": '''
            put_first_on_second("green block", "blue bowl")
            ''',
            "gold_next_state": ''' ''',
        },
    ]
}

eval_episode16 = {
    "obj_name_to_weight": {"green block": 2.,
                           "red block": 6.,
                           "black block": 6.,
                           "orange block": 3,},
    "init_state": '''
    # state = {
    #     "objects" = ["black block", "orange block", green block", "red block", "gray bowl", "blue bowl", "table"],
    #     "relations": [],
    #     “black block": {},
    #     “orange block": {},
    #     “green block": {},
    #     “red block": {},
    #     “gray bowl”: {},
    #     “blue bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["black block", "orange block", "green block", "red block", "gray bowl", "blue bowl", "table"],
    ''',
    "episode": [
        {
            "user_query": "Put the orange block in the gray bowl",
            "gold_code": '''put_first_on_second("orange block", "gray bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The weight of the black block is three times that of the green block.",
            # weight:
            # - black block == green block x 3
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put the red block in the gray bowl",
            "gold_code": '''put_first_on_second("red block", "gray bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The red block is twice the weight of the orange block",
            # weight:
            # - black block == green block x 3
            # - orange block x 2 == red block
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put the black block in the blue bowl",
            "gold_code": '''put_first_on_second("black block", "blue bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The red block has the same weight of the black block",
            # weight:
            # - black block == green block x 3
            # - orange block x 2 == red block
            # - black block == red block
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put a block in the blue bowl so that the total weight of blocks in the blue bowl is less than what is in the gray bowl",
            "gold_code": '''
            put_first_on_second("green block", "blue bowl")
            ''',
            "gold_next_state": ''' ''',
        },
    ]
}

eval_episode17 = {
    "obj_name_to_weight": {"green block": 2.,
                           "red block": 6.,
                           "black block": 6.,
                           "orange block": 3,},
    "init_state": '''
    # state = {
    #     "objects" = ["black block", "orange block", green block", "red block", "gray bowl", "blue bowl", table"],
    #     "relations": [],
    #     “black block": {},
    #     “orange block": {},
    #     “green block": {},
    #     “red block": {},
    #     “gray bowl”: {},
    #     “blue bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["black block", "orange block", "green block", "red block", "gray bowl", "blue bowl", "table"],
    ''',
    "episode": [
        {
            "user_query": "The weight of the black block is three times that of the green block.",
            # weight:
            # - black block == green block x 3
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put the green block in the gray bowl",
            "gold_code": '''put_first_on_second("green block", "gray bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put the red block in the gray bowl",
            "gold_code": '''put_first_on_second("red block", "gray bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The red block is twice the weight of the orange block",
            # weight:
            # - black block == green block x 3
            # - orange block x 2 == red block
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put the black block in the blue bowl",
            "gold_code": '''put_first_on_second("black block", "blue bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The red block has the same weight of the black block",
            # weight:
            # - black block == green block x 3
            # - orange block x 2 == red block
            # - black block == red block
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put a block in the blue bowl so that the total weight of blocks in the blue bowl is greater than what is in the gray bowl",
            "gold_code": '''
            put_first_on_second("orange block", "blue bowl")
            ''',
            "gold_next_state": ''' ''',
        },
    ]
}

eval_episode18 = {
    "init_state": '''
    # state = {
    #     "objects" = ["black block", "orange block", green block", "red block", "gray bowl", "blue bowl", table"],
    #     "relations": [],
    #     “black block": {},
    #     “orange block": {},
    #     “green block": {},
    #     “red block": {},
    #     “gray bowl”: {},
    #     “blue bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["black block", "orange block", green block", "red block", "gray bowl", "blue bowl", table"],
    ''',
    "episode": [
        {
            "user_query": "The weight of the black block is three times that of the green block.",
            # weight:
            # - black block == green block x 3
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put the green block in the gray bowl",
            "gold_code": '''put_first_on_second("green block", "gray bowl")''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The red block is twice the weight of the orange block",
            # weight:
            # - black block == green block x 3
            # - orange block x 2 == red block
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The red block has the same weight of the black block",
            # weight:
            # - black block == green block x 3
            # - orange block x 2 == red block
            # - black block == red block
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "Put a block in the blue bowl so that the total weight of blocks in the blue bowl is greater than what is in the gray bowl",
            "gold_code": '''
            put_first_on_second("orange block", "blue bowl")
            ''',
            "gold_next_state": ''' ''',
        },
    ]
}

eval_episode19 = {
    "init_state": '''
    # state = {
    #     "objects" = ["green block", "orange block", "white block", "black block", “gold block", "transparent bowl", "green bowl", "table"],
    #     "relations": [],
    #     “green block": {},
    #     “orange block": {},
    #     “white block": {},
    #     “black block": {},
    #     “gold block": {},
    #     “transparent bowl”: {},
    #     "green bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["green block", "orange block", "white block", "black block", “gold block", "transparent bowl", "green bowl", "table"],
    ''',
    "episode": [
        {
            "user_query": "The green block has the same weight as the white block",
            # weight: green block == white block
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The white block is twice the weight of the black block",
            # weight:
            # - green block == white block
            # - white block == black block x 2
            "gold_code": ''' ''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "The orange block is half the weight of the green block",
            # weight:
            # - green block == white block
            # - white block == black block x 2
            # - orange block == white block / 2 == black block
            "gold_code": ''' ''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "The gold block is ten times the weight of the green block",
            # weight:
            # - green block == white block
            # - white block == black block x 2
            # - orange block == white block / 2 == black block
            # - gold block == green block x 10
            "gold_code": ''' ''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "Put the gold block in the transparent bowl",
            "gold_code": '''put_first_on_second("gold block", "transparent bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "Put as much blocks as you can in the green bowl until their total weight becomes greater than what is in the transparent bowl",
            "gold_code": '''put_first_on_second("black block", "green bowl")
            put_first_on_second("white block", "green bowl"),
            put_first_on_second("green block", "green bowl"),
            put_first_on_second("orange block", "green bowl")
            ''',
            "gold_next_state": ''' ''',
        },
    ]
}

eval_episode20 = {
    "init_state": '''
    # state = {
    #     "objects" = ["green block", "orange block", "white block", "black block", “gold block", "transparent bowl", "green bowl", "table"],
    #     "relations": [],
    #     “green block": {},
    #     “orange block": {},
    #     “white block": {},
    #     “black block": {},
    #     “gold block": {},
    #     “transparent bowl”: {},
    #     "green bowl": {},
    # }
    ''',
    "init_simple_state": '''
    # objects = ["green block", "orange block", "white block", "black block", “gold block", "transparent bowl", "green bowl", "table"],
    ''',
    "episode": [
        {
            "user_query": "The green block has the same weight as the white block",
            # weight: green block == white block
            "gold_code": '''''',
            "gold_next_state": '''''',
        },
        {
            "user_query": "The white block is twice the weight of the black block",
            # weight:
            # - green block == white block
            # - white block == black block x 2
            "gold_code": ''' ''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "The orange block is half the weight of the green block",
            # weight:
            # - green block == white block
            # - white block == black block x 2
            # - orange block == white block / 2 == black block
            "gold_code": ''' ''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "The gold block is fours times the weight of the orange block",
            # weight:
            # - green block == white block
            # - white block == black block x 2
            # - orange block == white block / 2 == black block
            # - gold block == green block x 10
            "gold_code": ''' ''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "Put the gold block in the transparent bowl",
            "gold_code": '''put_first_on_second("gold block", "transparent bowl")''',
            "gold_next_state": ''' ''',
        },
        {
            "user_query": "Put as much blocks as you can in the green bowl until their total weight becomes greater than what is in the transparent bowl",
            # multiple answers are valid
            "gold_code": '''
            put_first_on_second("green block", "green bowl"),
            put_first_on_second("orange block", "green bowl"),
            put_first_on_second("black block", "green bowl")
            ''',
            "gold_next_state": ''' ''',
        },
    ]
}

eval_episodes = [eval_episode1, eval_episode2, eval_episode3, eval_episode4, eval_episode5, eval_episode6, eval_episode7, eval_episode8, eval_episode9, eval_episode10, eval_episode11, eval_episode12, eval_episode13, eval_episode14, eval_episode15, eval_episode16, eval_episode17, eval_episode18, eval_episode19, eval_episode20]

