import math 
import re

def get_episode_dict_str(d):
    """
    Converts episode information into a string that can be printed to file 
    """
    # print(d)
    key_tags_to_keys = {}
    key_tags_to_val_tags = {}
    val_tags_to_vals = {}
    for idx, (k,v) in enumerate(d.items()):
        key_tag = f"k{idx}"
        val_tag = f"v{idx}"
        key_tags_to_keys[key_tag] = k
        key_tags_to_val_tags[key_tag] = val_tag
        val_tags_to_vals[val_tag] = v
    output_str = repr(key_tags_to_val_tags).replace('\'', '')
    # print(output_str)
    # add keys to output
    for key_tag in key_tags_to_keys.keys():
        n = len(key_tag)
        i = output_str.find(key_tag)
        beginning = output_str[:i]
        ending = output_str[i+n:] 
        key = key_tags_to_keys[key_tag]
        new_line_prefix = "" if key_tag == "k0" else "\n"
        # print("-------------")
        # print(i)
        # print("Beginning:\n", beginning)
        # print("Ending:\n", ending)

        # print("Before:\n", output_str)
        if type(key) == str: 
            output_str = beginning + new_line_prefix + '\'' + key + '\'' + ending
        else: 
            output_str = beginning + new_line_prefix + str(key) +  ending
        # print("After:\n", output_str)

    # add values to output 
    for val_tag in val_tags_to_vals.keys():
        n = len(val_tag)
        i = output_str.find(val_tag)
        beginning = output_str[:i]
        ending = output_str[i+n:] 
        val = val_tags_to_vals[val_tag]
        if type(val) == str: 
            output_str = beginning + '\'\'\'' + val + '\'\'\'' + ending
        else: 
            # print(output_str[:100])
            output_str = beginning + str(val) +  ending
    # print(output_str)
    return output_str 

def get_gold_next_state_string(state):
    """
    Prepares gold_next_state string for episodes from dictionary of state 
    """
    # first we define the world_state variable 
    result = "\n    # world_state = {\n"
    # for each item in the dictionary, we give each a line 
    for key, value in state.items():
        # we do not return values if they are empty 
        if value not in ([], set(), None):
            # key = key if type(key) != str else f"'{key}'"  # Wrap keys in double quotes
            if type(key) == str: 
                key = f"'{key}'"
            # print("---------")
            # print(value)
            if not(any(isinstance(value, t) for t in (str, list, set, dict))):
                value = f"'{value}'"

            # val   ue = value if type(value) not in (str, list, set) else f"'{value}'"
            # print(value)
            result += f"    #    {key}: {value},\n"
    result += "    # }\n"
    return result

def add_prefix_to_lines(input_string, prefix):
    lines = input_string.split("\n")
    modified_lines = [prefix + line for line in lines]
    output_string = "\n".join(modified_lines)
    return output_string


def get_initial_state_str(state):
    """
    """
    s = get_episode_dict_str(state)
    s = s[1:-1]
    s = add_prefix_to_lines(s, "    #     ")
    return s     


def replace_quotes(s):
    # replace ' with " except when it's '''
    return re.sub(r"(?<!')'(?!')", '"', s)


def print_from_repr(obj):
    obj_str = repr(obj)
    n = len(obj_str)
    chunk_size = 50
    k = math.ceil(n/chunk_size)
    for i in range(k):
        print(obj_str[i*chunk_size:(i+1)*chunk_size])

def add_determiners(object_list):
    if len(object_list) == 1:
        return "the " + object_list[0]
    elif len(object_list) == 2:
        return "the " + object_list[0] + " and the " + object_list[1]
    else:
        return "the " + ", the ".join(object_list[:-1]) + ", and the " + object_list[-1]

def save_string_to_file(file_path, string_data):
    with open(file_path, 'w') as file:
        file.write(string_data)