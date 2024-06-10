#!/usr/bin/env python3

eval_episode = {
    "init_state": '''
    # state = {
    #     "objects": ["yellow block", "purple block", "green block", "white block", "tan bowl", "lavender bowl", "disinfector"], 
    #     "relations": [], 
    #     "disinfector": {"contains": []}, 
    #     "yellow block": {}, 
    #     "purple block": {}, 
    #     "green block": {}, 
    #     "white block": {}, 
    #     "tan bowl": {}, 
    #     "lavender bowl": {}
    # }
    ''',
    "init_simple_state": '''
    objects = ["yellow block", "purple block", "green block", "white block", "tan bowl", "lavender bowl", "disinfector"],
    ''', 
    "episode": [
        {"user_query": '''the yellow block and the purple block are clean.''', 
        "gold_code": '''update_wm("the yellow block and the purple block are clean.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["yellow block", "purple block", "green block", "white block", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "yellow block": {"is": ["clean"]},
            #    "purple block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''The other blocks are dirty''', 
        "gold_code": '''update_wm("the green block and the white block are dirty.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["yellow block", "purple block", "green block", "white block", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "yellow block": {"is": ["clean"]},
            #    "purple block": {"is": ["clean"]},
            #    "green block": {"is": ["dirty"]},
            #    "white block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Woops, somebody accidentally polluted the yellow block and the purple block''', 
        "gold_code": '''update_wm("the yellow block and the purple block become dirty.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["yellow block", "purple block", "green block", "white block", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "yellow block": {"is": ["dirty"]},
            #    "purple block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            #    "white block": {"is": ["dirty"]},
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
            #    "objects": ["yellow block", "purple block", "green block", "white block", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": ["green block", "white block", "yellow block"]},
            #    "yellow block": {"is": ["clean"]},
            #    "purple block": {"is": ["dirty"]},
            #    "green block": {"is": ["clean"]},
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
            #    "objects": ["yellow block", "purple block", "green block", "white block", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": ["white block", "yellow block"]},
            #    "yellow block": {"is": ["clean"]},
            #    "purple block": {"is": ["dirty"]},
            #    "green block": {"is": ["clean"]},
            #    "white block": {"is": ["clean"]},
            #    "tan bowl": {"contains": ["green block"]},
            # }
        '''},

        {"user_query": '''Put the yellow block in the lavender bowl''', 
        "gold_code": '''
        put_first_on_second("yellow block", "lavender bowl")
        update_wm("Put the yellow block in the lavender bowl.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["yellow block", "purple block", "green block", "white block", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": ["white block"]},
            #    "yellow block": {"is": ["clean"]},
            #    "purple block": {"is": ["dirty"]},
            #    "green block": {"is": ["clean"]},
            #    "white block": {"is": ["clean"]},
            #    "tan bowl": {"contains": ["green block"]},
            #    "lavender bowl": {"contains": ["yellow block"]},
            # }
        '''},

        {"user_query": '''Put the green block on the table.''', 
        "gold_code": '''
        put_first_on_second("green block", "table")
        update_wm("Put the green block on the table.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["yellow block", "purple block", "green block", "white block", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": ["white block"]},
            #    "yellow block": {"is": ["clean"]},
            #    "purple block": {"is": ["dirty"]},
            #    "green block": {"is": ["clean"]},
            #    "white block": {"is": ["clean"]},
            #    "lavender bowl": {"contains": ["yellow block"]},
            # }
        '''},

        {"user_query": '''Put the white block on the green block''', 
        "gold_code": '''
        put_first_on_second("white block", "green block")
        update_wm("Put the white block on the green block.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["yellow block", "purple block", "green block", "white block", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""white block" is on "green block""]],
            #    "disinfector": {"contains": []},
            #    "yellow block": {"is": ["clean"]},
            #    "purple block": {"is": ["dirty"]},
            #    "green block": {"is": ["clean"]},
            #    "white block": {"is": ["clean"]},
            #    "lavender bowl": {"contains": ["yellow block"]},
            # }
        '''},

        {"user_query": '''Put the yellow block on the table.''', 
        "gold_code": '''
        put_first_on_second("yellow block", "table")
        update_wm("Put the yellow block on the table.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["yellow block", "purple block", "green block", "white block", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""white block" is on "green block""]],
            #    "disinfector": {"contains": []},
            #    "yellow block": {"is": ["clean"]},
            #    "purple block": {"is": ["dirty"]},
            #    "green block": {"is": ["clean"]},
            #    "white block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the purple block on the yellow block''', 
        "gold_code": '''
        put_first_on_second("purple block", "yellow block")
        update_wm("Put the purple block on the yellow block. the yellow block becomes dirty.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["yellow block", "purple block", "green block", "white block", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""white block" is on "green block""], [""purple block" is on "yellow block""]],
            #    "disinfector": {"contains": []},
            #    "yellow block": {"is": ["dirty"]},
            #    "purple block": {"is": ["dirty"]},
            #    "green block": {"is": ["clean"]},
            #    "white block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the purple block on the table''',
        "gold_code": '''
        put_first_on_second("purple block", "table")
        update_wm("Put the purple block on the table.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["yellow block", "purple block", "green block", "white block", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""white block" is on "green block""]],
            #    "disinfector": {"contains": []},
            #    "yellow block": {"is": ["dirty"]},
            #    "purple block": {"is": ["dirty"]},
            #    "green block": {"is": ["clean"]},
            #    "white block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put all the dirty blocks in the tan bowl''',
        "gold_code": '''
        put_first_on_second("purple block", "tan bowl")
        put_first_on_second("yellow block", "tan bowl")
        update_wm("Put the purple block and the yellow block in the tan bowl.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["yellow block", "purple block", "green block", "white block", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""white block" is on "green block""]],
            #    "disinfector": {"contains": []},
            #    "yellow block": {"is": ["dirty"]},
            #    "purple block": {"is": ["dirty"]},
            #    "green block": {"is": ["clean"]},
            #    "white block": {"is": ["clean"]},
            #    "tan bowl": {"contains": ["purple block", "yellow block"]},
            # }
        '''}
    ]
}

eval_episodes = [eval_episode]
    