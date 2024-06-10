import unittest 
import math
from helper_functions import get_episode_dict_str, get_gold_next_state_string#, EpisodeDict, 

class GetEpisodeDictStr(unittest.TestCase):
    def test_get_episode_dict_str(self): 
        dic = {}
        dic[5] = 3
        dic[6] = "happy"
        dic["string 1"] = 5
        dic["string 2"] = "string 3"
        
        # verify that dic can store different types 
        self.assertEqual(3, dic[5])
        self.assertEqual("happy", dic[6])
        self.assertEqual(5, dic["string 1"])
        self.assertEqual("string 3", dic["string 2"])

        actual_dic_str = get_episode_dict_str(dic)
        # print(actual_dic_str)
        
        expected_dic_str = '{5: 3, \n6: \'\'\'happy\'\'\', \n\'string 1\': 5, \n\'string 2\': \'\'\'string 3\'\'\'}'
        self.assertEqual(expected_dic_str, actual_dic_str)

class TestGetGoldNextStateString(unittest.TestCase):
    def test_get_gold_next_state_string(self):
        state = {'objects': ['green block', 'white block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'], 
                 'containers': ['transparent bowl', 'disinfector'], 
                 'disinfector': {'contains': []}, 
                 'green block': ['dirty'], 
                 'table': [['green block'], ['white block']], 
                 'white block': ['dirty'], 
                 'black block': ['dirty'], 
                 'transparent bowl': {'contains': ['black block']}}
        actual_gns_string = repr(get_gold_next_state_string(state))
        expected_gns_string = repr("\n    # world_state = {\n    #    'objects': ['green block', 'white block', 'black block', 'blue block', 'transparent bowl', 'table', 'disinfector'],\n    #    'containers': ['transparent bowl', 'disinfector'],\n    #    'disinfector': {'contains': []},\n    #    'green block': ['dirty'],\n    #    'table': [['green block'], ['white block']],\n    #    'white block': ['dirty'],\n    #    'black block': ['dirty'],\n    #    'transparent bowl': {'contains': ['black block']},\n    # }\n")
        self.assertEqual(expected_gns_string, actual_gns_string)

if __name__ == '__main__':
    unittest.main()




