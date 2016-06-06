#!/bin/bash

#reset db
# ./reset-db.sh /home/backup/20150603-savepoint2-repos-enabled-not-sync

toolinterval=2
iter="001"
testname="vtopt-r6-resync-0"

register-tool --name=vmstat --group sat6 -- --interval ${toolinterval}
register-tool --name=mpstat --group sat6 -- --interval ${toolinterval}
register-tool --name=iostat --group sat6 -- --interval ${toolinterval}
register-tool --name=pidstat --group sat6 -- --interval ${toolinterval}
register-tool --name=sar --group sat6 -- --interval ${toolinterval}

sync; sync; echo 3 > /proc/sys/vm/drop_caches

mkdir -p /var/lib/pbench/${testname}/${iter}
start-tools --group=sat6 --dir=/var/lib/pbench/${testname}/${iter} --iteration=${iter}
sleep 6

# hammer command here
# time sleep 20
time hammer -u admin -p changeme repository synchronize --id 3

sleep 6
stop-tools --group=sat6 --dir=/var/lib/pbench/${testname}/${iter} --iteration=${iter}

postprocess-tools  --group=sat6 --dir=/var/lib/pbench/${testname}/${iter} --iteration=${iter}

move-results




