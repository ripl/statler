#!/usr/bin/env python3

eval_episode = {
    "init_state": '''
    # state = {
    #     "objects": ["red block", "green block", "pink block", "blue block", "rust bowl", "magenta bowl", "tan bowl", "disinfector"], 
    #     "relations": [], 
    #     "disinfector": {"contains": []}, 
    #     "red block": {}, 
    #     "green block": {}, 
    #     "pink block": {}, 
    #     "blue block": {}, 
    #     "rust bowl": {}, 
    #     "magenta bowl": {}, 
    #     "tan bowl": {}
    # }
    ''',
    "init_simple_state": '''
    objects = ["red block", "green block", "pink block", "blue block", "rust bowl", "magenta bowl", "tan bowl", "disinfector"],
    ''', 
    "episode": [
        {"user_query": '''the red block and the green block are dirty.''', 
        "gold_code": '''update_wm("the red block and the green block are dirty.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["red block", "green block", "pink block", "blue block", "rust bowl", "magenta bowl", "tan bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "red block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the red block in the rust bowl''', 
        "gold_code": '''
        put_first_on_second("red block", "rust bowl")
        update_wm("Put the red block in the rust bowl.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["red block", "green block", "pink block", "blue block", "rust bowl", "magenta bowl", "tan bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "red block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            #    "rust bowl": {"contains": ["red block"]},
            # }
        '''},

        {"user_query": '''the pink block is clean.''', 
        "gold_code": '''update_wm("the pink block is clean.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["red block", "green block", "pink block", "blue block", "rust bowl", "magenta bowl", "tan bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "red block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            #    "rust bowl": {"contains": ["red block"]},
            #    "pink block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the pink block in the magenta bowl''', 
        "gold_code": '''
        put_first_on_second("pink block", "magenta bowl")
        update_wm("Put the pink block in the magenta bowl.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["red block", "green block", "pink block", "blue block", "rust bowl", "magenta bowl", "tan bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "red block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            #    "rust bowl": {"contains": ["red block"]},
            #    "pink block": {"is": ["clean"]},
            #    "magenta bowl": {"contains": ["pink block"]},
            # }
        '''},

        {"user_query": '''Put the pink block on the table.''', 
        "gold_code": '''
        put_first_on_second("pink block", "table")
        update_wm("Put the pink block on the table.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["red block", "green block", "pink block", "blue block", "rust bowl", "magenta bowl", "tan bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "red block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            #    "rust bowl": {"contains": ["red block"]},
            #    "pink block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the red block on the pink block''', 
        "gold_code": '''
        put_first_on_second("red block", "pink block")
        update_wm("Put the red block on the pink block. the pink block becomes dirty.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["red block", "green block", "pink block", "blue block", "rust bowl", "magenta bowl", "tan bowl", "disinfector"],
            #    "relations": [[""red block" is on "pink block""]],
            #    "disinfector": {"contains": []},
            #    "red block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            #    "pink block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''the blue block is clean.''', 
        "gold_code": '''update_wm("the blue block is clean.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["red block", "green block", "pink block", "blue block", "rust bowl", "magenta bowl", "tan bowl", "disinfector"],
            #    "relations": [[""red block" is on "pink block""]],
            #    "disinfector": {"contains": []},
            #    "red block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            #    "pink block": {"is": ["dirty"]},
            #    "blue block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the blue block on the red block''', 
        "gold_code": '''
        put_first_on_second("blue block", "red block")
        update_wm("Put the blue block on the red block. the blue block becomes dirty.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["red block", "green block", "pink block", "blue block", "rust bowl", "magenta bowl", "tan bowl", "disinfector"],
            #    "relations": [[""blue block" is on "red block" is on "pink block""]],
            #    "disinfector": {"contains": []},
            #    "red block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            #    "pink block": {"is": ["dirty"]},
            #    "blue block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put all the dirty blocks on the table.''', 
        "gold_code": '''
        put_first_on_second("red block", "table")
        put_first_on_second("green block", "table")
        put_first_on_second("pink block", "table")
        put_first_on_second("blue block", "table")
        update_wm("Put the red block, the green block, the pink block, and the blue block on the relations.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["red block", "green block", "pink block", "blue block", "rust bowl", "magenta bowl", "tan bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "red block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            #    "pink block": {"is": ["dirty"]},
            #    "blue block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the red block, the pink block, the blue block, and the red block in the disinfector''', 
        "gold_code": '''
        put_first_on_second("red block", "disinfector")
        put_first_on_second("pink block", "disinfector")
        put_first_on_second("blue block", "disinfector")
        put_first_on_second("red block", "disinfector")
        update_wm("Put the red block, the pink block, the blue block, and the red block in the disinfector. the red block, the pink block, the blue block, and the red block become clean.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["red block", "green block", "pink block", "blue block", "rust bowl", "magenta bowl", "tan bowl", "disinfector"],
            #    "disinfector": {"contains": ["pink block", "blue block", "red block"]},
            #    "red block": {"is": ["clean"]},
            #    "green block": {"is": ["dirty"]},
            #    "pink block": {"is": ["clean"]},
            #    "blue block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the green block in the tan bowl''', 
        "gold_code": '''
        put_first_on_second("green block", "tan bowl")
        update_wm("Put the green block in the tan bowl.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["red block", "green block", "pink block", "blue block", "rust bowl", "magenta bowl", "tan bowl", "disinfector"],
            #    "disinfector": {"contains": ["pink block", "blue block", "red block"]},
            #    "red block": {"is": ["clean"]},
            #    "green block": {"is": ["dirty"]},
            #    "pink block": {"is": ["clean"]},
            #    "blue block": {"is": ["clean"]},
            #    "tan bowl": {"contains": ["green block"]},
            # }
        '''},

        {"user_query": '''Put the green block on the table.''', 
        "gold_code": '''
        put_first_on_second("green block", "table")
        update_wm("Put the green block on the table.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["red block", "green block", "pink block", "blue block", "rust bowl", "magenta bowl", "tan bowl", "disinfector"],
            #    "disinfector": {"contains": ["pink block", "blue block", "red block"]},
            #    "red block": {"is": ["clean"]},
            #    "green block": {"is": ["dirty"]},
            #    "pink block": {"is": ["clean"]},
            #    "blue block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the red block on the green block''', 
        "gold_code": '''
        put_first_on_second("red block", "green block")
        update_wm("Put the red block on the green block. the red block becomes dirty.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["red block", "green block", "pink block", "blue block", "rust bowl", "magenta bowl", "tan bowl", "disinfector"],
            #    "relations": [[""red block" is on "green block""]],
            #    "disinfector": {"contains": ["pink block", "blue block"]},
            #    "red block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            #    "pink block": {"is": ["clean"]},
            #    "blue block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the pink block on the red block''', 
        "gold_code": '''
        put_first_on_second("pink block", "red block")
        update_wm("Put the pink block on the red block. the pink block becomes dirty.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["red block", "green block", "pink block", "blue block", "rust bowl", "magenta bowl", "tan bowl", "disinfector"],
            #    "relations": [[""pink block" is on "red block" is on "green block""]],
            #    "disinfector": {"contains": ["pink block", "blue block"]},
            #    "red block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            #    "pink block": {"is": ["dirty"]},
            #    "blue block": {"is": ["clean"]},
            # }
        '''}
    ]
}

eval_episodes = [eval_episode]
    