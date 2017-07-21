#!/bin/bash
sleep_time=5s
for (( i=50; i<=59; i++ ))
do
    echo $i >> out.txt
    sleep $sleep_time
done
