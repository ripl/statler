#!/usr/bin/env python3
import importlib

from pathlib import Path
current_dir = Path(__file__).parent
import sys
sys.path.append(str(current_dir))

eval_episodes = []
for i in range(20):
    ep = importlib.import_module(f'disinfection.generated.disinfection_prompt_{i + 1:02d}')
    eval_episodes.append(ep.eval_episode)

print(f'loaded {len(eval_episodes)} episodes')

task_description = '''
In the following, the robot deals with dirty and clean blocks.
A clean block becomes dirty when it touches another dirty block.
This includes when a dirty block is stacked on top of a clean block, and also when a dirty block is right under a clean block.
The table, bowls and the robot gripper are protected from any dirtiness, so they stay clean forever.
When a dirty block is put into the disinfector, it becomes clean immediately.
Aside from the built-in python functions and statements, the robot can only run the following functions:
{list_of_functions}
Each code is carefully designed by professionals to meet all of these requirements.
'''
