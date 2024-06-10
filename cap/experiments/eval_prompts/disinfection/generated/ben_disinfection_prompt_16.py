#!/usr/bin/env python3

eval_episode = {
    "init_state": '''
    # state = {
    #     "objects": ["green block", "white block", "black block", "blue block", "pink block", "teal block", "gold bowl", "platinum bowl", "disinfector"], 
    #     "relations": [], 
    #     "disinfector": {"contains": []}, 
    #     "green block": {}, 
    #     "white block": {}, 
    #     "black block": {}, 
    #     "blue block": {}, 
    #     "pink block": {}, 
    #     "teal block": {}, 
    #     "gold bowl": {}, 
    #     "platinum bowl": {}
    # }
    ''',
    "init_simple_state": '''
    objects = ["green block", "white block", "black block", "blue block", "pink block", "teal block", "gold bowl", "platinum bowl", "disinfector"],
    ''', 
    "episode": [
        {"user_query": '''the black block is dirty.''', 
        "gold_code": '''update_wm("the black block is dirty.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "teal block", "gold bowl", "platinum bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "black block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''The other blocks are clean''', 
        "gold_code": '''update_wm("the green block, the white block, the pink block, the teal block, and the blue block are clean.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "teal block", "gold bowl", "platinum bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "black block": {"is": ["dirty"]},
            #    "green block": {"is": ["clean"]},
            #    "white block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            #    "teal block": {"is": ["clean"]},
            #    "blue block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the white block on the blue block''', 
        "gold_code": '''
        put_first_on_second("white block", "blue block")
        update_wm("Put the white block on the blue block.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "teal block", "gold bowl", "platinum bowl", "disinfector"],
            #    "relations": [[""white block" is on "blue block""]],
            #    "disinfector": {"contains": []},
            #    "black block": {"is": ["dirty"]},
            #    "green block": {"is": ["clean"]},
            #    "white block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            #    "teal block": {"is": ["clean"]},
            #    "blue block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the green block on the black block''', 
        "gold_code": '''
        put_first_on_second("green block", "black block")
        update_wm("Put the green block on the black block. the green block becomes dirty.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "teal block", "gold bowl", "platinum bowl", "disinfector"],
            #    "relations": [[""green block" is on "black block""], [""white block" is on "blue block""]],
            #    "disinfector": {"contains": []},
            #    "black block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            #    "white block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            #    "teal block": {"is": ["clean"]},
            #    "blue block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the blue block, the green block, the white block, and the black block in the disinfector''', 
        "gold_code": '''
        put_first_on_second("blue block", "disinfector")
        put_first_on_second("green block", "disinfector")
        put_first_on_second("white block", "disinfector")
        put_first_on_second("black block", "disinfector")
        update_wm("Put the blue block, the green block, the white block, and the black block in the disinfector. the blue block, the green block, the white block, and the black block become clean.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "teal block", "gold bowl", "platinum bowl", "disinfector"],
            #    "disinfector": {"contains": ["blue block", "green block", "white block", "black block"]},
            #    "black block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "white block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            #    "teal block": {"is": ["clean"]},
            #    "blue block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put all the clean blocks on the table.''', 
        "gold_code": '''
        put_first_on_second("black block", "table")
        put_first_on_second("green block", "table")
        put_first_on_second("white block", "table")
        put_first_on_second("pink block", "table")
        put_first_on_second("teal block", "table")
        put_first_on_second("blue block", "table")
        update_wm("Put the black block, the green block, the white block, the pink block, the teal block, and the blue block on the relations.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "teal block", "gold bowl", "platinum bowl", "disinfector"],
            #    "disinfector": {"contains": ["black block"]},
            #    "black block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "white block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            #    "teal block": {"is": ["clean"]},
            #    "blue block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''the teal block is dirty.''', 
        "gold_code": '''update_wm("the teal block is dirty.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "teal block", "gold bowl", "platinum bowl", "disinfector"],
            #    "disinfector": {"contains": ["black block"]},
            #    "black block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "white block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            #    "teal block": {"is": ["dirty"]},
            #    "blue block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Woops, somebody accidentally polluted the blue block''', 
        "gold_code": '''update_wm("the blue block become dirty.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "teal block", "gold bowl", "platinum bowl", "disinfector"],
            #    "disinfector": {"contains": ["black block"]},
            #    "black block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "white block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            #    "teal block": {"is": ["dirty"]},
            #    "blue block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the teal block in the gold bowl''', 
        "gold_code": '''
        put_first_on_second("teal block", "gold bowl")
        update_wm("Put the teal block in the gold bowl.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "teal block", "gold bowl", "platinum bowl", "disinfector"],
            #    "disinfector": {"contains": ["black block"]},
            #    "black block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "white block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            #    "teal block": {"is": ["dirty"]},
            #    "blue block": {"is": ["dirty"]},
            #    "gold bowl": {"contains": ["teal block"]},
            # }
        '''},

        {"user_query": '''Put the teal block on the table.''', 
        "gold_code": '''
        put_first_on_second("teal block", "table")
        update_wm("Put the teal block on the table.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "teal block", "gold bowl", "platinum bowl", "disinfector"],
            #    "disinfector": {"contains": ["black block"]},
            #    "black block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "white block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            #    "teal block": {"is": ["dirty"]},
            #    "blue block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the blue block on the teal block''', 
        "gold_code": '''
        put_first_on_second("blue block", "teal block")
        update_wm("Put the blue block on the teal block.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "teal block", "gold bowl", "platinum bowl", "disinfector"],
            #    "relations": [[""blue block" is on "teal block""]],
            #    "disinfector": {"contains": ["black block"]},
            #    "black block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "white block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            #    "teal block": {"is": ["dirty"]},
            #    "blue block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put all the dirty blocks on the table.''', 
        "gold_code": '''
        put_first_on_second("teal block", "table")
        put_first_on_second("blue block", "table")
        update_wm("Put the teal block and the blue block on the relations.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "teal block", "gold bowl", "platinum bowl", "disinfector"],
            #    "disinfector": {"contains": ["black block"]},
            #    "black block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "white block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            #    "teal block": {"is": ["dirty"]},
            #    "blue block": {"is": ["dirty"]},
            # }
        '''}
    ]
}

eval_episodes = [eval_episode]
    