#!/bin/bash
sleep_time=7s
for (( i=70; i<=79; i++ ))
do
    echo $i >> out.txt
    sleep $sleep_time
done
