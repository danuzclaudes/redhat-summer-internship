#!/bin/sh
# note: must execute the script line by line on console!
export BDIR=/home/backup/20150603-savepoint2-repos-enabled-not-sync
mkdir -p $BDIR
chmod 770 $BDIR
chgrp postgres $BDIR
cd $BDIR
katello-service stop
service foreman-proxy stop
sync; sync; echo 3 > /proc/sys/vm/drop_caches
tar --selinux -cvf pulp_data.tar /var/lib/pulp /var/www/pub
service mongod start
sleep 5
mongodump --host localhost --out $BDIR/mongo_dump
service mongod stop
service postgresql stop
sync; sync; echo 3 > /proc/sys/vm/drop_caches
service postgresql start
su postgres -c "pg_dump -Fc candlepin > $BDIR/candlepin.dump"
su postgres -c "pg_dump -Fc foreman > $BDIR/foreman.dump"
su postgres -c "pg_dump -Fc gutterball > $BDIR/gutterball.dump"
df -h >> $BDIR/df-h
df >> $BDIR/df
service foreman-proxy start
katello-service start
cd ~
hammer -u admin -p changeme ping

