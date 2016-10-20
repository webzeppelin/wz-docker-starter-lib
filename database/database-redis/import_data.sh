#!/bin/bash
while read -r line
do
    printf "%b" "$line"| redis-cli -p 6379 --pipe
done < $1
