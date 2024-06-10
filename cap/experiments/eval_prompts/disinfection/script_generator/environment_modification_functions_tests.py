import unittest 
import math
from helper_functions import get_episode_dict_str, print_from_repr
from environment_modification_functions import  is_dirty_item, is_dirty, is_clean_item, is_clean, \
    remove_obj_from_environment, unstack_stacking_string, find_paths_to_object, add_to_table_or_keep_same, \
    is_stacked_relation, get_obj_from_path, replace_obj_at_path, remove_empty_lists, \
    put_item_in_disinfector, put_in_disinfector, stack_block_on_block,\
    put_block_in_container_by_item, put_block_in_container, get_dirty_blocks, \
    add_to_table, put_all_dirty_on_table # add_item_to_environment, 

class TestEnvironmentalModificationFunctions(unittest.TestCase):
    # def test_add_item_to_environment(self):
    #     # item is not present  
    #     initial_state = {'objects': ['green block', 'white block', 'black block', 'red block', 'blue block', 'transparent bowl', 'purple bowl', 'table', 'disinfector'], 
    #                      'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
    #                      'disinfector': {'contains': []}, 
    #                      'transparent bowl' : {'contains' : []},
    #                      'table' : [['blue block']],
    #                      'blue block' : ['clean'],
    #                      'green block': ['dirty']}
    #     actual_state = add_item_to_environment(initial_state, "green block")
    #     expected_state = {'objects': ['green block', 'white block', 'black block', 'red block', 'blue block', 'transparent bowl', 'purple bowl', 'table', 'disinfector'], 
    #                      'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
    #                      'disinfector': {'contains': []}, 
    #                      'transparent bowl' : {'contains' : []},
    #                      'table' : [['blue block'], ['green block']],
    #                      'blue block' : ['clean'],
    #                      'green block': ['dirty']}
    #     self.assertEqual(expected_state, actual_state)
        
    #     # item is present in table 
    #     initial_state = {'objects': ['green block', 'white block', 'black block', 'red block', 'blue block', 'transparent bowl', 'purple bowl', 'table', 'disinfector'], 
    #                      'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
    #                      'disinfector': {'contains': []}, 
    #                      'transparent bowl' : {'contains' : []},
    #                      'table' : [['blue block'],['green block']],
    #                      'blue block' : ['clean'],
    #                      'green block': ['dirty']}
    #     actual_state = add_item_to_environment(initial_state, "green block")
    #     expected_state = initial_state
    #     self.assertEqual(expected_state, actual_state)

    #     # item is present in disinfector 
    #     initial_state = {'objects': ['green block', 'white block', 'black block', 'red block', 'blue block', 'transparent bowl', 'purple bowl', 'table', 'disinfector'], 
    #                      'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
    #                      'disinfector': {'contains': [['green block']]}, 
    #                      'transparent bowl' : {'contains' : []},
    #                      'table' : [['blue block']],
    #                      'blue block' : ['clean'],
    #                      'green block': ['dirty']}
    #     actual_state = add_item_to_environment(initial_state, "green block")
    #     expected_state = initial_state
    #     self.assertEqual(expected_state, actual_state)

    #     # item is present in disinfector 
    #     initial_state = {'objects': ['green block', 'white block', 'black block', 'red block', 'blue block', 'transparent bowl', 'purple bowl', 'table', 'disinfector'], 
    #                      'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
    #                      'disinfector': {'contains': []}, 
    #                      'transparent bowl' : {'contains' : [['green block']]},
    #                      'table' : [['blue block']],
    #                      'blue block' : ['clean'],
    #                      'green block': ['dirty']}
    #     actual_state = add_item_to_environment(initial_state, "green block")
    #     expected_state = initial_state
    #     self.assertEqual(expected_state, actual_state)

    def test_is_dirty_item(self):
        # item doesn't exist yet 
        initial_state = {'objects': ['green block', 'white block', 'black block', 'red block', 'blue block', 'transparent bowl', 'purple bowl', 'table', 'disinfector'], 
                         'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                         'disinfector': {'contains': []}, 
                         'transparent bowl' : {'contains' : []},
                         'table' : [['blue block']],
                         'blue block' : ['clean']}
        actual_state = is_dirty_item(initial_state, 'green block')
        expected_state = {'objects': ['green block', 'white block', 'black block', 'red block', 'blue block', 'transparent bowl', 'purple bowl', 'table', 'disinfector'], 
                         'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                         'disinfector': {'contains': []}, 
                         'transparent bowl' : {'contains' : []},
                         'table' : [['blue block'], ['green block']],
                         'blue block' : ['clean'],
                         'green block' : ['dirty']}
        self.assertEqual(expected_state, actual_state)
        # item in disinfector 
        initial_state = {'objects': ['green block', 'white block', 'black block', 'red block', 'blue block', 'transparent bowl', 'purple bowl', 'table', 'disinfector'], 
                         'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                         'disinfector': {'contains': ["green block"]}, 
                         'transparent bowl' : {'contains' : []},
                         'table' : [['blue block']],
                         'blue block' : ['clean'],
                         "green block": ['clean']}
        actual_state = is_dirty_item(initial_state, 'green block')
        expected_state = {'objects': ['green block', 'white block', 'black block', 'red block', 'blue block', 'transparent bowl', 'purple bowl', 'table', 'disinfector'], 
                         'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                         'disinfector': {'contains': ["green block"]}, 
                         'transparent bowl' : {'contains' : []},
                         'table' : [['blue block']],
                         'blue block' : ['clean'],
                         "green block": ['clean']}
        self.assertEqual(expected_state, actual_state)
        # item in bowl
        initial_state = {'objects': ['green block', 'white block', 'black block', 'red block', 'blue block', 'transparent bowl', 'purple bowl', 'table', 'disinfector'], 
                         'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                         'disinfector': {'contains': []}, 
                         'transparent bowl' : {'contains' : ["green block"]},
                         'table' : [['blue block']],
                         'blue block' : ['clean'],
                         "green block": ['clean']}
        actual_state = is_dirty_item(initial_state, 'green block')
        expected_state = {'objects': ['green block', 'white block', 'black block', 'red block', 'blue block', 'transparent bowl', 'purple bowl', 'table', 'disinfector'], 
                         'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                         'disinfector': {'contains': []}, 
                         'transparent bowl' : {'contains' : ["green block"]},
                         'table' : [['blue block']],
                         'blue block' : ['clean'],
                         "green block": ['dirty']}
        self.assertEqual(expected_state, actual_state)
    def test_is_clean_item(self):
        # item doesn't exist yet 
        initial_state = {'objects': ['green block', 'white block', 'black block', 'red block', 'blue block', 'transparent bowl', 'purple bowl', 'table', 'disinfector'], 
                         'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                         'disinfector': {'contains': []}, 
                         'transparent bowl' : {'contains' : []},
                         'table' : [['blue block']],
                         'blue block' : ['clean']}
        actual_state = is_clean_item(initial_state, 'green block')
        expected_state = {'objects': ['green block', 'white block', 'black block', 'red block', 'blue block', 'transparent bowl', 'purple bowl', 'table', 'disinfector'], 
                         'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                         'disinfector': {'contains': []}, 
                         'transparent bowl' : {'contains' : []},
                         'table' : [['blue block'], ['green block']],
                         'blue block' : ['clean'],
                         'green block' : ['clean']}
        self.assertEqual(expected_state, actual_state)
        # item in disinfector 
        initial_state = {'objects': ['green block', 'white block', 'black block', 'red block', 'blue block', 'transparent bowl', 'purple bowl', 'table', 'disinfector'], 
                         'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                         'disinfector': {'contains': ["green block"]}, 
                         'transparent bowl' : {'contains' : []},
                         'table' : [['blue block']],
                         'blue block' : ['clean'],
                         "green block": ['clean']}
        actual_state = is_clean_item(initial_state, 'green block')
        expected_state = {'objects': ['green block', 'white block', 'black block', 'red block', 'blue block', 'transparent bowl', 'purple bowl', 'table', 'disinfector'], 
                         'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                         'disinfector': {'contains': ["green block"]}, 
                         'transparent bowl' : {'contains' : []},
                         'table' : [['blue block']],
                         'blue block' : ['clean'],
                         "green block": ['clean']}
        self.assertEqual(expected_state, actual_state)
        # item in bowl
        initial_state = {'objects': ['green block', 'white block', 'black block', 'red block', 'blue block', 'transparent bowl', 'purple bowl', 'table', 'disinfector'], 
                         'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                         'disinfector': {'contains': []}, 
                         'transparent bowl' : {'contains' : ["green block"]},
                         'table' : [['blue block']],
                         'blue block' : ['clean'],
                         "green block": ['clean']}
        actual_state = is_clean_item(initial_state, 'green block')
        expected_state = {'objects': ['green block', 'white block', 'black block', 'red block', 'blue block', 'transparent bowl', 'purple bowl', 'table', 'disinfector'], 
                         'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                         'disinfector': {'contains': []}, 
                         'transparent bowl' : {'contains' : ["green block"]},
                         'table' : [['blue block']],
                         'blue block' : ['clean'],
                         "green block": ['clean']}
        self.assertEqual(expected_state, actual_state)
        

    def test_is_dirty(self):
        initial_state = {'objects': ['green block', 'white block', 'black block', 'red block', 'blue block', 'transparent bowl', 'purple bowl', 'table', 'disinfector'], 
                         'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                         'disinfector': {'contains': []}, 
                         'transparent bowl' : {'contains' : []},
                         'table' : [['blue block']],
                         'blue block' : ['clean']}
        actual_output_dict = is_dirty(initial_state, ['green block'])
        expected_output_dict = {'user_query': 'The green block is dirty.', 'gold_code': 'update_wm(The green block is dirty.)', 'gold_next_state': "\n    # world_state = {\n    #    'objects': ['green block', 'white block', 'black block', 'red block', 'blue block', 'transparent bowl', 'purple bowl', 'table', 'disinfector'],\n    #    'containers': ['transparent bowl', 'disinfector', 'purple bowl'],\n    #    'disinfector': {'contains': []},\n    #    'transparent bowl': {'contains': []},\n    #    'table': [['blue block'], ['green block']],\n    #    'blue block': ['clean'],\n    #    'green block': ['dirty'],\n    # }\n"}
        self.assertEqual(expected_output_dict, actual_output_dict)
    def test_is_clean(self):
        initial_state = {'objects': ['green block', 'white block', 'black block', 'red block', 'blue block', 'transparent bowl', 'purple bowl', 'table', 'disinfector'], 
                         'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                         'disinfector': {'contains': []}, 
                         'transparent bowl' : {'contains' : []},
                         'table' : [['blue block']],
                         'blue block' : ['clean']}
        actual_output_dict = is_clean(initial_state, ['green block'])
        expected_output_dict = {'user_query': 'The green block is clean.', 'gold_code': 'update_wm(The green block is clean.)', 'gold_next_state': "\n    # world_state = {\n    #    'objects': ['green block', 'white block', 'black block', 'red block', 'blue block', 'transparent bowl', 'purple bowl', 'table', 'disinfector'],\n    #    'containers': ['transparent bowl', 'disinfector', 'purple bowl'],\n    #    'disinfector': {'contains': []},\n    #    'transparent bowl': {'contains': []},\n    #    'table': [['blue block'], ['green block']],\n    #    'blue block': ['clean'],\n    #    'green block': ['clean'],\n    # }\n"}
        self.assertEqual(expected_output_dict, actual_output_dict)

    def test_unstack_stacking_string(self):
        initial_state = {'objects': ["green block", "white block", "black block", "red block", "transparent bowl", "table", "disinfector"], 
                         'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                         'disinfector': {'contains': []}, 
                         'table' : [['\"black block\" is under \"green block\" is under \"white block\" is under \"red block\"']],
                         'green block' : ['dirty'],
                         'black block' : ['dirty'],
                         'white block' : ['dirty'],
                         'red block' : ['dirty']}
        s = initial_state["table"][0][0] 
        target = "white block"
        actual_remaining_str, actual_ustacked_objects = unstack_stacking_string(s, target)
        expected_unstacked_objects = ['white block', 'red block']
        expected_remaining_str = '\"black block\" is under \"green block\"'
        self.assertEqual(expected_unstacked_objects, actual_ustacked_objects)
        self.assertEqual(expected_remaining_str, actual_remaining_str)

    def test_find_paths_to_object(self):
        state = {
                    'objects': ["green block", "white block", "red block", "black block", "blue block", "transparent bowl", "table", "disinfector"], 
                    'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                    'disinfector': {'contains': ["blue block"]}, 
                    'table' : [['\"black block\" is under \"green block\" is under \"white block\"']],
                    'green block' : ['dirty'],
                    'black block' : ['dirty'],
                    'transparent bowl' : {"contains" : ["red block"]},
                    'white block' : ['dirty']
                }
        actual_paths = find_paths_to_object(state, "blue block")
        expected_paths = [['disinfector', 'contains', 0]]
        self.assertEqual(expected_paths, actual_paths)
        actual_paths = find_paths_to_object(state, "red block")
        expected_paths = [['transparent bowl', 'contains', 0]]
        self.assertEqual(expected_paths, actual_paths)
        actual_paths = find_paths_to_object(state, "white block")
        expected_paths = [['table', 0, 0]]
        self.assertEqual(expected_paths, actual_paths)

        initial_state = {'objects': ['green block', 'white block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 
                         'containers': ['transparent bowl', 'disinfector'], 
                         'disinfector': {'contains': []}, 
                         'green block': ['dirty'], 
                         'table': [['green block'], ['black block']], 
                         'white block': ['dirty'], 
                         'black block': ['clean']}
        actual_paths = find_paths_to_object(initial_state, "black block")
        expected_paths = [['table', 1, 0]]
        self.assertEqual(expected_paths, actual_paths)
    def test_add_to_table_or_keep_same(self):
        # item is not present  
        initial_state = {'objects': ['green block', 'white block', 'black block', 'red block', 'blue block', 'transparent bowl', 'purple bowl', 'table', 'disinfector'], 
                         'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                         'disinfector': {'contains': []}, 
                         'transparent bowl' : {'contains' : []},
                         'table' : [['blue block']],
                         'blue block' : ['clean'],
                         'green block': ['dirty']}
        actual_state = add_to_table_or_keep_same(initial_state, "green block")
        expected_state = {'objects': ['green block', 'white block', 'black block', 'red block', 'blue block', 'transparent bowl', 'purple bowl', 'table', 'disinfector'], 
                         'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                         'disinfector': {'contains': []}, 
                         'transparent bowl' : {'contains' : []},
                         'table' : [['blue block'], ['green block']],
                         'blue block' : ['clean'],
                         'green block': ['dirty']}
        self.assertEqual(expected_state, actual_state)
        
        # item is present in table 
        initial_state = {'objects': ['green block', 'white block', 'black block', 'red block', 'blue block', 'transparent bowl', 'purple bowl', 'table', 'disinfector'], 
                         'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                         'disinfector': {'contains': []}, 
                         'transparent bowl' : {'contains' : []},
                         'table' : [['blue block'],['green block']],
                         'blue block' : ['clean'],
                         'green block': ['dirty']}
        actual_state = add_to_table_or_keep_same(initial_state, "green block")
        expected_state = initial_state
        self.assertEqual(expected_state, actual_state)

        # item is present in disinfector 
        initial_state = {'objects': ['green block', 'white block', 'black block', 'red block', 'blue block', 'transparent bowl', 'purple bowl', 'table', 'disinfector'], 
                         'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                         'disinfector': {'contains': [['green block']]}, 
                         'transparent bowl' : {'contains' : []},
                         'table' : [['blue block']],
                         'blue block' : ['clean'],
                         'green block': ['dirty']}
        actual_state = add_to_table_or_keep_same(initial_state, "green block")
        expected_state = initial_state
        self.assertEqual(expected_state, actual_state)

        # item is present in disinfector 
        initial_state = {'objects': ['green block', 'white block', 'black block', 'red block', 'blue block', 'transparent bowl', 'purple bowl', 'table', 'disinfector'], 
                         'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                         'disinfector': {'contains': []}, 
                         'transparent bowl' : {'contains' : [['green block']]},
                         'table' : [['blue block']],
                         'blue block' : ['clean'],
                         'green block': ['dirty']}
        actual_state = add_to_table_or_keep_same(initial_state, "green block")
        expected_state = initial_state
        self.assertEqual(expected_state, actual_state)
    def test_is_stacked_relation(self):
        # a stacked example 
        state = {
                    'objects': ["green block", "white block", "red block", "black block", "blue block", "transparent bowl", "table", "disinfector"], 
                    'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                    'disinfector': {'contains': ["blue block"]}, 
                    'table' : [['\"black block\" is under \"green block\" is under \"white block\"']],
                    'green block' : ['dirty'],
                    'black block' : ['dirty'],
                    'transparent bowl' : {"contains" : ["red block"]},
                    'white block' : ['dirty']
                }
        paths = find_paths_to_object(state, "green block")
        actual_output = is_stacked_relation(state, paths[0])  
        expected_output = True
        self.assertEqual(expected_output, actual_output)    
        # an unstacked example 
        state = {
                    'objects': ["green block", "white block", "red block", "black block", "blue block", "transparent bowl", "table", "disinfector"], 
                    'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                    'disinfector': {'contains': ["blue block"]}, 
                    'table' : [['\"black block\" is under \"green block\" is under \"white block\"']],
                    'green block' : ['dirty'],
                    'black block' : ['dirty'],
                    'transparent bowl' : {"contains" : ["red block"]},
                    'white block' : ['dirty']
                }
        paths = find_paths_to_object(state, "red block")
        actual_output = is_stacked_relation(state, paths[0])  
        expected_output = False
        self.assertEqual(expected_output, actual_output) 
    def test_get_obj_from_path(self):
        initial_state = {
                        'objects': ["green block", "white block", "red block", "black block", "blue block", "transparent bowl", "table", "disinfector"], 
                        'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                        'disinfector': {'contains': ["blue block"]}, 
                        'table' : [['\"black block\" is under \"green block\" is under \"white block\"']],
                        'green block' : ['dirty'],
                        'black block' : ['dirty'],
                        'transparent bowl' : {"contains" : ["red block"]},
                        'white block' : ['dirty']
                    }
        target = "black block" 
        paths = find_paths_to_object(initial_state, target)
        path = paths[0]
        actual_obj = get_obj_from_path(initial_state, path)
        expected_obj = '\"black block\" is under \"green block\" is under \"white block\"'
        self.assertEqual(expected_obj, actual_obj)  

    def test_replace_obj_at_path(self):
        initial_state = {
                        'objects': ["green block", "white block", "red block", "black block", "blue block", "transparent bowl", "table", "disinfector"], 
                        'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                        'disinfector': {'contains': ["blue block"]}, 
                        'table' : [['\"black block\" is under \"green block\" is under \"white block\"']],
                        'green block' : ['dirty'],
                        'black block' : ['dirty'],
                        'transparent bowl' : {"contains" : ["red block"]},
                        'white block' : ['dirty']
                    }
        target = "red block"
        new_obj = "blue block"
        paths = find_paths_to_object(initial_state, target)
        actual_state = replace_obj_at_path(initial_state, paths[0], new_obj)
        expected_state = {'objects': ['green block', 'white block', 'red block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 'disinfector': {'contains': ['blue block']}, 'table': [['"black block" is under "green block" is under "white block"']], 'green block': ['dirty'], 'black block': ['dirty'], 'transparent bowl': {'contains': ['blue block']}, 'white block': ['dirty']}
        self.assertEqual(expected_state, actual_state)


    def test_remove_empty_lists(self):
        initial_state = {'objects': ['green block', 'white block', 'red block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 
                         'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                         'disinfector': {'contains': ['blue block']}, 
                         'table': [[], ['green block'], ['white block']], 
                         'green block': ['dirty'], 
                         'black block': ['dirty'], 
                         'transparent bowl': {'contains': [[]]}, 
                         'white block': ['dirty']}
        actual_state = remove_empty_lists(initial_state)
        expected_state = {'objects': ['green block', 'white block', 'red block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 
                         'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                         'disinfector': {'contains': ['blue block']}, 
                         'table': [ ['green block'], ['white block']], 
                         'green block': ['dirty'], 
                         'black block': ['dirty'], 
                         'transparent bowl': {'contains': []}, 
                         'white block': ['dirty']}
        # print(actual_state)
    def test_remove_obj_from_environment(self):
        initial_state = {'objects': ['green block', 'white block', 'black block', 'red block', 'blue block', 'transparent bowl', 'purple bowl', 'table', 'disinfector'], 
                         'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                         'disinfector': {'contains': []}, 
                         'transparent bowl' : {'contains' : [['green block']]},
                         'table' : [['blue block']],
                         'blue block' : ['clean'],
                         'green block': ['dirty']}  
        target = "green block"
        actual_state, _ = remove_obj_from_environment(initial_state, target) 
        expected_state ={'objects': ['green block', 'white block', 'black block', 'red block', 'blue block', 'transparent bowl', 'purple bowl', 'table', 'disinfector'], 
                         'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                         'disinfector': {'contains': []}, 
                         'table': [['blue block']], 
                         'blue block': ['clean'], 
                         'green block': ['dirty']}     
        self.assertEqual(expected_state, actual_state)
        # stacked target, entire thing 
        initial_state = {
                        'objects': ["green block", "white block", "red block", "black block", "blue block", "transparent bowl", "table", "disinfector"], 
                        'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                        'disinfector': {'contains': ["blue block"]}, 
                        'table' : [['\"black block\" is under \"green block\" is under \"white block\"']],
                        'green block' : ['dirty'],
                        'black block' : ['dirty'],
                        'transparent bowl' : {"contains" : ["red block"]},
                        'white block' : ['dirty']
                    }
        target = "black block"
        actual_state, _ = remove_obj_from_environment(initial_state, target) 
        expected_state = {'objects': ['green block', 'white block', 'red block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 
                          'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                          'disinfector': {'contains': ['blue block']}, 
                          'table': [['green block'], ['white block']], 
                          'green block': ['dirty'], 
                          'black block': ['dirty'], 
                          'transparent bowl': {'contains': ['red block']}, 
                          'white block': ['dirty']}
        self.assertEqual(expected_state, actual_state)
        # stacked target, partial thing 
        initial_state = {
                        'objects': ["green block", "white block", "red block", "black block", "blue block", "transparent bowl", "table", "disinfector"], 
                        'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                        'disinfector': {'contains': ["blue block"]}, 
                        'table' : [['\"black block\" is under \"green block\" is under \"white block\"']],
                        'green block' : ['dirty'],
                        'black block' : ['dirty'],
                        'transparent bowl' : {"contains" : ["red block"]},
                        'white block' : ['dirty']
                    }
        target = "green block"
        actual_state, _ = remove_obj_from_environment(initial_state, target)
        expected_state = {'objects': ['green block', 'white block', 'red block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 
                          'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                          'disinfector': {'contains': ['blue block']}, 
                          'table': [['black block'], ['white block']], 
                          'green block': ['dirty'], 
                          'black block': ['dirty'], 
                          'transparent bowl': {'contains': ['red block']}, 
                          'white block': ['dirty']}
        self.assertEqual(expected_state, actual_state)
        initial_state = {'objects': ['green block', 'white block', 'red block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 
                         'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                         'disinfector': {'contains': ['blue block', 'green block']}, 
                         'table': [], 
                         'green block': ['clean'], 
                         'black block': ['dirty'], 
                         'blue block': ['clean'], 
                         'red block': ['dirty'], 
                         'transparent bowl': {'contains': ['black block', 'red block']}, 
                         'white block': ['dirty']}
        
        target = "black block"
        actual_state, removed = remove_obj_from_environment(initial_state, target)
        expected_state = {'objects': ['green block', 'white block', 'red block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                          'disinfector': {'contains': ['blue block', 'green block']}, 
                          'table': [], 'green block': ['clean'], 
                          'black block': ['dirty'], 
                          'blue block': ['clean'], 
                          'red block': ['dirty'], 
                          'transparent bowl': {'contains': ['red block']}, 
                          'white block': ['dirty']}

        initial_state = {'objects': ['green block', 'white block', 'red block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 
                        'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                        'disinfector': {'contains': ['blue block', 'green block']}, 
                        'table': [], 
                        'green block': ['clean'], 
                        'black block': ['dirty'], 
                        'blue block': ['clean'],
                        'red block': ['dirty'], 
                        'transparent bowl': {'contains': ['white block', 'black block', 'red block']}, 
                        'white block': ['dirty']} 
        target = "black block"
        actual_state, removed = remove_obj_from_environment(initial_state, target)
        expected_state = {'objects': ['green block', 'white block', 'red block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 
                          'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                          'disinfector': {'contains': ['blue block', 'green block']}, 
                          'table': [], 'green block': ['clean'], 
                          'black block': ['dirty'], 
                          'blue block': ['clean'], 
                          'red block': ['dirty'], 
                          'transparent bowl': {'contains': ['white block', 'red block']}, 
                          'white block': ['dirty']}
        self.assertEqual(expected_state,actual_state)
    
    def test_put_item_in_disinfector(self):
        # insert from table 
        initial_state = {'objects': ['green block', 'white block', 'red block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 
                          'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                          'disinfector': {'contains': ['blue block']}, 
                          'table': [['black block'], ['white block']], 
                          'green block': ['dirty'], 
                          'black block': ['dirty'], 
                          'transparent bowl': {'contains': ['red block']}, 
                          'white block': ['dirty']}
        target = 'black block'
        actual_state = put_item_in_disinfector(initial_state, target)
        expected_state = {'objects': ['green block', 'white block', 'red block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 
                          'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                          'disinfector': {'contains': ['blue block', 'black block']}, 
                          'table': [['white block']], 
                          'green block': ['dirty'], 
                          'black block': ['clean'], 
                          'transparent bowl': {'contains': ['red block']}, 
                          'white block': ['dirty']}
        self.assertEqual(expected_state, actual_state)
        # insert from bowl 
        initial_state = {'objects': ['green block', 'white block', 'red block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 
                          'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                          'disinfector': {'contains': ['blue block']}, 
                          'table': [['black block'], ['white block']], 
                          'green block': ['dirty'], 
                          'black block': ['dirty'], 
                          'transparent bowl': {'contains': ['red block']}, 
                          'white block': ['dirty']}
        target = 'red block'
        actual_state = put_item_in_disinfector(initial_state, target)
        expected_state = {'objects': ['green block', 'white block', 'red block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                          'disinfector': {'contains': ['blue block', 'red block']}, 
                          'table': [['black block'], ['white block']], 
                          'green block': ['dirty'], 
                          'black block': ['dirty'], 
                          'white block': ['dirty'], 
                          'red block': ['clean']}
        self.assertEqual(expected_state, actual_state)
    def test_put_in_disinfector(self):
            # insert from table 
        initial_state = {'objects': ['green block', 'white block', 'red block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 
                          'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                          'disinfector': {'contains': ['blue block']}, 
                          'table': [['black block'], ['white block']], 
                          'green block': ['dirty'], 
                          'black block': ['dirty'], 
                          'transparent bowl': {'contains': ['red block']}, 
                          'white block': ['dirty']}
        obj_list = ['black block']
        actual_state = put_in_disinfector(initial_state, obj_list)
        # print(get_episode_dict_str(actual_state))
        expected_state = {'user_query': 'Put black block, in the disinfector', 'gold_code': 'put_first_on_second(black block, "disinfector")', 'gold_next_state': "\n    # world_state = {\n    #    'objects': ['green block', 'white block', 'red block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'],\n    #    'containers': ['transparent bowl', 'disinfector', 'purple bowl'],\n    #    'disinfector': {'contains': ['blue block', 'black block']},\n    #    'table': [['white block']],\n    #    'green block': ['dirty'],\n    #    'black block': ['clean'],\n    #    'transparent bowl': {'contains': ['red block']},\n    #    'white block': ['dirty'],\n    # }\n"}
        self.assertEqual(expected_state, actual_state)

    def test_stack_block_on_block(self):
        # stack within table 
        initial_state = {'objects': ['green block', 'white block', 'red block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 
                          'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                          'disinfector': {'contains': ['blue block']}, 
                          'table': [['\"black block\" is under \"green block\"'], ['white block']], 
                          'green block': ['dirty'], 
                          'black block': ['dirty'], 
                          'transparent bowl': {'contains': ['red block']}, 
                          'white block': ['clean']}
        obj_list = ["white block", 'black block']
        actual_state = stack_block_on_block(initial_state, obj_list)
        expected_state = {'objects': ['green block', 'white block', 'red block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 
                          'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                          'disinfector': {'contains': ['blue block']}, 
                          'table': [['"black block" is under "white block" is under "green block"']], 
                          'green block': ['dirty'], 
                          'black block': ['dirty'], 
                          'transparent bowl': {'contains': ['red block']}, 
                          'white block': ['dirty']}
        self.assertEqual(expected_state, actual_state)
        # stack within disinfector 
        initial_state = {'objects': ['green block', 'white block', 'red block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 
                          'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                          'disinfector': {'contains': ['blue block', '\"black block\" is under \"green block\"']}, 
                          'table': [['white block']], 
                          'green block': ['dirty'], 
                          'black block': ['dirty'], 
                          'transparent bowl': {'contains': ['red block']}, 
                          'white block': ['clean']}
        obj_list = ["white block", 'black block']
        actual_state = stack_block_on_block(initial_state, obj_list)
        # print(actual_state)
        expected_state = {'objects': ['green block', 'white block', 'red block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 
                          'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                          'disinfector': {'contains': ['blue block','"black block" is under "white block" is under "green block"']}, 
                          'table': [], 
                          'green block': ['clean'], 
                          'black block': ['clean'], 
                          'transparent bowl': {'contains': ['red block']}, 
                          'white block': ['clean']}
        self.assertEqual(expected_state, actual_state)
        # stack within transparent bowl 
        initial_state = {'objects': ['green block', 'white block', 'red block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 
                          'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                          'disinfector': {'contains': ['red block']}, 
                          'table': [['white block']], 
                          'green block': ['dirty'], 
                          'black block': ['dirty'], 
                          'transparent bowl': {'contains': ['blue block', '\"black block\" is under \"green block\"']}, 
                          'white block': ['clean']}
        obj_list = ["white block", 'black block']
        actual_state = stack_block_on_block(initial_state, obj_list)
        expected_state = {'objects': ['green block', 'white block', 'red block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 
                          'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                          'disinfector': {'contains': ['red block']}, 'table': [], 
                          'green block': ['dirty'], 
                          'black block': ['dirty'], 
                          'transparent bowl': {'contains': ['blue block', '"black block" is under "white block" is under "green block"']}, 
                          'white block': ['dirty']}
        self.assertEqual(expected_state, actual_state)
        initial_state = {'objects': ['green block', 'white block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 
                         'containers': ['transparent bowl', 'disinfector'], 
                         'disinfector': {'contains': []}, 
                         'green block': ['dirty'], 
                         'table': [['green block'], ['white block'], ['black block']], 
                         'white block': ['dirty'], 
                         'black block': ['clean']}
        obj_list = ["white block","black block"]
        actual_state = stack_block_on_block(initial_state, obj_list)
        expected_state = {'objects': ['green block', 'white block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 'containers': ['transparent bowl', 'disinfector'], 'disinfector': {'contains': []}, 'green block': ['dirty'], 'table': [['green block'], ['"black block" is under "white block"']], 'white block': ['dirty'], 'black block': ['dirty']}
        self.assertEqual(expected_state, actual_state)
    def test_put_block_in_container_by_item(self):
        # move object from disinfector to transparent bowl 
        initial_state = {'objects': ['green block', 'white block', 'red block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 
                          'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                          'disinfector': {'contains': ['blue block']}, 
                          'table': [['\"black block\" is under \"green block\"'], ['white block']], 
                          'green block': ['dirty'], 
                          'black block': ['dirty'], 
                          'blue block' : ["clean"], 
                          'red block' : ["dirty"],
                          'transparent bowl': {'contains': ['red block']}, 
                          'white block': ['clean']}
        target = "blue block"
        container = "transparent bowl"
        actual_state, _ = put_block_in_container_by_item(initial_state, target, container)
        expected_state = {'objects': ['green block', 'white block', 'red block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 
                            'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 'disinfector': {'contains': []}, 'table': [['"black block" is under "green block"'], ['white block']], 
                            'green block': ['dirty'], 
                            'black block': ['dirty'], 
                            'blue block': ['clean'], 
                            'red block': ['dirty'], 
                            'transparent bowl': {'contains': ['red block', 'blue block']}, 
                            'white block': ['clean']}
        self.assertEqual(expected_state, actual_state)
        # move object from disinfector to transparent bowl 
        initial_state = {'objects': ['green block', 'white block', 'red block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 
                          'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                          'disinfector': {'contains': ['blue block']}, 
                          'table': [['\"black block\" is under \"green block\"'], ['white block']], 
                          'green block': ['dirty'], 
                          'black block': ['dirty'], 
                          'blue block' : ["clean"], 
                          'red block' : ["dirty"],
                          'transparent bowl': {'contains': ['red block']}, 
                          'white block': ['clean']}
        target = "black block"
        container = "transparent bowl"
        actual_state, _ = put_block_in_container_by_item(initial_state, target, container)
        expected_state = {'objects': ['green block', 'white block', 'red block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 
                            'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                            'disinfector': {'contains': ['blue block']}, 
                            'table': [['white block'], ['green block']], 
                            'green block': ['dirty'], 
                            'black block': ['dirty'], 
                            'blue block': ['clean'], 
                            'red block': ['dirty'], 
                            'transparent bowl': {'contains': ['red block', 'black block']}, 
                            'white block': ['clean']}
        self.assertEqual(expected_state, actual_state)
    def test_put_block_in_container(self):
        # move object from disinfector to transparent bowl 
        initial_state = {'objects': ['green block', 'white block', 'red block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 
                          'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                          'disinfector': {'contains': ['blue block']}, 
                          'table': [['\"black block\" is under \"green block\"'], ['white block']], 
                          'green block': ['dirty'], 
                          'black block': ['dirty'], 
                          'blue block' : ["clean"], 
                          'red block' : ["dirty"],
                          'transparent bowl': {'contains': ['red block']}, 
                          'white block': ['clean']}
        target = "blue block"
        container = "transparent bowl"
        actual_state = put_block_in_container(initial_state, [container, target])
        expected_state = {'user_query': 'Put the blue block in the transparent bowl', 
                          'gold_code': 'put_first_on_second("blue block", "transparent bowl")', 
                          'gold_next_state': '\n    # world_state = {\n    #    \'objects\': [\'green block\', \'white block\', \'red block\', \'black block\', \'blue block\', \'transparent bowl\', \'table\', \'disinfector\'],\n    #    \'containers\': [\'transparent bowl\', \'disinfector\', \'purple bowl\'],\n    #    \'disinfector\': {\'contains\': []},\n    #    \'table\': [[\'"black block" is under "green block"\'], [\'white block\']],\n    #    \'green block\': [\'dirty\'],\n    #    \'black block\': [\'dirty\'],\n    #    \'blue block\': [\'clean\'],\n    #    \'red block\': [\'dirty\'],\n    #    \'transparent bowl\': {\'contains\': [\'red block\', \'blue block\']},\n    #    \'white block\': [\'clean\'],\n    # }\n'}
        self.assertEqual(expected_state, actual_state)
        # move object from table to transparent bowl 
        initial_state = {'objects': ['green block', 'white block', 'red block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 
                          'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                          'disinfector': {'contains': ['blue block']}, 
                          'table': [['\"black block\" is under \"green block\"'], ['white block']], 
                          'green block': ['dirty'], 
                          'black block': ['dirty'], 
                          'blue block' : ["clean"], 
                          'red block' : ["dirty"],
                          'transparent bowl': {'contains': ['red block']}, 
                          'white block': ['clean']}
        target = "black block"
        container = "transparent bowl"
        actual_state = put_block_in_container(initial_state, [container, target])
        expected_state = {'user_query': 'Put the black block in the transparent bowl', 
                          'gold_code': 'place_pos_10 = parse_position("10cm to the right of transparent bowl"),\nput_first_on_second("green block", place_pos_10),\nput_first_on_second("black block", "transparent bowl")', 
                          'gold_next_state': "\n    # world_state = {\n    #    'objects': ['green block', 'white block', 'red block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'],\n    #    'containers': ['transparent bowl', 'disinfector', 'purple bowl'],\n    #    'disinfector': {'contains': ['blue block']},\n    #    'table': [['white block'], ['green block']],\n    #    'green block': ['dirty'],\n    #    'black block': ['dirty'],\n    #    'blue block': ['clean'],\n    #    'red block': ['dirty'],\n    #    'transparent bowl': {'contains': ['red block', 'black block']},\n    #    'white block': ['clean'],\n    # }\n"}
        self.assertEqual(expected_state, actual_state)
    def test_get_dirty_blocks(self):
        initial_state = {'objects': ['green block', 'white block', 'red block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 
                    'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                    'disinfector': {'contains': ['blue block']}, 
                    'table': [['black block'], ['white block']], 
                    'green block': ['dirty'], 
                    'black block': ['dirty'], 
                    'transparent bowl': {'contains': ['red block']}, 
                    'white block': ['dirty']}
        actual_block_list = get_dirty_blocks(initial_state)
        expected_block_list = ['green block', 'black block', 'white block']
        self.assertEqual(expected_block_list,actual_block_list)
    def test_add_to_table(self):
        initial_state = {'objects': ['green block', 'white block', 'red block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 
                        'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                        'disinfector': {'contains': ['blue block']}, 
                        'table': [['black block'], ['white block']], 
                        'green block': ['dirty'], 
                        'black block': ['dirty'], 
                        'transparent bowl': {'contains': ['red block']}, 
                        'white block': ['dirty']}
        target = "blue block"
        actual_state, _ = add_to_table(initial_state, target)
        expected_state = {'objects': ['green block', 'white block', 'red block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 
                        'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                        'disinfector': {'contains': []}, 
                        'table': [['black block'], ['white block'],['blue block']], 
                        'green block': ['dirty'], 
                        'black block': ['dirty'], 
                        'transparent bowl': {'contains': ['red block']}, 
                        'white block': ['dirty']}
        self.assertEqual(expected_state, actual_state)
        
        initial_state = {'objects': ['green block', 'white block', 'red block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 
                        'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                        'disinfector': {'contains': ['blue block', 'green block']}, 
                        'table': [], 
                        'green block': ['clean'], 
                        'black block': ['dirty'], 
                        'blue block': ['clean'],
                        'red block': ['dirty'], 
                        'transparent bowl': {'contains': ['white block', 'black block', 'red block']}, 
                        'white block': ['dirty']} 
        target = "black block"
        actual_state, _ = add_to_table(initial_state, target)
        # print(actual_state)

    def test_put_all_dirty_on_table(self):
        initial_state = {'objects': ['green block', 'white block', 'red block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 
                        'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 
                        'disinfector': {'contains': ['blue block', 'green block']}, 
                        'table': [], 
                        'green block': ['clean'], 
                        'black block': ['dirty'], 
                        'blue block': ['clean'],
                        'red block': ['dirty'], 
                        'transparent bowl': {'contains': ['white block', 'black block', 'red block']}, 
                        'white block': ['dirty']} 
        actual_state = put_all_dirty_on_table(initial_state)
        expected_state = {'objects': ['green block', 'white block', 'red block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 'containers': ['transparent bowl', 'disinfector', 'purple bowl'], 'disinfector': {'contains': ['blue block', 'green block']}, 'table': [['black block'], ['red block'], ['white block']], 'green block': ['clean'], 'black block': ['dirty'], 'blue block': ['clean'], 'red block': ['dirty'], 'white block': ['dirty']}
        self.assertEqual(expected_state, actual_state)

if __name__ == '__main__':
    unittest.main()


