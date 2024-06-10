#!/usr/bin/env python3

eval_episode = {
    "init_state": '''
    # state = {
    #     "objects": ["blue block", "teal block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"], 
    #     "relations": [], 
    #     "disinfector": {"contains": []}, 
    #     "blue block": {}, 
    #     "teal block": {}, 
    #     "black block": {}, 
    #     "purple block": {}, 
    #     "cyan block": {}, 
    #     "rust bowl": {}, 
    #     "magenta bowl": {}, 
    #     "tan bowl": {}, 
    #     "lavender bowl": {}
    # }
    ''',
    "init_simple_state": '''
    objects = ["blue block", "teal block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
    ''', 
    "episode": [
        {"user_query": '''the cyan block and the black block are clean.''', 
        "gold_code": '''update_wm("the cyan block and the black block are clean.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["blue block", "teal block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "cyan block": {"is": ["clean"]},
            #    "black block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''the teal block and the purple block are dirty.''', 
        "gold_code": '''update_wm("the teal block and the purple block are dirty.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["blue block", "teal block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "cyan block": {"is": ["clean"]},
            #    "black block": {"is": ["clean"]},
            #    "teal block": {"is": ["dirty"]},
            #    "purple block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''The other blocks are clean''', 
        "gold_code": '''update_wm("the blue block is clean.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["blue block", "teal block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "cyan block": {"is": ["clean"]},
            #    "black block": {"is": ["clean"]},
            #    "teal block": {"is": ["dirty"]},
            #    "purple block": {"is": ["dirty"]},
            #    "blue block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the black block on the purple block''', 
        "gold_code": '''
        put_first_on_second("black block", "purple block")
        update_wm("Put the black block on the purple block. the black block becomes dirty.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["blue block", "teal block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""black block" is on "purple block""]],
            #    "disinfector": {"contains": []},
            #    "cyan block": {"is": ["clean"]},
            #    "black block": {"is": ["dirty"]},
            #    "teal block": {"is": ["dirty"]},
            #    "purple block": {"is": ["dirty"]},
            #    "blue block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the teal block on the black block''', 
        "gold_code": '''
        put_first_on_second("teal block", "black block")
        update_wm("Put the teal block on the black block.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["blue block", "teal block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""teal block" is on "black block" is on "purple block""]],
            #    "disinfector": {"contains": []},
            #    "cyan block": {"is": ["clean"]},
            #    "black block": {"is": ["dirty"]},
            #    "teal block": {"is": ["dirty"]},
            #    "purple block": {"is": ["dirty"]},
            #    "blue block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Woops, somebody accidentally polluted the cyan block''', 
        "gold_code": '''update_wm("the cyan block become dirty.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["blue block", "teal block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""teal block" is on "black block" is on "purple block""]],
            #    "disinfector": {"contains": []},
            #    "cyan block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            #    "teal block": {"is": ["dirty"]},
            #    "purple block": {"is": ["dirty"]},
            #    "blue block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the cyan block in the tan bowl''', 
        "gold_code": '''
        put_first_on_second("cyan block", "tan bowl")
        update_wm("Put the cyan block in the tan bowl.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["blue block", "teal block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""teal block" is on "black block" is on "purple block""]],
            #    "disinfector": {"contains": []},
            #    "cyan block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            #    "teal block": {"is": ["dirty"]},
            #    "purple block": {"is": ["dirty"]},
            #    "blue block": {"is": ["clean"]},
            #    "tan bowl": {"contains": ["cyan block"]},
            # }
        '''},

        {"user_query": '''Put the teal block in the disinfector''', 
        "gold_code": '''
        put_first_on_second("teal block", "disinfector")
        update_wm("Put the teal block in the disinfector. the teal block becomes clean.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["blue block", "teal block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""black block" is on "purple block""]],
            #    "disinfector": {"contains": ["teal block"]},
            #    "cyan block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            #    "teal block": {"is": ["clean"]},
            #    "purple block": {"is": ["dirty"]},
            #    "blue block": {"is": ["clean"]},
            #    "tan bowl": {"contains": ["cyan block"]},
            # }
        '''},

        {"user_query": '''Put the cyan block on the table.''', 
        "gold_code": '''
        put_first_on_second("cyan block", "table")
        update_wm("Put the cyan block on the table.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["blue block", "teal block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""black block" is on "purple block""]],
            #    "disinfector": {"contains": ["teal block"]},
            #    "cyan block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            #    "teal block": {"is": ["clean"]},
            #    "purple block": {"is": ["dirty"]},
            #    "blue block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the black block on the cyan block''', 
        "gold_code": '''
        put_first_on_second("black block", "cyan block")
        update_wm("Put the black block on the cyan block.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["blue block", "teal block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""black block" is on "cyan block""]],
            #    "disinfector": {"contains": ["teal block"]},
            #    "cyan block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            #    "teal block": {"is": ["clean"]},
            #    "purple block": {"is": ["dirty"]},
            #    "blue block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put all the clean blocks on the table.''', 
        "gold_code": '''
        put_first_on_second("teal block", "table")
        put_first_on_second("blue block", "table")
        update_wm("Put the teal block and the blue block on the relations.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["blue block", "teal block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""black block" is on "cyan block""]],
            #    "disinfector": {"contains": []},
            #    "cyan block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            #    "teal block": {"is": ["clean"]},
            #    "purple block": {"is": ["dirty"]},
            #    "blue block": {"is": ["clean"]},
            # }
        '''}
    ]
}

eval_episodes = [eval_episode]
    