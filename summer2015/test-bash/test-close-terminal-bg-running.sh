#!/usr/bin/env bash
# test if background bash script would still run
# if terminal is shut down

sleep 30
for i in `seq 1 10000`; do
    echo "${i}"
done

# even the script is running at bg,
# once close its terminal,
# the process is still killed
