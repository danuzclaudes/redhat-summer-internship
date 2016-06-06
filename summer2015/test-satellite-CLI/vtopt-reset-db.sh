#!/bin/sh
# author: akrzos
if [ ! $# == 1 ]; then
  echo "Usage: ./reset-db.sh <backup-directory>"
  echo "Backup Directories available: " `ls /home/backup`
  echo "Example: ./reset-db.sh /home/backup/clean"
  exit
fi
export BDIR=$1
echo "Restoring from: $BDIR"

# Restore from backup
cd $BDIR

katello-service stop
service tomcat stop
service postgresql stop
service foreman-proxy stop

sync; sync; echo 3 > /proc/sys/vm/drop_caches

service postgresql start
su postgres -c "dropdb foreman"
su postgres -c "dropdb candlepin"
su postgres -c "dropdb gutterball"
su postgres -c "pg_restore -C -d postgres $BDIR/foreman.dump"
su postgres -c "pg_restore -C -d postgres $BDIR/candlepin.dump"
su postgres -c "pg_restore -C -d postgres $BDIR/gutterball.dump"

# Delete synced folder:
rm -rf /var/lib/pulp/*

# Copy synced content back in
tar --selinux -xf pulp_data.tar -C /

# Delete old manifests/cached data
rm -rf /var/cache/tomcat6/temp/*
rm -rf /var/run/foreman/import_*
rm -rf /var/run/foreman/cache/*

service mongod start
sleep 10
echo 'db.dropDatabase();' | mongo pulp_database
mongorestore --host localhost mongo_dump/pulp_database/

service foreman-proxy start
service tomcat start
katello-service start
cd ~
hammer -u admin -p 333666 ping
foreman-rake katello:reindex
sleep 5

