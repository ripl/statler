#!/usr/bin/env python3

eval_episode = {
    "init_state": '''
    # state = {
    #     "objects": ["red block", "green block", "white block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"], 
    #     "relations": [], 
    #     "disinfector": {"contains": []}, 
    #     "red block": {}, 
    #     "green block": {}, 
    #     "white block": {}, 
    #     "purple block": {}, 
    #     "cyan block": {}, 
    #     "rust bowl": {}, 
    #     "magenta bowl": {}, 
    #     "tan bowl": {}, 
    #     "lavender bowl": {}
    # }
    ''',
    "init_simple_state": '''
    objects = ["red block", "green block", "white block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
    ''', 
    "episode": [
        {"user_query": '''the red block and the green block are clean.''', 
        "gold_code": '''update_wm("the red block and the green block are clean.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["red block", "green block", "white block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "red block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Woops, somebody accidentally polluted the red block and the green block''', 
        "gold_code": '''update_wm("the red block and the green block become dirty.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["red block", "green block", "white block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "red block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''The other blocks are clean''', 
        "gold_code": '''update_wm("the purple block, the cyan block, and the white block are clean.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["red block", "green block", "white block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "red block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            #    "purple block": {"is": ["clean"]},
            #    "cyan block": {"is": ["clean"]},
            #    "white block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the cyan block on the red block''', 
        "gold_code": '''
        put_first_on_second("cyan block", "red block")
        update_wm("Put the cyan block on the red block. the cyan block becomes dirty.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["red block", "green block", "white block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""cyan block" is on "red block""]],
            #    "disinfector": {"contains": []},
            #    "red block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            #    "purple block": {"is": ["clean"]},
            #    "cyan block": {"is": ["dirty"]},
            #    "white block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the green block in the tan bowl''', 
        "gold_code": '''
        put_first_on_second("green block", "tan bowl")
        update_wm("Put the green block in the tan bowl.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["red block", "green block", "white block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""cyan block" is on "red block""]],
            #    "disinfector": {"contains": []},
            #    "red block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            #    "purple block": {"is": ["clean"]},
            #    "cyan block": {"is": ["dirty"]},
            #    "white block": {"is": ["clean"]},
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
            #    "objects": ["red block", "green block", "white block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""cyan block" is on "red block""]],
            #    "disinfector": {"contains": []},
            #    "red block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            #    "purple block": {"is": ["clean"]},
            #    "cyan block": {"is": ["dirty"]},
            #    "white block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the white block on the green block''', 
        "gold_code": '''
        put_first_on_second("white block", "green block")
        update_wm("Put the white block on the green block. the white block becomes dirty.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["red block", "green block", "white block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""cyan block" is on "red block""], [""white block" is on "green block""]],
            #    "disinfector": {"contains": []},
            #    "red block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            #    "purple block": {"is": ["clean"]},
            #    "cyan block": {"is": ["dirty"]},
            #    "white block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the green block on the white block''', 
        "gold_code": '''
        put_first_on_second("green block", "white block")
        update_wm("Put the green block on the white block.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["red block", "green block", "white block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""cyan block" is on "red block""], [""green block" is on "white block""]],
            #    "disinfector": {"contains": []},
            #    "red block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            #    "purple block": {"is": ["clean"]},
            #    "cyan block": {"is": ["dirty"]},
            #    "white block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put all the dirty blocks on the table.''', 
        "gold_code": '''
        put_first_on_second("red block", "table")
        put_first_on_second("green block", "table")
        put_first_on_second("cyan block", "table")
        put_first_on_second("white block", "table")
        update_wm("Put the red block, the green block, the cyan block, and the white block on the relations.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["red block", "green block", "white block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "red block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            #    "purple block": {"is": ["clean"]},
            #    "cyan block": {"is": ["dirty"]},
            #    "white block": {"is": ["dirty"]},
            # }
        '''}
    ]
}

eval_episodes = [eval_episode]
