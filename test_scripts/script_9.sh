#!/bin/bash
sleep_time=9s
for (( i=90; i<=99; i++ ))
do
    echo $i >> out.txt
    sleep $sleep_time
done
