#!/usr/bin/env python3

eval_episode = {
    "init_state": '''
    # state = {
    #     "objects": ["teal block", "black block", "cyan block", "blue block", "tan bowl", "disinfector"], 
    #     "relations": [], 
    #     "disinfector": {"contains": []}, 
    #     "teal block": {}, 
    #     "black block": {}, 
    #     "cyan block": {}, 
    #     "blue block": {}, 
    #     "tan bowl": {}
    # }
    ''',
    "init_simple_state": '''
    objects = ["teal block", "black block", "cyan block", "blue block", "tan bowl", "disinfector"],
    ''', 
    "episode": [
        {"user_query": '''the teal block and the black block are dirty.''', 
        "gold_code": '''update_wm("the teal block and the black block are dirty.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["teal block", "black block", "cyan block", "blue block", "tan bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "teal block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''The other blocks are clean''', 
        "gold_code": '''update_wm("the blue block and the cyan block are clean.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["teal block", "black block", "cyan block", "blue block", "tan bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "teal block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            #    "blue block": {"is": ["clean"]},
            #    "cyan block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Woops, somebody accidentally polluted the cyan block and the blue block''', 
        "gold_code": '''update_wm("the cyan block and the blue block become dirty.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["teal block", "black block", "cyan block", "blue block", "tan bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "teal block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            #    "blue block": {"is": ["dirty"]},
            #    "cyan block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the cyan block on the teal block''', 
        "gold_code": '''
        put_first_on_second("cyan block", "teal block")
        update_wm("Put the cyan block on the teal block.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["teal block", "black block", "cyan block", "blue block", "tan bowl", "disinfector"],
            #    "relations": [[""cyan block" is on "teal block""]],
            #    "disinfector": {"contains": []},
            #    "teal block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            #    "blue block": {"is": ["dirty"]},
            #    "cyan block": {"is": ["dirty"]},
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
            #    "objects": ["teal block", "black block", "cyan block", "blue block", "tan bowl", "disinfector"],
            #    "relations": [[""cyan block" is on "teal block""]],
            #    "disinfector": {"contains": ["blue block", "black block"]},
            #    "teal block": {"is": ["dirty"]},
            #    "black block": {"is": ["clean"]},
            #    "blue block": {"is": ["clean"]},
            #    "cyan block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the blue block in the tan bowl''', 
        "gold_code": '''
        put_first_on_second("blue block", "tan bowl")
        update_wm("Put the blue block in the tan bowl.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["teal block", "black block", "cyan block", "blue block", "tan bowl", "disinfector"],
            #    "relations": [[""cyan block" is on "teal block""]],
            #    "disinfector": {"contains": ["black block"]},
            #    "teal block": {"is": ["dirty"]},
            #    "black block": {"is": ["clean"]},
            #    "blue block": {"is": ["clean"]},
            #    "cyan block": {"is": ["dirty"]},
            #    "tan bowl": {"contains": ["blue block"]},
            # }
        '''},

        {"user_query": '''Put the blue block on the table.''', 
        "gold_code": '''
        put_first_on_second("blue block", "table")
        update_wm("Put the blue block on the table.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["teal block", "black block", "cyan block", "blue block", "tan bowl", "disinfector"],
            #    "relations": [[""cyan block" is on "teal block""]],
            #    "disinfector": {"contains": ["black block"]},
            #    "teal block": {"is": ["dirty"]},
            #    "black block": {"is": ["clean"]},
            #    "blue block": {"is": ["clean"]},
            #    "cyan block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the black block on the blue block''', 
        "gold_code": '''
        put_first_on_second("black block", "blue block")
        update_wm("Put the black block on the blue block.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["teal block", "black block", "cyan block", "blue block", "tan bowl", "disinfector"],
            #    "relations": [[""cyan block" is on "teal block""], [""black block" is on "blue block""]],
            #    "disinfector": {"contains": []},
            #    "teal block": {"is": ["dirty"]},
            #    "black block": {"is": ["clean"]},
            #    "blue block": {"is": ["clean"]},
            #    "cyan block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put all the dirty blocks on the table.''', 
        "gold_code": '''
        put_first_on_second("teal block", "table")
        put_first_on_second("cyan block", "table")
        update_wm("Put the teal block and the cyan block on the relations.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["teal block", "black block", "cyan block", "blue block", "tan bowl", "disinfector"],
            #    "relations": [[""black block" is on "blue block""]],
            #    "disinfector": {"contains": []},
            #    "teal block": {"is": ["dirty"]},
            #    "black block": {"is": ["clean"]},
            #    "blue block": {"is": ["clean"]},
            #    "cyan block": {"is": ["dirty"]},
            # }
        '''}
    ]
}

eval_episodes = [eval_episode]
    