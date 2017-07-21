#!/bin/bash
sleep_time=2s
for (( i=20; i<=29; i++ ))
do
    echo $i >> out.txt
    sleep $sleep_time
done
