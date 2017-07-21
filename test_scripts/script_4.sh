#!/bin/bash
sleep_time=4s
for (( i=40; i<=49; i++ ))
do
    echo $i >> out.txt
    sleep $sleep_time
done
