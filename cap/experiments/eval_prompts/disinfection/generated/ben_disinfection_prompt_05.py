#!/usr/bin/env python3

eval_episode = {
    "init_state": '''
    # state = {
    #     "objects": ["green block", "white block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "disinfector"], 
    #     "relations": [], 
    #     "disinfector": {"contains": []}, 
    #     "green block": {}, 
    #     "white block": {}, 
    #     "black block": {}, 
    #     "purple block": {}, 
    #     "cyan block": {}, 
    #     "rust bowl": {}, 
    #     "magenta bowl": {}
    # }
    ''',
    "init_simple_state": '''
    objects = ["green block", "white block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "disinfector"],
    ''', 
    "episode": [
        {"user_query": '''the green block is dirty.''', 
        "gold_code": '''update_wm("the green block is dirty.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "green block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''the white block is dirty.''', 
        "gold_code": '''update_wm("the white block is dirty.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "green block": {"is": ["dirty"]},
            #    "white block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''the black block is dirty.''', 
        "gold_code": '''update_wm("the black block is dirty.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "green block": {"is": ["dirty"]},
            #    "white block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''the purple block is clean.''', 
        "gold_code": '''update_wm("the purple block is clean.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "green block": {"is": ["dirty"]},
            #    "white block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            #    "purple block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''the cyan block is clean.''', 
        "gold_code": '''update_wm("the cyan block is clean.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "green block": {"is": ["dirty"]},
            #    "white block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            #    "purple block": {"is": ["clean"]},
            #    "cyan block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the green block in the rust bowl''', 
        "gold_code": '''
        put_first_on_second("green block", "rust bowl")
        update_wm("Put the green block in the rust bowl.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "green block": {"is": ["dirty"]},
            #    "white block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            #    "purple block": {"is": ["clean"]},
            #    "cyan block": {"is": ["clean"]},
            #    "rust bowl": {"contains": ["green block"]},
            # }
        '''},

        {"user_query": '''Put the blue block in the magenta bowl''', 
        "gold_code": '''
        put_first_on_second("blue block", "magenta bowl")
        update_wm("Put the blue block in the magenta bowl.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "green block": {"is": ["dirty"]},
            #    "white block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            #    "purple block": {"is": ["clean"]},
            #    "cyan block": {"is": ["clean"]},
            #    "rust bowl": {"contains": ["green block"]},
            #    "magenta bowl": {"contains": ["blue block"]},
            # }
        '''},

        {"user_query": '''Put the green block on the table.''', 
        "gold_code": '''
        put_first_on_second("green block", "table")
        update_wm("Put the green block on the table.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "green block": {"is": ["dirty"]},
            #    "white block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            #    "purple block": {"is": ["clean"]},
            #    "cyan block": {"is": ["clean"]},
            #    "magenta bowl": {"contains": ["blue block"]},
            # }
        '''},

        {"user_query": '''Put the purple block on the table.''', 
        "gold_code": '''
        put_first_on_second("purple block", "table")
        update_wm("Put the purple block on the table.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "green block": {"is": ["dirty"]},
            #    "white block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            #    "purple block": {"is": ["clean"]},
            #    "cyan block": {"is": ["clean"]},
            #    "magenta bowl": {"contains": ["blue block"]},
            # }
        '''},

        {"user_query": '''Put the white block on the green block''', 
        "gold_code": '''
        put_first_on_second("white block", "green block")
        update_wm("Put the white block on the green block.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "disinfector"],
            #    "relations": [[""white block" is on "green block""]],
            #    "disinfector": {"contains": []},
            #    "green block": {"is": ["dirty"]},
            #    "white block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            #    "purple block": {"is": ["clean"]},
            #    "cyan block": {"is": ["clean"]},
            #    "magenta bowl": {"contains": ["blue block"]},
            # }
        '''},

        {"user_query": '''Put the cyan block on the white block''', 
        "gold_code": '''
        put_first_on_second("cyan block", "white block")
        update_wm("Put the cyan block on the white block. the cyan block becomes dirty.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "disinfector"],
            #    "relations": [[""cyan block" is on "white block" is on "green block""]],
            #    "disinfector": {"contains": []},
            #    "green block": {"is": ["dirty"]},
            #    "white block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            #    "purple block": {"is": ["clean"]},
            #    "cyan block": {"is": ["dirty"]},
            #    "magenta bowl": {"contains": ["blue block"]},
            # }
        '''},

        {"user_query": '''Put the black block on the purple block''', 
        "gold_code": '''
        put_first_on_second("black block", "purple block")
        update_wm("Put the black block on the purple block. the purple block becomes dirty.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "disinfector"],
            #    "relations": [[""cyan block" is on "white block" is on "green block""], [""black block" is on "purple block""]],
            #    "disinfector": {"contains": []},
            #    "green block": {"is": ["dirty"]},
            #    "white block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            #    "purple block": {"is": ["dirty"]},
            #    "cyan block": {"is": ["dirty"]},
            #    "magenta bowl": {"contains": ["blue block"]},
            # }
        '''},

        {"user_query": '''Put all the dirty blocks on the table.''', 
        "gold_code": '''
        put_first_on_second("green block", "table")
        put_first_on_second("white block", "table")
        put_first_on_second("black block", "table")
        put_first_on_second("purple block", "table")
        put_first_on_second("cyan block", "table")
        update_wm("Put the green block, the white block, the black block, the purple block, and the cyan block on the relations.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "green block": {"is": ["dirty"]},
            #    "white block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            #    "purple block": {"is": ["dirty"]},
            #    "cyan block": {"is": ["dirty"]},
            #    "magenta bowl": {"contains": ["blue block"]},
            # }
        '''}
    ]
}

eval_episodes = [eval_episode]
    