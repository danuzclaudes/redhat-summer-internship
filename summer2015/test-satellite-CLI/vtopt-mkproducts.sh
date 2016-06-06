#!/bin/bash
timingsfile=$1

echo "[$(date -R)] Outputing to ${timingsfile}"
for product in perf-gen1 perf-gen2 perf-gen3 perf-gen4 perf-gen5 perf-gen6 perf-gen7 perf-gen8
do
  echo "[$(date -R)] Adding Product: ${product}" | tee -a ${timingsfile}
  (time hammer -u admin -p changeme product create --organization-id 1 --name ${product}) >> ${timingsfile} 2>&1
done
