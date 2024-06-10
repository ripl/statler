# Statler: State-Maintaining Language Models for Embodied Reasoning

[Takuma Yoneda*](https://takuma.yoneda.xyz), [Jiading Fang*](https://sites.google.com/view/jiadingfang), [Peng Li*](https://artpli.github.io/), [Huanyu Zhang*](),  
[Tianchong Jiang](), [Shengjie Lin](), [Ben Picker](), [David Yunis](), [Hongyuan Mei](https://www.hongyuanmei.com/), [Matthew R. Walter](https://ttic.edu/walter)

[[Paper]](https://arxiv.org/abs/2306.17840) [[Website]](https://statler-lm.github.io/)

<img width="1091" alt="statler_teaser" src="https://github.com/ripl/statler/assets/28857806/9e9d5670-c93a-4102-886b-6bc131c8a839">

## Set up your environment

``` sh
$ pip install -e .
```
If things fail, you can look at `pyproject.toml` to find dependencies. (If you use pdm, you should be able to just run `pdm install`)

## What you can play with
**Running a minimal demo**
``` sh
$ python -m cap.minimal_demo
```
This runs Statler on a simple environment with covers and objects.

**Running models on evaluation episodes**
``` sh
$ python -m cap.experiments.evaluate_models disinfection --agents baseline
```

This runs baseline agent on each episode in disinfection domain, and save the results to
- `results/{task_name}/baseline-episode{ep_idx}.txt`


## Directories
- `cap/experiments/prompts`
  - In-context learning prompt for each domain (`pick_and_place`, `disinfection`, `weight`, `real_robot`)
  - There are 3 prompts for each domain
    - `cap_baseline`: used by the baseline CaP agent
    - `cap_wm_reader`: used by Statler, *world state reader*
    - `cap_wm_updater`: used by Statler, *world state writer*
  - `cap_auto_*` is for Statler-Auto

- `cap/experiments/eval_prompts`
  - User queries and expected code for each domain, used in our evaluation
  - Please disregard "gold_next_state" entry

- `results-reference`
  - generated code / state during evaluation for each domain


## Disclaimer
Some of the code here were used to run real robot experiments, which contains a lot of low-level functions (for example, to identify the bounding box as well as orientation of an object from its pointcloud).
Although it's difficult for us to provide a clean and complete code repository that works for other UR5s out-of-the box, we leave them here in case they're helpful.

---
If you find our work useful in your research, please consider citing the paper as follows:
``` bibtex
@inproceedings{yoneda2024statler,
  title={Statler: State-Maintaining Language Models for Embodied Reasoning}, 
  author={Takuma Yoneda and Jiading Fang and Peng Li and Huanyu Zhang and 
  Tianchong Jiang and Shengjie Lin and Ben Picker and David Yunis and Hongyuan Mei and Matthew R. Walter},
  booktitle={Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)},
  year={2024},
}
```
