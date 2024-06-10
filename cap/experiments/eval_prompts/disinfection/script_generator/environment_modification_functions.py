from helper_functions import  get_gold_next_state_string, get_episode_dict_str, print_from_repr, add_determiners
import re 
import textwrap

def find_paths_to_object(data, target, path=[]):
    # print(data)

    paths = []
    if isinstance(data, dict):
        for key, value in data.items():
            new_path = path + [key]
            if new_path[0] in set(['objects','containers', 'blocks']):
                continue
            paths += find_paths_to_object(value, target, new_path)
    elif isinstance(data, list) or isinstance(data, set):
        for i, value in enumerate(data):
            new_path = path + [i]
            paths += find_paths_to_object(value, target, new_path)
    elif isinstance(data, str) and target in data:
        paths.append(path)
    return paths



def add_to_table_or_keep_same(state, item):
    """
    Adds item to the table unless it is present somewhere else 
    """
    found = False 
    # check if it exists already 
    paths = find_paths_to_object(state, item)
    # if not, then add it to the table 
    if len(paths)  == 0:
        # check if its in the tables. if not, add it there 
        if "table" not in state.keys():
            state["table"] = []
        state["table"].append([item]) 
    return state       

def add_to_table(state, item):
    """
    Adds item to the table and removes from current location
    """
    state, unstacked = remove_obj_from_environment(state, item)
    state["table"].append([item]) 
    return state, unstacked


def is_dirty_item(state, item):
    """
    Makes items dirty. If they are not present, it adds them. 
    """
    # set the state for the item to dirty 
    if not(item in state["disinfector"]["contains"]):
        state[item] = ["dirty"]
        add_to_table_or_keep_same(state, item)
    return state 



def is_dirty(state, object_list):
    """
    Prepares an episode that makes an object dirty.  
    """
    output = {}
    user_query = ""
    objs = ""

    if len(object_list) == 1: 
        verb = "is"
    if len(object_list) > 1: 
        verb = "are"

    for item in object_list: 
        objs += f" {item},"
        state = is_dirty_item(state, item)
    objs = objs[1:-1]
    output["user_query"] = f"{add_determiners(object_list)} {verb} dirty."
    output["gold_code"] = f"update_wm(\"{output['user_query']}\")"
    output["gold_next_state"] = get_gold_next_state_string(state) 
    return output



def is_clean_item(state, item):
    """
    Makes items clean. If they are not present, it adds them. 
    """
    # set the state for the item to clean 
    state[item] = ["clean"]
    add_to_table_or_keep_same(state, item)
    return state 



def is_clean(state, object_list):
    """
    Prepares an episode that makes an object clean.  
    """
    output = {}
    user_query = ""
    objs = ""

    if len(object_list) == 1: 
        verb = "is"
    if len(object_list) > 1: 
        verb = "are"

    for item in object_list: 
        objs += f" {item},"
        state = is_clean_item(state, item)
    objs = objs[1:-1]
    output["user_query"] = f"{add_determiners(object_list)} {verb} clean."
    output["gold_code"] = f"update_wm(\"{output['user_query']}\")"
    output["gold_next_state"] = get_gold_next_state_string(state) 
    return output



# def unstack_stacking_string(stacking_string):
#     """
#     Converts a stacking string 

#     '\"black block\" is under \"green block\" is under \"white block\"'

#     ["black block", "green block", "white block"]
#     """
#     pattern = r'"([^"]+)"'
#     result = re.findall(pattern, stacking_string)
#     return result
def stack_string_to_list(input_string):
    # Extract the block names using regex
    blocks = re.findall(r'"(.*?)"', input_string)
    return blocks

def unstack_stacking_string(stack, target):
    """
    Converts a stacking string 

    '\"black block\" is under \"green block\" is under \"white block\"'

    ["black block", "green block", "white block"]
    """
    blocks = re.findall(r'"([^"]+)"', stack)
    idx = blocks.index(target)
    if idx > 0: 
        remaining_stack = stack[:stack.find(blocks[idx-1])+len(blocks[idx-1])+1]
    else:
        remaining_stack = ""
    unstacked = blocks[idx:]
    if "under" not in remaining_stack:
        remaining_stack = remaining_stack[1:-1]
    return remaining_stack, unstacked

def get_obj_from_path(state, path):
    c = state
    for key in path[:-1]:
        c = c[key]
    c = c[-1]
    return c

def replace_obj_at_path(state, path, new_obj):
    c = state
    for key in path[:-1]:
        c = c[key] 
    key = path[-1]
    if new_obj != "": 
        c[key] = new_obj
    else:
        del c[key]
    return state

def delete_obj_at_path(state, path):
    c = state
    for key in path[:-1]:
        c = c[key]
    key = path[-1]
    del c[key]
    return state


def is_stacked_relation(state, path):
    # c = container in python (e.g. set, list, dict)
    obj = get_obj_from_path(state, path)
    return True if "under" in obj else False

def remove_empty_lists(state): 
    if "table" in state.keys():
        state["table"] = [el for el in state["table"] if el != []]
    containers = [obj for obj in state["objects"] if "bowl" in obj]
    for container in containers:
        if container in state.keys():
            contents = state[container]["contains"]
            contents = [el for el in contents if el != []]
            if len(contents) == 0:
                if container != "disinfector":
                    del state[container]
            else:
                state[container]["contains"] = contents
    non_containers = set(state["objects"]).difference(set(containers).union(set(["table"])))
    for obj in non_containers: 
        if (obj in state.keys()) and (state[obj] == []):
            del state[obj]
    return state

def remove_obj_from_environment(state, target_obj):
    """
    Removes object from wherever it was sitting but 
    * doesn't delete their state properties (e.g. dirty)
    * automatically puts stacked items in the table 
    """
    # find target
    paths = find_paths_to_object(state, target_obj)
    # print("paths", paths)
    # print(state)
    if len(paths) > 0: 
        path = paths[0]
        found_obj = get_obj_from_path(state, path)
        # delete the target 
        if "under" in found_obj: 
            remaining_stack, unstacked = unstack_stacking_string(found_obj, target_obj)
            state = replace_obj_at_path(state, path, remaining_stack)
            unstacked.remove(target_obj)
            for item in unstacked: 
                if item != target_obj:
                    state = add_to_table_or_keep_same(state, item)
            # clean up empty lists 
            state = remove_empty_lists(state)
            return state, unstacked
        if found_obj in state["objects"]:
            # print("-------------")
            # print(found_obj)
            # print(path)
            # print(state)
            # val = get_obj_from_path(state, path)
            # print(val)
            delete_obj_at_path(state, path)
            # print("!!!!!!!!!!!!!!!!!!!!!!!!!")
            # print(state)
            unstacked = []
            # clean up empty lists 
            state = remove_empty_lists(state)
            return state, unstacked
    return state, []
def put_item_in_disinfector(state, obj):
    state, _ = remove_obj_from_environment(state, obj)
    if (obj in state) and ("dirty" in state[obj]):
        state[obj] = [x for x in state[obj] if x != "dirty"]
    state["disinfector"]["contains"].append(obj)
    state[obj] = ["clean"]
    return state 

def put_in_disinfector(state, object_list):
    """
    Creates episode text for disinfector. 
    """
    output = {}
    gold_code = ""
    objs = ""

    for obj in object_list: 
        state = put_item_in_disinfector(state, obj)
        # get a list of objects for query and gold_code
        objs += f"{obj}, "
        gold_code += f'put_first_on_second(\"{obj}\", "disinfector")\n'
    become = "become" if len(object_list) > 1 else "becomes"
    gold_code += f'update_wm(\"Put {add_determiners(object_list)} in the disinfector. {add_determiners(object_list)} {become} clean.\")'

    output["user_query"] = f"Put {add_determiners(object_list)} in the disinfector"
    output["gold_code"] = gold_code
    output["gold_next_state"] = get_gold_next_state_string(state) 
    return output

def check_dirty_elements(state, stacked_elements):
    for element in stacked_elements:
        if element in state:
            if 'dirty' in state[element]:
                return True
    return False


def stack_block_on_block(state, object_list):
    initial_state = state
    blocks = [obj for obj in state["objects"] if "block" in obj]
    # print("start")
    cleanliness = {}
    for b in blocks: 
        if b in state.keys():
            cleanliness[b] = {"start" : state[b]}

    output = {}
    obj_high = object_list[0]
    obj_low = object_list[1]
    state, _ = remove_obj_from_environment(state, obj_high)
    # print("intermediate:" , state)
    # print(obj_low)
    paths = find_paths_to_object(state, obj_low)
    # print(paths)
    obj_low_path = paths[0]
    path_val = get_obj_from_path(state, obj_low_path)
    if "under" in path_val: 
        stack_objs = stack_string_to_list(path_val)
        idx_low = stack_objs.index(obj_low)
        stack_objs = stack_objs[:idx_low+1] + [obj_high] + stack_objs[idx_low+1:]
    else: 
        stack_objs = [path_val] + [obj_high]
    if "disinfector" in obj_low_path:
         for obj in stack_objs:
            state[obj] = ["clean"]
    else: 
        any_dirty = check_dirty_elements(state, stack_objs)
        if any_dirty == True:
            for obj in stack_objs:
                state[obj] = ["dirty"]
    new_path_val = ""
    for obj in stack_objs:
        new_path_val += f"\"{obj}\" is under "
    new_path_val = new_path_val[:-10] 
    state = replace_obj_at_path(state, obj_low_path, new_path_val)

    changed_cleanliness = {"dirty" : [], "clean": []}
    for b in blocks: 
        if b in state.keys():
            cleanliness[b]["end"] = state[b]
            cleanliness[b]["same"] = (cleanliness[b]["start"]==cleanliness[b]["end"])
            if cleanliness[b]["same"] == False: 
                # print(cleanliness[b]["end"])
                changed_cleanliness[cleanliness[b]["end"][0]].append(b)
    # print("cleanliness:\n", changed_cleanliness)
    gold_code = ""
    gold_code += f'put_first_on_second(\"{obj_high}\", \"{obj_low}\")'
    gold_code += f'\nupdate_wm(\"Put the {obj_high} on the {obj_low}.'
    if len(changed_cleanliness["dirty"]) > 0: 
        become = "become" if len(changed_cleanliness["dirty"]) > 1 else "becomes"
        # objs = ", ".join(changed_cleanliness["dirty"])
        gold_code += f' {add_determiners(changed_cleanliness["dirty"])} {become} dirty.'
    if len(changed_cleanliness["clean"]) > 0: 
        become = "become" if len(changed_cleanliness["clean"]) > 1 else "becomes"
        # objs = ", ".join(changed_cleanliness["clean"])
        gold_code += f' {add_determiners(changed_cleanliness["clean"])} {become} clean.'
    gold_code += "\")"
    output["user_query"] = f"Put the {obj_high} on the {obj_low}"
    output["gold_code"] = gold_code
    output["gold_next_state"] = get_gold_next_state_string(state) 
    return output

def put_block_in_container_by_item(state, obj, container):
    state, unstacked = remove_obj_from_environment(state, obj)
    # print(state, unstacked)
    if not(container in state.keys()):
        state[container] = {"contains" : []}
    # print(state[container])
    state[container]["contains"].append(obj)
    return state, unstacked


def put_block_in_container(state, object_list):
    """
    Creates episode output for putting a block in container 
    """
    initial_state = state
    blocks = [obj for obj in state["objects"] if "block" in obj]
    # print("start")
    cleanliness = {}
    for b in blocks: 
        if b in state.keys():
            cleanliness[b] = {"start" : state[b]}

    container, target_object = object_list
    output = {}
    state, unstacked = put_block_in_container_by_item(state, target_object, container)
    changed_cleanliness = {"dirty" : [], "clean": []}
    for b in blocks: 
        if b in state.keys():
            cleanliness[b]["end"] = state[b]
            cleanliness[b]["same"] = (cleanliness[b]["start"]==cleanliness[b]["end"])
            if cleanliness[b]["same"] == False: 
                # print(cleanliness[b]["end"])
                changed_cleanliness[cleanliness[b]["end"][0]].append(b)
    
    # print("unstacked: ", unstacked)
    gold_code = ""
    if len(unstacked) > 0: 
        prior_distance = 10
        for obj in unstacked:
            gold_code += f'place_pos = parse_position("{prior_distance}cm to the right of {container}"),\n'
            gold_code += f'put_first_on_second("{obj}", place_pos),\n'
            prior_distance += 10
    gold_code += f'put_first_on_second("{target_object}", "{container}")'
    # gold_code = gold_code[:-3]
    if len(unstacked) > 0: 
        # objs = ", ".join(unstacked)
        gold_code += f'\nupdate_wm(\"Put {add_determiners(unstacked)} on the table. Put the {target_object} in the {container}.' 
    else:     
        gold_code += f'\nupdate_wm(\"Put the {target_object} in the {container}.' 
    if len(changed_cleanliness["dirty"]) > 0: 
        # objs = ", ".join(changed_cleanliness["dirty"])
        gold_code += f' {add_determiners(changed_cleanliness["clean"])} become dirty.'
    if len(changed_cleanliness["clean"]) > 0: 
        # objs = ", ".join(changed_cleanliness["clean"])
        gold_code += f' {add_determiners(changed_cleanliness["clean"])} become clean.'
    gold_code += "\")"
    output["user_query"] = f"Put the {target_object} in the {container}"
    output["gold_code"] = gold_code
    output["gold_next_state"] = get_gold_next_state_string(state) 
    return output

def get_dirty_blocks(state):
    target = "dirty"
    paths = find_paths_to_object(state, target)
    dirty_blocks = [path[0] for path in paths]
    return dirty_blocks

def put_all_dirty_on_table(state, object_list=[]):
    dirty_blocks = get_dirty_blocks(state)
    dislocated = set([])
    moved_blocks = []
    for block in dirty_blocks:
        state, unstacked = add_to_table(state, block)
        # print(state,unstacked)
        dislocated = dislocated.union(set(unstacked))
        moved_blocks.append(block)
    output = {}
    prior_distance = 10
    reference_position = moved_blocks[0]
    gold_code = ""
    for obj in moved_blocks:
        gold_code += f'place_pos = parse_position("{prior_distance}cm to the right of {reference_position}")\n'
        gold_code += f'put_first_on_second("{obj}", place_pos)\n'
        prior_distance += 10
    # objs = ", ".join(moved_blocks)
    gold_code += f'update_wm(\"Put {add_determiners(moved_blocks)} on the table.\")'
    output["user_query"] = f"Put all the dirty blocks on the table"
    output["gold_code"] = gold_code
    output["gold_next_state"] = get_gold_next_state_string(state)
    return output

def get_clean_blocks(state):
    target = "clean"
    paths = find_paths_to_object(state, target)
    clean_blocks = [path[0] for path in paths]
    return clean_blocks

def put_all_clean_on_table(state, object_list=[]):
    clean_blocks = get_clean_blocks(state)
    dislocated = set([])
    moved_blocks = []
    for block in clean_blocks:
        state, unstacked = add_to_table(state, block)
        # print(state,unstacked)
        dislocated = dislocated.union(set(unstacked))
        moved_blocks.append(block)
    output = {}
    prior_distance = 10
    reference_position = moved_blocks[0]
    gold_code = ""
    for obj in moved_blocks:
        gold_code += f'place_pos = parse_position("{prior_distance}cm to the right of {reference_position}")\n'
        gold_code += f'put_first_on_second("{obj}", place_pos)\n'
        prior_distance += 10
    # objs = ", ".join(moved_blocks)
    gold_code += f'update_wm(\"Put {add_determiners(moved_blocks)} on the table.\")'
    output["user_query"] = f"Put all the clean blocks on the table"
    output["gold_code"] = gold_code
    output["gold_next_state"] = get_gold_next_state_string(state)
    return output


def get_episode_string(initial_state, actions):
    episodes = []
    state = initial_state
    for action_info in actions: 
        # print("------------")
        # print(action_info)
        # print(state)
        func = action_info[0]
        object_list = action_info[1]
        output = func(state, object_list)
        episodes.append(get_episode_dict_str(output))
    episodes_string = ',\n\n'.join(str(obj) for obj in episodes)
    episodes_string = textwrap.indent(episodes_string, " " * 8)
    return episodes_string

def get_valid_actions(state):
    pass


def add_table_dirty_item(state, target_obj):
    state, _ = add_to_table(state, target_obj)
    state[target_obj] = ["dirty"]
    return state

def add_table_dirty(state, object_list):
    gold_code = ""
    for obj in object_list: 
        state = add_table_dirty_item(state, obj)
        gold_code += f'\nupdate_wm(\"The {obj} is placed on the table, and becomes dirty.\")'
    # objs = ", ".join(object_list)
    output = {}
    output["user_query"] = f"Woops, somebody was moving {add_determiners(object_list)} and dropped them on some dirty region on the table",
    output["gold_code"] = gold_code
    output["gold_next_state"] = get_gold_next_state_string(state) 
    return output

def other_blocks_clean(state, object_list=None):
    blocks = set([obj for obj in state["objects"] if "block" in obj])
    already_stated_blocks = set([obj for obj in state.keys() if "block" in obj])
    unstated_blocks = blocks.difference(already_stated_blocks)
    output = is_clean(state, list(unstated_blocks))
    output["user_query"] = "The other blocks are clean"
    return output 

def other_blocks_dirty(state, object_list=None):
    blocks = set([obj for obj in state["objects"] if "block" in obj])
    already_stated_blocks = set([obj for obj in state.keys() if "block" in obj])
    unstated_blocks = blocks.difference(already_stated_blocks)
    output = is_dirty(state, list(unstated_blocks))
    output["user_query"] = "The other blocks are dirty"
    return output 

def turn_dirty(state, object_list): 
    objs = ""
    
    for obj in object_list: 
        paths = find_paths_to_object(state, obj)
        if len(paths) > 0: 
            objs += f" {obj},"
            state[obj] = ["dirty"]
        else: 
            raise ValueError(f"{obj} isn't in the state yet so it can't be polluted")
    output = {}
    output["user_query"] = f"Woops, somebody accidentally polluted {add_determiners(object_list)}"
    output["gold_code"] = f"update_wm(\"{add_determiners(object_list)} become dirty.\")"
    output["gold_next_state"] = get_gold_next_state_string(state) 
    return output