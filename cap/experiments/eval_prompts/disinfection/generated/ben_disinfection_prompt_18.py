#!/usr/bin/env python3

eval_episode = {
    "init_state": '''
    # state = {
    #     "objects": ["green block", "white block", "yellow block", "gray block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"], 
    #     "relations": [], 
    #     "disinfector": {"contains": []}, 
    #     "green block": {}, 
    #     "white block": {}, 
    #     "yellow block": {}, 
    #     "gray block": {}, 
    #     "cyan block": {}, 
    #     "rust bowl": {}, 
    #     "magenta bowl": {}, 
    #     "tan bowl": {}, 
    #     "lavender bowl": {}
    # }
    ''',
    "init_simple_state": '''
    objects = ["green block", "white block", "yellow block", "gray block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
    ''', 
    "episode": [
        {"user_query": '''the white block and the gray block are dirty.''', 
        "gold_code": '''update_wm("the white block and the gray block are dirty.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "yellow block", "gray block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "white block": {"is": ["dirty"]},
            #    "gray block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''The other blocks are clean''', 
        "gold_code": '''update_wm("the green block, the yellow block, and the cyan block are clean.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "yellow block", "gray block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "white block": {"is": ["dirty"]},
            #    "gray block": {"is": ["dirty"]},
            #    "green block": {"is": ["clean"]},
            #    "yellow block": {"is": ["clean"]},
            #    "cyan block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Woops, somebody accidentally polluted the white block''', 
        "gold_code": '''update_wm("the white block become dirty.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "yellow block", "gray block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "white block": {"is": ["dirty"]},
            #    "gray block": {"is": ["dirty"]},
            #    "green block": {"is": ["clean"]},
            #    "yellow block": {"is": ["clean"]},
            #    "cyan block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the green block, the white block, and the yellow block in the disinfector''', 
        "gold_code": '''
        put_first_on_second("green block", "disinfector")
        put_first_on_second("white block", "disinfector")
        put_first_on_second("yellow block", "disinfector")
        update_wm("Put the green block, the white block, and the yellow block in the disinfector. the green block, the white block, and the yellow block become clean.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "yellow block", "gray block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": ["green block", "white block", "yellow block"]},
            #    "white block": {"is": ["clean"]},
            #    "gray block": {"is": ["dirty"]},
            #    "green block": {"is": ["clean"]},
            #    "yellow block": {"is": ["clean"]},
            #    "cyan block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the gray block in the lavender bowl''', 
        "gold_code": '''
        put_first_on_second("gray block", "lavender bowl")
        update_wm("Put the gray block in the lavender bowl.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "yellow block", "gray block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": ["green block", "white block", "yellow block"]},
            #    "white block": {"is": ["clean"]},
            #    "gray block": {"is": ["dirty"]},
            #    "green block": {"is": ["clean"]},
            #    "yellow block": {"is": ["clean"]},
            #    "cyan block": {"is": ["clean"]},
            #    "lavender bowl": {"contains": ["gray block"]},
            # }
        '''},

        {"user_query": '''Put the gray block on the table.''', 
        "gold_code": '''
        put_first_on_second("gray block", "table")
        update_wm("Put the gray block on the table.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "yellow block", "gray block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": ["green block", "white block", "yellow block"]},
            #    "white block": {"is": ["clean"]},
            #    "gray block": {"is": ["dirty"]},
            #    "green block": {"is": ["clean"]},
            #    "yellow block": {"is": ["clean"]},
            #    "cyan block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the white block on the gray block''', 
        "gold_code": '''
        put_first_on_second("white block", "gray block")
        update_wm("Put the white block on the gray block. the white block becomes dirty.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "yellow block", "gray block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""white block" is on "gray block""]],
            #    "disinfector": {"contains": ["green block", "yellow block"]},
            #    "white block": {"is": ["dirty"]},
            #    "gray block": {"is": ["dirty"]},
            #    "green block": {"is": ["clean"]},
            #    "yellow block": {"is": ["clean"]},
            #    "cyan block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the cyan block in the disinfector''',
        "gold_code": '''
        put_first_on_second("cyan block", "disinfector")
        update_wm("Put the cyan block in the disinfector.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "yellow block", "gray block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""white block" is on "gray block""]],
            #    "disinfector": {"contains": ["green block", "yellow block", "cyan block"]},
            #    "white block": {"is": ["dirty"]},
            #    "gray block": {"is": ["dirty"]},
            #    "green block": {"is": ["clean"]},
            #    "yellow block": {"is": ["clean"]},
            #    "cyan block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put all the clean blocks on the table''',
        "gold_code": '''
        put_first_on_second("green block", "table")
        put_first_on_second("yellow block", "table")
        put_first_on_second("cyan block", "table")
        update_wm("Put the green block, yellow block, and cyan block on the table.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "yellow block", "gray block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""white block" is on "gray block""]],
            #    "disinfector": {"contains": []},
            #    "white block": {"is": ["dirty"]},
            #    "gray block": {"is": ["dirty"]},
            #    "green block": {"is": ["clean"]},
            #    "yellow block": {"is": ["clean"]},
            #    "cyan block": {"is": ["clean"]},
            # }
        '''}
    ]
}

eval_episodes = [eval_episode]
    