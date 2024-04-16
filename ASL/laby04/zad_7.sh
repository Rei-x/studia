#!/bin/bash

i=1
while [ $i -le 10 ]; do
    echo $i
    ((i++))
done

j=1
until [ $j -gt 10 ]; do
    echo $j
    ((j++))
done
