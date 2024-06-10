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
        {"user_query": '''the blue block and the green block are clean.''', 
        "gold_code": '''update_wm("the blue block and the green block are clean.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "blue block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''The other blocks are dirty''', 
        "gold_code": '''update_wm("the pink block, the black block, and the white block are dirty.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "blue block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "pink block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            #    "white block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put all the dirty blocks on the table.''', 
        "gold_code": '''
        put_first_on_second("pink block", "table")
        put_first_on_second("black block", "table")
        put_first_on_second("white block", "table")
        update_wm("Put the pink block, the black block, and the white block on the relations.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "blue block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "pink block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            #    "white block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the green block on the blue block''', 
        "gold_code": '''
        put_first_on_second("green block", "blue block")
        update_wm("Put the green block on the blue block.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""green block" is on "blue block""]],
            #    "disinfector": {"contains": []},
            #    "blue block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "pink block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            #    "white block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the pink block and the black block in the disinfector''', 
        "gold_code": '''
        put_first_on_second("pink block", "disinfector")
        put_first_on_second("black block", "disinfector")
        update_wm("Put the pink block and the black block in the disinfector. the pink block and the black block become clean.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""green block" is on "blue block""]],
            #    "disinfector": {"contains": ["pink block", "black block"]},
            #    "blue block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            #    "black block": {"is": ["clean"]},
            #    "white block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put all the clean blocks on the table.''', 
        "gold_code": '''
        put_first_on_second("blue block", "table")
        put_first_on_second("green block", "table")
        put_first_on_second("pink block", "table")
        put_first_on_second("black block", "table")
        update_wm("Put the blue block, the green block, the pink block, and the black block on the relations.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "blue block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            #    "black block": {"is": ["clean"]},
            #    "white block": {"is": ["dirty"]},
            # }
        '''}
    ]
}

eval_episodes = [eval_episode]
    