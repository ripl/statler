#!/usr/bin/env python3

eval_episode = {
    "init_state": '''
    # state = {
    #     "objects": ["green block", "white block", "red block", "green block", "rust bowl", "magenta bowl", "disinfector"],
    #     "relations": [],
    #     "disinfector": {"contains": []},
    #     "green block": {},
    #     "white block": {},
    #     "red block": {},
    #     "rust bowl": {},
    #     "magenta bowl": {}
    # }
    ''',
    "dirty_object_list": ["green block", "white block"],
    "init_simple_state": '''
    objects = ["green block", "white block", "red block", "green block", "rust bowl", "magenta bowl", "disinfector"],
    ''',
    "episode": [
        {"user_query": '''the white block and the green block are clean.''',
        "gold_code": '''update_wm("the white block and the green block are clean.")''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "red block", "green block", "rust bowl", "magenta bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "white block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''The other blocks are dirty''',
        "gold_code": '''update_wm("the red block is dirty.")''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "red block", "green block", "rust bowl", "magenta bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "white block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "red block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put all the clean blocks on the table.''',
        "gold_code": '''
        put_first_on_second("white block", "table")
        put_first_on_second("green block", "table")
        update_wm("Put the white block and the green block on the relations.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "red block", "green block", "rust bowl", "magenta bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "white block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "red block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the white block on the green block''',
        "gold_code": '''
        put_first_on_second("white block", "green block")
        update_wm("Put the white block on the green block.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "red block", "green block", "rust bowl", "magenta bowl", "disinfector"],
            #    "relations": [[""white block" is on "green block""]],
            #    "disinfector": {"contains": []},
            #    "white block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "red block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''the red block is dirty.''',
        "gold_code": '''update_wm("the red block is dirty.")''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "red block", "green block", "rust bowl", "magenta bowl", "disinfector"],
            #    "relations": [[""white block" is on "green block""]],
            #    "disinfector": {"contains": []},
            #    "white block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "red block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the red block on the white block''',
        "gold_code": '''
        put_first_on_second("red block", "white block")
        update_wm("Put the red block on the white block. the green block, the white block, and the green block become dirty.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "red block", "green block", "rust bowl", "magenta bowl", "disinfector"],
            #    "relations": [[""red block" is on "white block" is on "green block""]],
            #    "disinfector": {"contains": []},
            #    "white block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            #    "red block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put all the dirty blocks on the table.''',
        "gold_code": '''
        put_first_on_second("white block", "table")
        put_first_on_second("green block", "table")
        put_first_on_second("red block", "table")
        update_wm("Put the white block, the green block, and the red block on the relations.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "red block", "green block", "rust bowl", "magenta bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "white block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            #    "red block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the red block and the green block in the disinfector''',
        "gold_code": '''
        put_first_on_second("red block", "disinfector")
        put_first_on_second("green block", "disinfector")
        update_wm("Put the red block and the green block in the disinfector. the red block and the green block become clean.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "red block", "green block", "rust bowl", "magenta bowl", "disinfector"],
            #    "disinfector": {"contains": ["red block", "green block"]},
            #    "white block": {"is": ["dirty"]},
            #    "green block": {"is": ["clean"]},
            #    "red block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put the red block on the white block''',
        "gold_code": '''
        put_first_on_second("red block", "white block")
        update_wm("Put the red block on the white block. the red block becomes dirty.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "red block", "green block", "rust bowl", "magenta bowl", "disinfector"],
            #    "relations": [[""red block" is on "white block""]],
            #    "disinfector": {"contains": ["green block"]},
            #    "white block": {"is": ["dirty"]},
            #    "green block": {"is": ["clean"]},
            #    "red block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the green block on the red block''',
        "gold_code": '''
        put_first_on_second("green block", "red block")
        update_wm("Put the green block on the red block. the green block and the green block become dirty.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "red block", "green block", "rust bowl", "magenta bowl", "disinfector"],
            #    "relations": [[""green block" is on "red block" is on "white block""]],
            #    "disinfector": {"contains": ["green block"]},
            #    "white block": {"is": ["dirty"]},
            #    "green block": {"is": ["dirty"]},
            #    "red block": {"is": ["dirty"]},
            # }
        '''}
    ]
}

eval_episodes = [eval_episode]
