#!/bin/sh
while true; do
    curl -k -s -A "DDoS-Test-Agent" https://apache/ > /dev/null &
    sleep 0.5
done
