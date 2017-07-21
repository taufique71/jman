#!/bin/bash
sleep_time=6s
for (( i=60; i<=69; i++ ))
do
    echo $i >> out.txt
    sleep $sleep_time
done
