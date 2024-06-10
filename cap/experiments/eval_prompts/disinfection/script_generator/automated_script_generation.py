import numpy as np
from helper_functions import get_episode_dict_str
from environment_modification_functions import get_valid_actions, is_clean, is_dirty, put_in_disinfector, \
    put_block_in_container_by_item, put_all_dirty_on_table, put_all_clean_on_table, stack_block_on_block

# seed_value = 123   # Choose any seed value you prefer

# np.random.seed(seed_value)


# target_num_scripts = 5

# script_count = 0

# make this a loop once you get a loop to work 
# while script_count < target_num_scripts:
# make the blocks and bowls 

colors = ["blue", "green", "red", "blue", "bronze", "yellow", "gray", "transparent", "black", "white", "pink"]
n_blocks = np.random.randint(4,len(colors))
n_bowls = np.random.randint(2,5)
blocks = np.random.choice(colors, size=n_blocks, replace=False)
blocks = [f"{color} block" for color in blocks]
bowls = np.random.choice(colors, size=n_bowls, replace=False)
bowls = [f"{color} bowl" for color in bowls]

initial_objects = blocks + bowls + ["table", "disinfector"]
container_list = bowls + ["disinfector"]
initial_state = {"objects": initial_objects,
                "containers" : container_list,
                "disinfector": {"contains": []}}

initial_state_string = get_episode_dict_str(initial_state)

episode_length = np.random.randint(8,20)
action_count = 0

add_actions = [is_dirty, is_clean]
move_actions = [put_in_disinfector, put_block_in_container_by_item, put_all_dirty_on_table, put_all_clean_on_table]
stack_actions = [stack_block_on_block]

blocks_available_to_add = blocks
added = []
moves = []
action_options = {"add" : add_actions, 
               "move" : move_actions, 
               "stack" : stack_actions}

for i in range(12):
    # if we don't have enough blocks added, we should add some 
    if (len(blocks_available_to_add) > 0) and len(added) <= 4: 
        probs = [1,0,0]
    elif (len(added) > 4) and (len(moves) < 3):
        if (len(blocks_available_to_add) > 0): 
            probs = [.2,.6,.2]
        else: 
            probs = [0,.7,.3]

    elif (len(added) > 4) and (len(moves) >= 3):
        if (len(blocks_available_to_add) > 0): 
            probs = [.05, 0.475,0.475]
        else:
            probs = [0, 0.5,0.5]
    
    action_type = np.random.choice(list(action_options.keys()), p=probs)
    action = np.random.choice(action_options[action_type], size=1, replace=False)
    block = np.random.choice(blocks_available_to_add, size=1, replace=False)[0]
    blocks_available_to_add.remove(block)
    added.append(block)
    print(block, blocks_available_to_add) 
    print(added) 
    print(action)

# while (action_count < episode_length) and (len(valid_actions) > 0):
    