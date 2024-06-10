#!/usr/bin/env python3

eval_episode = {
    "init_state": '''
    # state = {
    #     "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "gold bowl", "silver bowl", "disinfector"],
    #     "relations": [],
    #     "disinfector": {"contains": []},
    #     "green block": {},
    #     "white block": {},
    #     "black block": {},
    #     "blue block": {},
    #     "pink block": {},
    #     "red block": {},
    #     "gold bowl": {},
    #     "silver bowl": {}
    # }
    ''',
    "dirty_object_list": ["black block", "blue block"],
    "init_simple_state": '''
    objects = ["green block", "white block", "black block", "blue block", "pink block", "red block", "gold bowl", "silver bowl", "disinfector"],
    ''',
    "episode": [
        {"user_query": '''the blue block and the black block are dirty.''',
        "gold_code": '''update_wm("the blue block and the black block are dirty.")''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "gold bowl", "silver bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "blue block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''the pink block is clean.''',
        "gold_code": '''update_wm("the pink block is clean.")''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "gold bowl", "silver bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "blue block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            #    "pink block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the blue block in the disinfector''',
        "gold_code": '''
        put_first_on_second("blue block", "disinfector")
        update_wm("Put the blue block in the disinfector. the blue block becomes clean.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "gold bowl", "silver bowl", "disinfector"],
            #    "disinfector": {"contains": ["blue block"]},
            #    "blue block": {"is": ["clean"]},
            #    "black block": {"is": ["dirty"]},
            #    "pink block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the pink block in the silver bowl''',
        "gold_code": '''
        put_first_on_second("pink block", "silver bowl")
        update_wm("Put the pink block in the silver bowl.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "gold bowl", "silver bowl", "disinfector"],
            #    "disinfector": {"contains": ["blue block"]},
            #    "blue block": {"is": ["clean"]},
            #    "black block": {"is": ["dirty"]},
            #    "pink block": {"is": ["clean"]},
            #    "silver bowl": {"contains": ["pink block"]},
            # }
        '''},

        {"user_query": '''Put the pink block on the table.''',
        "gold_code": '''
        put_first_on_second("pink block", "table")
        update_wm("Put the pink block on the table.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "gold bowl", "silver bowl", "disinfector"],
            #    "disinfector": {"contains": ["blue block"]},
            #    "blue block": {"is": ["clean"]},
            #    "black block": {"is": ["dirty"]},
            #    "pink block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the blue block on the pink block''',
        "gold_code": '''
        put_first_on_second("blue block", "pink block")
        update_wm("Put the blue block on the pink block.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "gold bowl", "silver bowl", "disinfector"],
            #    "relations": [[""blue block" is on "pink block""]],
            #    "disinfector": {"contains": []},
            #    "blue block": {"is": ["clean"]},
            #    "black block": {"is": ["dirty"]},
            #    "pink block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the black block on the blue block''',
        "gold_code": '''
        put_first_on_second("black block", "blue block")
        update_wm("Put the black block on the blue block. the blue block and the pink block become dirty.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "gold bowl", "silver bowl", "disinfector"],
            #    "relations": [[""black block" is on "blue block" is on "pink block""]],
            #    "disinfector": {"contains": []},
            #    "blue block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            #    "pink block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put all the dirty blocks on the table.''',
        "gold_code": '''
        put_first_on_second("blue block", "table")
        put_first_on_second("black block", "table")
        put_first_on_second("pink block", "table")
        update_wm("Put the blue block, the black block, and the pink block on the relations.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "gold bowl", "silver bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "blue block": {"is": ["dirty"]},
            #    "black block": {"is": ["dirty"]},
            #    "pink block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the black block, the blue block, and the pink block in the disinfector''',
        "gold_code": '''
        put_first_on_second("black block", "disinfector")
        put_first_on_second("blue block", "disinfector")
        put_first_on_second("pink block", "disinfector")
        update_wm("Put the black block, the blue block, and the pink block in the disinfector. the black block, the blue block, and the pink block become clean.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "gold bowl", "silver bowl", "disinfector"],
            #    "disinfector": {"contains": ["black block", "blue block", "pink block"]},
            #    "blue block": {"is": ["clean"]},
            #    "black block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put all the clean blocks on the table.''',
        "gold_code": '''
        put_first_on_second("blue block", "table")
        put_first_on_second("black block", "table")
        put_first_on_second("pink block", "table")
        update_wm("Put the blue block, the black block, and the pink block on the relations.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "gold bowl", "silver bowl", "disinfector"],
            #    "disinfector": {"contains": ["pink block"]},
            #    "blue block": {"is": ["clean"]},
            #    "black block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the pink block on the black block''',
        "gold_code": '''
        put_first_on_second("pink block", "black block")
        update_wm("Put the pink block on the black block.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "gold bowl", "silver bowl", "disinfector"],
            #    "relations": [[""pink block" is on "black block""]],
            #    "disinfector": {"contains": ["pink block"]},
            #    "blue block": {"is": ["clean"]},
            #    "black block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the blue block on the pink block''',
        "gold_code": '''
        put_first_on_second("blue block", "pink block")
        update_wm("Put the blue block on the pink block.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "gold bowl", "silver bowl", "disinfector"],
            #    "relations": [[""blue block" is on ""pink block"""], [""pink block" is on "black block""]],
            #    "disinfector": {"contains": ["pink block"]},
            #    "blue block": {"is": ["clean"]},
            #    "black block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            # }
        '''}
    ]
}

eval_episodes = [eval_episode]
