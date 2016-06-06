#!/bin/bash

contenthostsfile=content-hosts-uuids.txt
qpidqueuesfile=qpid-queues-uuids.txt

# run psql query against katello_systems table in foreman db and print sorted UUIDs
echo "finding content hosts UUIDs from foreman's db.."
su - postgres -c "psql -d foreman -c 'select * from katello_systems;'" | awk '{ print $3 }' | egrep -v '(^$|uuid)' | sort > $contenthostsfile

#find pulp.admin.* queues and remember just the (only relevant) UUID
echo "finding qpid queues for pulp consumers.."
ls -1 /var/lib/qpidd/qls/jrnl/ /var/lib/qpidd/.qpidd/qls/jrnl/ 2> /dev/null | grep "^pulp.agent" | cut -d'.' -f3 | sort > $qpidqueuesfile

contenthostsfilelines=$(wc -l $contenthostsfile | cut -d' ' -f1)
qpidqueuesfilelines=$(wc -l $qpidqueuesfile | cut -d' ' -f1)
echo
echo "found $contenthostsfilelines content hosts and $qpidqueuesfilelines qpid queues for pulp consumers"
echo
echo "list of content hosts: $contenthostsfile, list of qpid queues: $qpidqueuesfile"
echo "- please remove the files once you dont need them"
echo
echo "Please check above output for number of content hosts in each organization. If those numbers dont correspond to expected nubers, dont continue with script execution."
echo

echo -n "Delete $(($((qpidqueuesfilelines))-$((contenthostsfilelines)))) orphaned queues with no matching content host UUID (y/n)? "
read answer
if echo "$answer" | grep -iq "^y" ; then
    export HOSTNAMEF=$(hostname -f)
    for uuid in $(diff $contenthostsfile $qpidqueuesfile | grep "^> " | cut -d' ' -f2); do
        queue="pulp.agent.${uuid}"
        echo "deleting queue $queue"
        qpid-config --ssl-certificate /etc/pki/katello/certs/java-client.crt --ssl-key /etc/pki/katello/private/java-client.key -b "amqps://${HOSTNAMEF}:5671" del queue $queue --force
    done
fi
