#!/usr/bin/env bash

for file in ./ben_disinfection_prompt_*.py; do
    echo $file
    if [[ -f $file ]]; then
        sed -i 's/\r//g' $file
        sed -i '/parse_position/d' $file
        sed -i 's/place_pos/"table"/g' $file
        sed -i 's/world_state/state/g' $file
    fi
done
