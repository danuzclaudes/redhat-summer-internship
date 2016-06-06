#!/usr/bin/env sh
su postgres -c 'psql -A -t -d foreman -c "SELECT uuid FROM katello_systems;"' > uuids; wc -l uuids
