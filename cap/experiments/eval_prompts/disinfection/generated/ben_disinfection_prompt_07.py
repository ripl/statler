#!/usr/bin/env python3

eval_episode = {
    "init_state": '''
    # state = {
    #     "objects": ["blue block", "black block", "pink block", "teal block", "red block", "rust bowl", "tan bowl", "disinfector"], 
    #     "relations": [], 
    #     "disinfector": {"contains": []}, 
    #     "blue block": {}, 
    #     "black block": {}, 
    #     "pink block": {}, 
    #     "teal block": {}, 
    #     "red block": {}, 
    #     "rust bowl": {}, 
    #     "tan bowl": {}
    # }
    ''',
    "init_simple_state": '''
    objects = ["blue block", "black block", "pink block", "teal block", "red block", "rust bowl", "tan bowl", "disinfector"],
    ''', 
    "episode": [
        {"user_query": '''the blue block and the black block are clean.''', 
        "gold_code": '''update_wm("the blue block and the black block are clean.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["blue block", "black block", "pink block", "teal block", "red block", "rust bowl", "tan bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "blue block": {"is": ["clean"]},
            #    "black block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the black block in the rust bowl''', 
        "gold_code": '''
        put_first_on_second("black block", "rust bowl")
        update_wm("Put the black block in the rust bowl.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["blue block", "black block", "pink block", "teal block", "red block", "rust bowl", "tan bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "blue block": {"is": ["clean"]},
            #    "black block": {"is": ["clean"]},
            #    "rust bowl": {"contains": ["black block"]},
            # }
        '''},

        {"user_query": '''the pink block and the teal block are clean.''', 
        "gold_code": '''update_wm("the pink block and the teal block are clean.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["blue block", "black block", "pink block", "teal block", "red block", "rust bowl", "tan bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "blue block": {"is": ["clean"]},
            #    "black block": {"is": ["clean"]},
            #    "rust bowl": {"contains": ["black block"]},
            #    "pink block": {"is": ["clean"]},
            #    "teal block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the blue block and the black block in the disinfector''', 
        "gold_code": '''
        put_first_on_second("blue block", "disinfector")
        put_first_on_second("black block", "disinfector")
        update_wm("Put the blue block and the black block in the disinfector. the blue block and the black block become clean.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["blue block", "black block", "pink block", "teal block", "red block", "rust bowl", "tan bowl", "disinfector"],
            #    "disinfector": {"contains": ["blue block", "black block"]},
            #    "blue block": {"is": ["clean"]},
            #    "black block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            #    "teal block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''the red block is dirty.''', 
        "gold_code": '''update_wm("the red block is dirty.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["blue block", "black block", "pink block", "teal block", "red block", "rust bowl", "tan bowl", "disinfector"],
            #    "disinfector": {"contains": ["blue block", "black block"]},
            #    "blue block": {"is": ["clean"]},
            #    "black block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            #    "teal block": {"is": ["clean"]},
            #    "red block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the red block in the tan bowl''', 
        "gold_code": '''
        put_first_on_second("red block", "tan bowl")
        update_wm("Put the red block in the tan bowl.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["blue block", "black block", "pink block", "teal block", "red block", "rust bowl", "tan bowl", "disinfector"],
            #    "disinfector": {"contains": ["blue block", "black block"]},
            #    "blue block": {"is": ["clean"]},
            #    "black block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            #    "teal block": {"is": ["clean"]},
            #    "red block": {"is": ["dirty"]},
            #    "tan bowl": {"contains": ["red block"]},
            # }
        '''},

        {"user_query": '''Put the red block on the table.''', 
        "gold_code": '''
        put_first_on_second("red block", "table")
        update_wm("Put the red block on the table.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["blue block", "black block", "pink block", "teal block", "red block", "rust bowl", "tan bowl", "disinfector"],
            #    "disinfector": {"contains": ["blue block", "black block"]},
            #    "blue block": {"is": ["clean"]},
            #    "black block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            #    "teal block": {"is": ["clean"]},
            #    "red block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the black block on the red block''', 
        "gold_code": '''
        put_first_on_second("black block", "red block")
        update_wm("Put the black block on the red block. the black block becomes dirty.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["blue block", "black block", "pink block", "teal block", "red block", "rust bowl", "tan bowl", "disinfector"],
            #    "relations": [[""black block" is on "red block""]],
            #    "disinfector": {"contains": ["blue block"]},
            #    "blue block": {"is": ["clean"]},
            #    "black block": {"is": ["dirty"]},
            #    "pink block": {"is": ["clean"]},
            #    "teal block": {"is": ["clean"]},
            #    "red block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the blue block on the black block''', 
        "gold_code": '''
        put_first_on_second("blue block", "black block")
        update_wm("Put the blue block on the black block. the blue block becomes dirty.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["blue block", "black block", "pink block", "teal block", "red block", "rust bowl", "tan bowl", "disinfector"],
            #    "relations": [[""blue block" is on "black block" is on "red block""]],
            #    "disinfector": {"contains": []},
            #    "blue block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            #    "pink block": {"is": ["clean"]},
            #    "teal block": {"is": ["clean"]},
            #    "red block": {"is": ["dirty"]},
            # }
        '''},
        {"user_query": '''Put all the clean blocks in the tan bowl''',
        "gold_code": '''
        put_first_on_second("pink block", "tan bowl")
        put_first_on_second("teal block", "tan bowl")
        update_wm("Put the pink block and the teal block in the tan bowl")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["blue block", "black block", "pink block", "teal block", "red block", "rust bowl", "tan bowl", "disinfector"],
            #    "relations": [[""blue block" is on "black block" is on "red block""]],
            #    "disinfector": {"contains": []},
            #    "blue block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            #    "pink block": {"is": ["clean"]},
            #    "teal block": {"is": ["clean"]},
            #    "red block": {"is": ["dirty"]},
            #    "tan bowl": {"contains": ["pink block", "teal block"]},
            # }
        '''}
    ]
}

eval_episodes = [eval_episode]
    