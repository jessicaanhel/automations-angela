#!/bin/bash

paths=$(git status --porcelain | grep '^.[MADRC]' | sed 's/^...//' | tr '\n' ' ')
last_updated_file=($paths)
#last_modified_file=$(echo $last_updated_file | sed 's|^smart-comit/||')

echo ${last_updated_file}
