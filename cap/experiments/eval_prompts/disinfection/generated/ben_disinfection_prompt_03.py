#!/usr/bin/env python3

eval_episode = {
    "init_state": '''
    # state = {
    #     "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "gold bowl", "platinum bowl", "disinfector"],
    #     "relations": [],
    #     "disinfector": {"contains": []},
    #     "green block": {},
    #     "white block": {},
    #     "black block": {},
    #     "blue block": {},
    #     "pink block": {},
    #     "red block": {},
    #     "gold bowl": {},
    #     "platinum bowl": {}
    # }
    ''',
    "dirty_object_list": ["black block"],
    "init_simple_state": '''
    objects = ["green block", "white block", "black block", "blue block", "pink block", "red block", "gold bowl", "platinum bowl", "disinfector"],
    ''',
    "episode": [
        {"user_query": '''the blue block, the green block, and the white block are clean.''',
        "gold_code": '''update_wm("the blue block, the green block, and the white block are clean.")''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "gold bowl", "platinum bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "blue block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "white block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''the black block is dirty.''',
        "gold_code": '''update_wm("the black block is dirty.")''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "gold bowl", "platinum bowl", "disinfector"],
            #    "disinfector": {"contains": []},
            #    "blue block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "white block": {"is": ["clean"]},
            #    "black block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the white block on the blue block''',
        "gold_code": '''
        put_first_on_second("white block", "blue block")
        update_wm("Put the white block on the blue block.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "gold bowl", "platinum bowl", "disinfector"],
            #    "relations": [[""white block" is on "blue block""]],
            #    "disinfector": {"contains": []},
            #    "blue block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "white block": {"is": ["clean"]},
            #    "black block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the green block on the black block''',
        "gold_code": '''
        put_first_on_second("green block", "black block")
        update_wm("Put the green block on the black block. the green block becomes dirty.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "gold bowl", "platinum bowl", "disinfector"],
            #    "relations": [[""white block" is on "blue block""], [""green block" is on "black block""]],
            #    "disinfector": {"contains": []},
            #    "blue block": {"is": ["clean"]},
            #    "green block": {"is": ["dirty"]},
            #    "white block": {"is": ["clean"]},
            #    "black block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the blue block, the green block, the white block, and the black block in the disinfector''',
        "gold_code": '''
        put_first_on_second("blue block", "disinfector")
        put_first_on_second("green block", "disinfector")
        put_first_on_second("white block", "disinfector")
        put_first_on_second("black block", "disinfector")
        update_wm("Put the blue block, the green block, the white block, and the black block in the disinfector. the blue block, the green block, the white block, and the black block become clean.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "gold bowl", "platinum bowl", "disinfector"],
            #    "disinfector": {"contains": ["blue block", "green block", "white block", "black block"]},
            #    "blue block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "white block": {"is": ["clean"]},
            #    "black block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''Put all the clean blocks on the table.''',
        "gold_code": '''
        put_first_on_second("blue block", "table")
        put_first_on_second("green block", "table")
        put_first_on_second("white block", "table")
        put_first_on_second("black block", "table")
        update_wm("Put the blue block, the green block, the white block, and the black block on the relations.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "gold bowl", "platinum bowl", "disinfector"],
            #    "disinfector": {"contains": ["black block"]},
            #    "blue block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "white block": {"is": ["clean"]},
            #    "black block": {"is": ["clean"]},
            # }
        '''},

        {"user_query": '''the red block is dirty.''',
        "gold_code": '''update_wm("the red block is dirty.")''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "gold bowl", "platinum bowl", "disinfector"],
            #    "disinfector": {"contains": ["black block"]},
            #    "blue block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "white block": {"is": ["clean"]},
            #    "black block": {"is": ["clean"]},
            #    "red block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the red block in the gold bowl''',
        "gold_code": '''
        put_first_on_second("red block", "gold bowl")
        update_wm("Put the red block in the gold bowl.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "gold bowl", "platinum bowl", "disinfector"],
            #    "disinfector": {"contains": ["black block"]},
            #    "blue block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "white block": {"is": ["clean"]},
            #    "black block": {"is": ["clean"]},
            #    "red block": {"is": ["dirty"]},
            #    "gold bowl": {"contains": ["red block"]},
            # }
        '''},

        {"user_query": '''Put the red block on the table.''',
        "gold_code": '''
        put_first_on_second("red block", "table")
        update_wm("Put the red block on the table.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "gold bowl", "platinum bowl", "disinfector"],
            #    "disinfector": {"contains": ["black block"]},
            #    "blue block": {"is": ["clean"]},
            #    "green block": {"is": ["clean"]},
            #    "white block": {"is": ["clean"]},
            #    "black block": {"is": ["clean"]},
            #    "red block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put the blue block on the red block''',
        "gold_code": '''
        put_first_on_second("blue block", "red block")
        update_wm("Put the blue block on the red block. the blue block becomes dirty.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "gold bowl", "platinum bowl", "disinfector"],
            #    "relations": [[""blue block" is on "red block""]],
            #    "disinfector": {"contains": ["black block"]},
            #    "blue block": {"is": ["dirty"]},
            #    "green block": {"is": ["clean"]},
            #    "white block": {"is": ["clean"]},
            #    "black block": {"is": ["clean"]},
            #    "red block": {"is": ["dirty"]},
            # }
        '''},

        {"user_query": '''Put all the dirty blocks on the table.''',
        "gold_code": '''
        put_first_on_second("blue block", "table")
        put_first_on_second("red block", "table")
        update_wm("Put the blue block and the red block on the relations.")
        ''',
        "gold_next_state": '''
            # state = {
            #    "objects": ["green block", "white block", "black block", "blue block", "pink block", "red block", "gold bowl", "platinum bowl", "disinfector"],
            #    "disinfector": {"contains": ["black block"]},
            #    "blue block": {"is": ["dirty"]},
            #    "green block": {"is": ["clean"]},
            #    "white block": {"is": ["clean"]},
            #    "black block": {"is": ["clean"]},
            #    "red block": {"is": ["dirty"]},
            # }
        '''}
    ]
}

eval_episodes = [eval_episode]
