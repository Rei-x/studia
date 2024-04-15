#!/bin/bash

folder=$1

for file in "$folder"/*; do
    if [[ $file =~ \.(html|htm|php|css|gif|jpg)$ ]]; then
        echo $(basename "$file")
    fi
done