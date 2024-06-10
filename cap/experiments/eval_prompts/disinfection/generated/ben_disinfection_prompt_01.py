#!/usr/bin/env python3

eval_episode = {
    "init_state": '''
    # state = {
    #     "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "orange bowl", "silver bowl", "disinfector"],
    #     "relations": [],
    #     "disinfector": {"contains": []},
    #     "green block": {},
    #     "white block": {},
    #     "black block": {},
    #     "blue block": {},
    #     "pink block": {},
    #     "red block": {},
    #     "orange bowl": {},
    #     "silver bowl": {}
    # }
    ''',
    "dirty_object_list": ["red block"],
    "init_simple_state": '''
    objects = ["green block", "white block", "black block", "blue block", "pink block", "red block", "orange bowl", "silver bowl", "disinfector"],
    ''',
    "episode": [
        {"user_query": '''the red block is dirty.''',
        "gold_code": '''update_wm("the red block is dirty.")''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "orange bowl", "silver bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "red block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''the pink block is clean.''',
        "gold_code": '''update_wm("the pink block is clean.")''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "orange bowl", "silver bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "red block": {"is": ["dirty"]},
            #    "pink block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the pink block in the disinfector''',
        "gold_code": '''
        put_first_on_second("pink block", "disinfector")
        update_wm("Put the pink block in the disinfector. the pink block becomes clean.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "orange bowl", "silver bowl", "disinfector"],
            #    "disinfector": {"contains": ["pink block"]},
            #    "red block": {"is": ["dirty"]},
            #    "pink block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the red block in the orange bowl''',
        "gold_code": '''
        put_first_on_second("red block", "orange bowl")
        update_wm("Put the red block in the orange bowl.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "orange bowl", "silver bowl", "disinfector"],
            #    "disinfector": {"contains": ["pink block"]},
            #    "red block": {"is": ["dirty"]},
            #    "pink block": {"is": ["clean"]},
            #    "orange bowl": {"contains": ["red block"]},
            # }
        '''},

        {"user_query": '''Put all the dirty blocks on the table.''',
        "gold_code": '''
        put_first_on_second("red block", "table")
        update_wm("Put the red block on the relations.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "orange bowl", "silver bowl", "disinfector"],
            #    "disinfector": {"contains": ["pink block"]},
            #    "red block": {"is": ["dirty"]},
            #    "pink block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put all the clean blocks on the table.''',
        "gold_code": '''
        put_first_on_second("pink block", "table")
        update_wm("Put the pink block on the relations.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "orange bowl", "silver bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "red block": {"is": ["dirty"]},
            #    "pink block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the red block on the pink block''',
        "gold_code": '''
        put_first_on_second("red block", "pink block")
        update_wm("Put the red block on the pink block. the pink block becomes dirty.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "orange bowl", "silver bowl", "disinfector"],
            #    "relations": [[""red block" is on "pink block""]],
            #    "disinfector": {"contains": []},
            #    "red block": {"is": ["dirty"]},
            #    "pink block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the red block in the orange bowl''',
        "gold_code": '''
        put_first_on_second("red block", "orange bowl")
        update_wm("Put the red block in the orange bowl.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "orange bowl", "silver bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "red block": {"is": ["dirty"]},
            #    "pink block": {"is": ["dirty"]},
            #    "orange bowl": {"contains": ["red block"]},
            # }
        '''},

        {"user_query": '''Put the red block on the table.''',
        "gold_code": '''
        put_first_on_second("red block", "table")
        update_wm("Put the red block on the table.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "orange bowl", "silver bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "red block": {"is": ["dirty"]},
            #    "pink block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the pink block on the red block''',
        "gold_code": '''
        put_first_on_second("pink block", "red block")
        update_wm("Put the pink block on the red block.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "orange bowl", "silver bowl", "disinfector"],
            #    "relations": [[""pink block" is on "red block""]],
            #    "disinfector": {"contains": []},
            #    "red block": {"is": ["dirty"]},
            #    "pink block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the red block and the pink block in the disinfector''',
        "gold_code": '''
        put_first_on_second("red block", "disinfector")
        put_first_on_second("pink block", "disinfector")
        update_wm("Put the red block and the pink block in the disinfector. the red block and the pink block become clean.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "orange bowl", "silver bowl", "disinfector"],
            #    "disinfector": {"contains": ["red block", "pink block"]},
            #    "red block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put all the clean blocks on the table.''',
        "gold_code": '''
        put_first_on_second("red block", "table")
        put_first_on_second("pink block", "table")
        update_wm("Put the red block and the pink block on the relations.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "orange bowl", "silver bowl", "disinfector"],
            #    "disinfector": {"contains": ["pink block"]},
            #    "red block": {"is": ["clean"]},
            #    "pink block": {"is": ["clean"]},
            # }
        '''}
    ]
}

eval_episodes = [eval_episode]
