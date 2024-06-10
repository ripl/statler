#!/usr/bin/env python3

eval_episode = {
    "init_state": '''
    # state = {
    #     "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "teal block", "brown block", "gray block", "yellow block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"], 
    #     "relations": [], 
    #     "disinfector": {"contains": []}, 
    #     "green block": {}, 
    #     "white block": {}, 
    #     "black block": {}, 
    #     "blue block": {}, 
    #     "pink block": {}, 
    #     "red block": {}, 
    #     "teal block": {}, 
    #     "brown block": {}, 
    #     "gray block": {}, 
    #     "yellow block": {}, 
    #     "purple block": {}, 
    #     "cyan block": {}, 
    #     "rust bowl": {}, 
    #     "magenta bowl": {}, 
    #     "tan bowl": {}, 
    #     "lavender bowl": {}
    # }
    ''',
    "init_simple_state": '''
    objects = ["green block", "white block", "black block", "blue block", "pink block", "red block", "teal block", "brown block", "gray block", "yellow block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
    ''', 
    "episode": [
        {"user_query": '''the blue block and the green block are clean.''', 
        "gold_code": '''update_wm("the blue block and the green block are clean.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "teal block", "brown block", "gray block", "yellow block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "blue block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the blue block and the green block in the disinfector''', 
        "gold_code": '''
        put_first_on_second("blue block", "disinfector")
        put_first_on_second("green block", "disinfector")
        update_wm("Put the blue block and the green block in the disinfector. the blue block and the green block become clean.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "teal block", "brown block", "gray block", "yellow block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": ["blue block", "green block"]},
            #    "blue block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": "Woops, somebody was moving the blue block and the green block and dropped them on some dirty region on the table",
        "gold_code": '''

        update_wm("The blue block is placed on the table, and becomes dirty.")
        update_wm("The green block is placed on the table, and becomes dirty.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "teal block", "brown block", "gray block", "yellow block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "blue block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''the red block is clean.''', 
        "gold_code": '''update_wm("the red block is clean.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "teal block", "brown block", "gray block", "yellow block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "blue block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            #    "red block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the blue block in the tan bowl''', 
        "gold_code": '''
        put_first_on_second("blue block", "tan bowl")
        update_wm("Put the blue block in the tan bowl.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "teal block", "brown block", "gray block", "yellow block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "blue block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            #    "red block": {"is": ["clean"]},
            #    "tan bowl": {"contains": ["blue block"]},
            # }
        '''},

        {"user_query": '''Put the blue block on the table.''', 
        "gold_code": '''
        put_first_on_second("blue block", "table")
        update_wm("Put the blue block on the table.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "teal block", "brown block", "gray block", "yellow block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "blue block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            #    "red block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the red block on the blue block''', 
        "gold_code": '''
        put_first_on_second("red block", "blue block")
        update_wm("Put the red block on the blue block. the red block becomes dirty.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "teal block", "brown block", "gray block", "yellow block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""red block" is on "blue block""]],
            #    "disinfector": {"contains": []},
            #    "blue block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            #    "red block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the red block and the blue block in the disinfector''', 
        "gold_code": '''
        put_first_on_second("red block", "disinfector")
        put_first_on_second("blue block", "disinfector")
        update_wm("Put the red block and the blue block in the disinfector. the red block and the blue block become clean.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "teal block", "brown block", "gray block", "yellow block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": ["red block", "blue block"]},
            #    "blue block": {"is": ["clean"]},
            #    "green block": {"is": ["dirty"]},
            #    "red block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the red block in the rust bowl''', 
        "gold_code": '''
        put_first_on_second("red block", "rust bowl")
        update_wm("Put the red block in the rust bowl.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "teal block", "brown block", "gray block", "yellow block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": ["blue block"]},
            #    "blue block": {"is": ["clean"]},
            #    "green block": {"is": ["dirty"]},
            #    "red block": {"is": ["clean"]},
            #    "rust bowl": {"contains": ["red block"]},
            # }
        '''},

        {"user_query": '''Put the red block on the table.''', 
        "gold_code": '''
        put_first_on_second("red block", "table")
        update_wm("Put the red block on the table.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "teal block", "brown block", "gray block", "yellow block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": ["blue block"]},
            #    "blue block": {"is": ["clean"]},
            #    "green block": {"is": ["dirty"]},
            #    "red block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the blue block on the red block''', 
        "gold_code": '''
        put_first_on_second("blue block", "red block")
        update_wm("Put the blue block on the red block.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "teal block", "brown block", "gray block", "yellow block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""blue block" is on "red block""]],
            #    "disinfector": {"contains": ["blue block"]},
            #    "blue block": {"is": ["clean"]},
            #    "green block": {"is": ["dirty"]},
            #    "red block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the green block on the blue block''', 
        "gold_code": '''
        put_first_on_second("green block", "blue block")
        update_wm("Put the green block on the blue block.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "teal block", "brown block", "gray block", "yellow block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""green block" is on ""blue block"""], [""blue block" is on "red block""]],
            #    "disinfector": {"contains": ["blue block"]},
            #    "blue block": {"is": ["clean"]},
            #    "green block": {"is": ["dirty"]},
            #    "red block": {"is": ["clean"]},
            #    ""blue block"": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the red block, the blue block, and the green block in the disinfector''', 
        "gold_code": '''
        put_first_on_second("red block", "disinfector")
        put_first_on_second("blue block", "disinfector")
        put_first_on_second("green block", "disinfector")
        update_wm("Put the red block, the blue block, and the green block in the disinfector. the red block, the blue block, and the green block become clean.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "teal block", "brown block", "gray block", "yellow block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": ["blue block", "red block", "blue block", "green block"]},
            #    "blue block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "red block": {"is": ["clean"]},
            #    ""blue block"": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put all the clean blocks on the table.''', 
        "gold_code": '''
        put_first_on_second("blue block", "table")
        put_first_on_second("green block", "table")
        put_first_on_second("red block", "table")
        update_wm("Put the blue block, the green block, and the red block on the relations.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "teal block", "brown block", "gray block", "yellow block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": ["blue block"]},
            #    "blue block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "red block": {"is": ["clean"]},
            #    ""blue block"": {"is": ["dirty"]},
            # }
        '''}
    ]
}

eval_episodes = [eval_episode]
    