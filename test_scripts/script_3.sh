#!/bin/bash
sleep_time=3s
for (( i=30; i<=39; i++ ))
do
    echo $i >> out.txt
    sleep $sleep_time
done
