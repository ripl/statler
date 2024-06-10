#!/usr/bin/env python3

eval_episode = {
    "init_state": '''
    # state = {
    #     "objects": ["green block", "blue block", "red block", "rust bowl", "magenta bowl", "disinfector"],
    #     "relations": [],
    #     "disinfector": {"contains": []},
    #     "green block": {},
    #     "blue block": {},
    #     "red block": {},
    #     "rust bowl": {},
    #     "magenta bowl": {}
    # }
    ''',
    "dirty_object_list": ["green block", "blue block"],
    "init_simple_state": '''
    objects = ["green block", "blue block", "red block", "rust bowl", "magenta bowl", "disinfector"],
    ''',
    "episode": [
        {"user_query": '''the blue block and the green block are dirty.''',
        "gold_code": '''update_wm("the blue block and the green block are dirty.")''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "blue block", "red block", "rust bowl", "magenta bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "blue block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''The other blocks are clean''',
        "gold_code": '''update_wm("the red block is clean.")''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "blue block", "red block", "rust bowl", "magenta bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "blue block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            #    "red block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put all the clean blocks on the table.''',
        "gold_code": '''
        put_first_on_second("red block", "table")
        update_wm("Put the red block on the relations.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "blue block", "red block", "rust bowl", "magenta bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "blue block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            #    "red block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put all the dirty blocks on the table.''',
        "gold_code": '''
        put_first_on_second("blue block", "table")
        put_first_on_second("green block", "table")
        update_wm("Put the blue block and the green block on the relations.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "blue block", "red block", "rust bowl", "magenta bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "blue block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            #    "red block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the blue block on the green block''',
        "gold_code": '''
        put_first_on_second("blue block", "green block")
        update_wm("Put the blue block on the green block.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "blue block", "red block", "rust bowl", "magenta bowl", "disinfector"],
            #    "relations": [[""blue block" is on "green block""]],
            #    "disinfector": {"contains": []},
            #    "blue block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            #    "red block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the green block on the blue block''',
        "gold_code": '''
        put_first_on_second("green block", "blue block")
        update_wm("Put the green block on the blue block.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "blue block", "red block", "rust bowl", "magenta bowl", "disinfector"],
            #    "relations": [[""green block" is on "blue block""]],
            #    "disinfector": {"contains": []},
            #    "blue block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            #    "red block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the blue block and the green block in the disinfector''',
        "gold_code": '''
        put_first_on_second("blue block", "disinfector")
        put_first_on_second("green block", "disinfector")
        update_wm("Put the blue block and the green block in the disinfector. the blue block and the green block become clean.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "blue block", "red block", "rust bowl", "magenta bowl", "disinfector"],
            #    "disinfector": {"contains": ["blue block", "green block"]},
            #    "blue block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "red block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put all the clean blocks on the table.''',
        "gold_code": '''
        put_first_on_second("blue block", "table")
        put_first_on_second("green block", "table")
        put_first_on_second("red block", "table")
        update_wm("Put the blue block, the green block, and the red block on the relations.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "blue block", "red block", "rust bowl", "magenta bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "blue block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "red block": {"is": ["clean"]},
            # }
        '''}
    ]
}

eval_episodes = [eval_episode]
