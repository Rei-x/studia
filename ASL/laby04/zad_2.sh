#!/bin/bash

directory=$1

for file in "$directory"/*; do
    if [[ $file =~ \.(html|htm|php|css|gif|jpg)$ ]]; then
        echo $(basename "$file")
    fi
done