#!/usr/bin/env python3

eval_episode = {
    "init_state": '''
    # state = {
    #     "objects": ["green block", "white block", "black block", "blue block", "pink block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"], 
    #     "relations": [], 
    #     "disinfector": {"contains": []}, 
    #     "green block": {}, 
    #     "white block": {}, 
    #     "black block": {}, 
    #     "blue block": {}, 
    #     "pink block": {}, 
    #     "rust bowl": {}, 
    #     "magenta bowl": {}, 
    #     "tan bowl": {}, 
    #     "lavender bowl": {}
    # }
    ''',
    "init_simple_state": '''
    objects = ["green block", "white block", "black block", "blue block", "pink block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
    ''', 
    "episode": [
        {"user_query": '''the white block and the green block are clean.''', 
        "gold_code": '''update_wm("the white block and the green block are clean.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "white block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the white block in the rust bowl''', 
        "gold_code": '''
        put_first_on_second("white block", "rust bowl")
        update_wm("Put the white block in the rust bowl.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "white block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "rust bowl": {"contains": ["white block"]},
            # }
        '''},

        {"user_query": '''the pink block is dirty.''', 
        "gold_code": '''update_wm("the pink block is dirty.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "white block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "rust bowl": {"contains": ["white block"]},
            #    "pink block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the pink block in the magenta bowl''', 
        "gold_code": '''
        put_first_on_second("pink block", "magenta bowl")
        update_wm("Put the pink block in the magenta bowl.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "white block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "rust bowl": {"contains": ["white block"]},
            #    "pink block": {"is": ["dirty"]},
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
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "white block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "rust bowl": {"contains": ["white block"]},
            #    "pink block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the white block on the pink block''', 
        "gold_code": '''
        put_first_on_second("white block", "pink block")
        update_wm("Put the white block on the pink block. the white block becomes dirty.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""white block" is on "pink block""]],
            #    "disinfector": {"contains": []},
            #    "white block": {"is": ["dirty"]},
            #    "green block": {"is": ["clean"]},
            #    "pink block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''The other blocks are clean''', 
        "gold_code": '''update_wm("the blue block and the black block are clean.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""white block" is on "pink block""]],
            #    "disinfector": {"contains": []},
            #    "white block": {"is": ["dirty"]},
            #    "green block": {"is": ["clean"]},
            #    "pink block": {"is": ["dirty"]},
            #    "blue block": {"is": ["clean"]},
            #    "black block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Woops, somebody accidentally polluted the blue block and the black block''', 
        "gold_code": '''update_wm("the blue block and the black block become dirty.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""white block" is on "pink block""]],
            #    "disinfector": {"contains": []},
            #    "white block": {"is": ["dirty"]},
            #    "green block": {"is": ["clean"]},
            #    "pink block": {"is": ["dirty"]},
            #    "blue block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the blue block on the black block''', 
        "gold_code": '''
        put_first_on_second("blue block", "black block")
        update_wm("Put the blue block on the black block.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""white block" is on "pink block""], [""blue block" is on "black block""]],
            #    "disinfector": {"contains": []},
            #    "white block": {"is": ["dirty"]},
            #    "green block": {"is": ["clean"]},
            #    "pink block": {"is": ["dirty"]},
            #    "blue block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put all the dirty blocks on the table.''', 
        "gold_code": '''
        put_first_on_second("white block", "table")
        put_first_on_second("pink block", "table")
        put_first_on_second("blue block", "table")
        put_first_on_second("black block", "table")
        update_wm("Put the white block, the pink block, the blue block, and the black block on the relations.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "white block": {"is": ["dirty"]},
            #    "green block": {"is": ["clean"]},
            #    "pink block": {"is": ["dirty"]},
            #    "blue block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the white block, the pink block, the blue block, and the black block in the disinfector''', 
        "gold_code": '''
        put_first_on_second("white block", "disinfector")
        put_first_on_second("pink block", "disinfector")
        put_first_on_second("blue block", "disinfector")
        put_first_on_second("black block", "disinfector")
        update_wm("Put the white block, the pink block, the blue block, and the black block in the disinfector. the white block, the pink block, the blue block, and the black block become clean.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": ["white block", "pink block", "blue block", "black block"]},
            #    "white block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            #    "blue block": {"is": ["clean"]},
            #    "black block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the green block in the tan bowl''', 
        "gold_code": '''
        put_first_on_second("green block", "tan bowl")
        update_wm("Put the green block in the tan bowl.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": ["white block", "pink block", "blue block", "black block"]},
            #    "white block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            #    "blue block": {"is": ["clean"]},
            #    "black block": {"is": ["clean"]},
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
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": ["white block", "pink block", "blue block", "black block"]},
            #    "white block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            #    "blue block": {"is": ["clean"]},
            #    "black block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the white block on the green block''', 
        "gold_code": '''
        put_first_on_second("white block", "green block")
        update_wm("Put the white block on the green block.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""white block" is on "green block""]],
            #    "disinfector": {"contains": ["pink block", "blue block", "black block"]},
            #    "white block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            #    "blue block": {"is": ["clean"]},
            #    "black block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the black block on the table.''', 
        "gold_code": '''
        put_first_on_second("black block", "table")
        update_wm("Put the black block on the table.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""white block" is on "green block""]],
            #    "disinfector": {"contains": ["pink block", "blue block", "black block"]},
            #    "white block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            #    "blue block": {"is": ["clean"]},
            #    "black block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the pink block on the black block''', 
        "gold_code": '''
        put_first_on_second("pink block", "black block")
        update_wm("Put the pink block on the black block.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""pink block" is on ""black block"""], [""white block" is on "green block""]],
            #    "disinfector": {"contains": ["pink block", "blue block", "black block"]},
            #    "white block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            #    "blue block": {"is": ["clean"]},
            #    "black block": {"is": ["clean"]},
            # }
        '''}
    ]
}

eval_episodes = [eval_episode]
    