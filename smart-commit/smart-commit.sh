#!/bin/bash

paths=$(git status --porcelain | grep '^.[MADRC]' | sed 's/^...//' | tr '\n' ' ')
add=$(git add $paths)

#without folder:
#last_updated_file=($paths)
#last_modified_file=$(echo $last_updated_file | sed 's|^smart-commit/||')
#add=$(git add "$last_modified_file")
