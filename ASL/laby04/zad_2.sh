#!/bin/bash

directory=$1

for file in "$directory"/*; do
    if [[ $file =~ \.(html|htm|php|css|gif|jpg)$ ]]; then
        basename "$file"
    fi
done
