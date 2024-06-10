#!/usr/bin/env python3

eval_episode = {
    "init_state": '''
    # state = {
    #     "objects": ["green block", "white block", "black block", "blue block", "pink block", "transparent bowl", "platinum bowl", "disinfector"], 
    #     "relations": [], 
    #     "disinfector": {"contains": []}, 
    #     "green block": {}, 
    #     "white block": {}, 
    #     "black block": {}, 
    #     "blue block": {}, 
    #     "pink block": {}, 
    #     "transparent bowl": {}, 
    #     "platinum bowl": {}
    # }
    ''',
    "init_simple_state": '''
    objects = ["green block", "white block", "black block", "blue block", "pink block", "transparent bowl", "platinum bowl", "disinfector"],
    ''', 
    "episode": [
        {"user_query": '''the green block is dirty.''', 
        "gold_code": '''update_wm("the green block is dirty.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "transparent bowl", "platinum bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "green block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the green block in the transparent bowl''', 
        "gold_code": '''
        put_first_on_second("green block", "transparent bowl")
        update_wm("Put the green block in the transparent bowl.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "transparent bowl", "platinum bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "green block": {"is": ["dirty"]},
            #    "transparent bowl": {"contains": ["green block"]},
            # }
        '''},

        {"user_query": '''the pink block and the blue block are clean.''', 
        "gold_code": '''update_wm("the pink block and the blue block are clean.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "transparent bowl", "platinum bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "green block": {"is": ["dirty"]},
            #    "transparent bowl": {"contains": ["green block"]},
            #    "pink block": {"is": ["clean"]},
            #    "blue block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the green block on the table.''', 
        "gold_code": '''
        put_first_on_second("green block", "table")
        update_wm("Put the green block on the table.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "transparent bowl", "platinum bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "green block": {"is": ["dirty"]},
            #    "pink block": {"is": ["clean"]},
            #    "blue block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the pink block on the green block''', 
        "gold_code": '''
        put_first_on_second("pink block", "green block")
        update_wm("Put the pink block on the green block. the pink block becomes dirty.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "transparent bowl", "platinum bowl", "disinfector"],
            #    "relations": [[""pink block" is on "green block""]],
            #    "disinfector": {"contains": []},
            #    "green block": {"is": ["dirty"]},
            #    "pink block": {"is": ["dirty"]},
            #    "blue block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the green block and the pink block in the disinfector''', 
        "gold_code": '''
        put_first_on_second("green block", "disinfector")
        put_first_on_second("pink block", "disinfector")
        update_wm("Put the green block and the pink block in the disinfector. the green block and the pink block become clean.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "transparent bowl", "platinum bowl", "disinfector"],
            #    "disinfector": {"contains": ["green block", "pink block"]},
            #    "green block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            #    "blue block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the pink block in the platinum bowl''', 
        "gold_code": '''
        put_first_on_second("pink block", "platinum bowl")
        update_wm("Put the pink block in the platinum bowl.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "transparent bowl", "platinum bowl", "disinfector"],
            #    "disinfector": {"contains": ["green block"]},
            #    "green block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            #    "blue block": {"is": ["clean"]},
            #    "platinum bowl": {"contains": ["pink block"]},
            # }
        '''},

        {"user_query": '''Put the pink block on the table.''', 
        "gold_code": '''
        put_first_on_second("pink block", "table")
        update_wm("Put the pink block on the table.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "transparent bowl", "platinum bowl", "disinfector"],
            #    "disinfector": {"contains": ["green block"]},
            #    "green block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            #    "blue block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the green block on the pink block''', 
        "gold_code": '''
        put_first_on_second("green block", "pink block")
        update_wm("Put the green block on the pink block.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "transparent bowl", "platinum bowl", "disinfector"],
            #    "relations": [[""green block" is on "pink block""]],
            #    "disinfector": {"contains": []},
            #    "green block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            #    "blue block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the blue block on the green block''', 
        "gold_code": '''
        put_first_on_second("blue block", "green block")
        update_wm("Put the blue block on the green block.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "transparent bowl", "platinum bowl", "disinfector"],
            #    "relations": [[""blue block" is on "green block" is on "pink block""]],
            #    "disinfector": {"contains": []},
            #    "green block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            #    "blue block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put all the clean blocks on the table.''', 
        "gold_code": '''
        put_first_on_second("green block", "table")
        put_first_on_second("pink block", "table")
        put_first_on_second("blue block", "table")
        update_wm("Put the green block, the pink block, and the blue block on the relations.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "transparent bowl", "platinum bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "green block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            #    "blue block": {"is": ["clean"]},
            # }
        '''}
    ]
}

eval_episodes = [eval_episode]
    