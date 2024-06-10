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
        {"user_query": '''the teal block and the black block are clean.''', 
        "gold_code": '''update_wm("the teal block and the black block are clean.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["blue block", "teal block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "teal block": {"is": ["clean"]},
            #    "black block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''the cyan block and the purple block are clean.''', 
        "gold_code": '''update_wm("the cyan block and the purple block are clean.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["blue block", "teal block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "teal block": {"is": ["clean"]},
            #    "black block": {"is": ["clean"]},
            #    "cyan block": {"is": ["clean"]},
            #    "purple block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''The other blocks are dirty''', 
        "gold_code": '''update_wm("the blue block is dirty.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["blue block", "teal block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "teal block": {"is": ["clean"]},
            #    "black block": {"is": ["clean"]},
            #    "cyan block": {"is": ["clean"]},
            #    "purple block": {"is": ["clean"]},
            #    "blue block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the cyan block on the blue block''', 
        "gold_code": '''
        put_first_on_second("cyan block", "blue block")
        update_wm("Put the cyan block on the blue block. the cyan block becomes dirty.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["blue block", "teal block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""cyan block" is on "blue block""]],
            #    "disinfector": {"contains": []},
            #    "teal block": {"is": ["clean"]},
            #    "black block": {"is": ["clean"]},
            #    "cyan block": {"is": ["dirty"]},
            #    "purple block": {"is": ["clean"]},
            #    "blue block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Woops, somebody accidentally polluted the teal block''', 
        "gold_code": '''update_wm("the teal block become dirty.")''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["blue block", "teal block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""cyan block" is on "blue block""]],
            #    "disinfector": {"contains": []},
            #    "teal block": {"is": ["dirty"]},
            #    "black block": {"is": ["clean"]},
            #    "cyan block": {"is": ["dirty"]},
            #    "purple block": {"is": ["clean"]},
            #    "blue block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the teal block on the black block''', 
        "gold_code": '''
        put_first_on_second("teal block", "black block")
        update_wm("Put the teal block on the black block. the black block becomes dirty.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["blue block", "teal block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""teal block" is on "black block""], [""cyan block" is on "blue block""]],
            #    "disinfector": {"contains": []},
            #    "teal block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            #    "cyan block": {"is": ["dirty"]},
            #    "purple block": {"is": ["clean"]},
            #    "blue block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the teal block in the tan bowl''', 
        "gold_code": '''
        put_first_on_second("teal block", "tan bowl")
        update_wm("Put the teal block in the tan bowl.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["blue block", "teal block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""cyan block" is on "blue block""]],
            #    "disinfector": {"contains": []},
            #    "teal block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            #    "cyan block": {"is": ["dirty"]},
            #    "purple block": {"is": ["clean"]},
            #    "blue block": {"is": ["dirty"]},
            #    "tan bowl": {"contains": ["teal block"]},
            # }
        '''},

        {"user_query": '''Put the teal block on the table.''', 
        "gold_code": '''
        put_first_on_second("teal block", "table")
        update_wm("Put the teal block on the table.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["blue block", "teal block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""cyan block" is on "blue block""]],
            #    "disinfector": {"contains": []},
            #    "teal block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            #    "cyan block": {"is": ["dirty"]},
            #    "purple block": {"is": ["clean"]},
            #    "blue block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the black block on the teal block''', 
        "gold_code": '''
        put_first_on_second("black block", "teal block")
        update_wm("Put the black block on the teal block.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["blue block", "teal block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "relations": [[""cyan block" is on "blue block""], [""black block" is on "teal block""]],
            #    "disinfector": {"contains": []},
            #    "teal block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            #    "cyan block": {"is": ["dirty"]},
            #    "purple block": {"is": ["clean"]},
            #    "blue block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put all the dirty blocks on the table.''', 
        "gold_code": '''
        put_first_on_second("teal block", "table")
        put_first_on_second("black block", "table")
        put_first_on_second("cyan block", "table")
        put_first_on_second("blue block", "table")
        update_wm("Put the teal block, the black block, the cyan block, and the blue block on the relations.")
        ''', 
        "gold_next_state": '''
            # state = {
            #    "objects": ["blue block", "teal block", "black block", "purple block", "cyan block", "rust bowl", "magenta bowl", "tan bowl", "lavender bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "teal block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            #    "cyan block": {"is": ["dirty"]},
            #    "purple block": {"is": ["clean"]},
            #    "blue block": {"is": ["dirty"]},
            # }
        '''}
    ]
}

eval_episodes = [eval_episode]
    