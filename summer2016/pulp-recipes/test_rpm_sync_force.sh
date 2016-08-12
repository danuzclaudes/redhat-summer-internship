#!/usr/bin/env bash
#
# Attempt to trigger https://github.com/PulpQE/pulp-smash/issues/301
#

pulp-admin rpm repo create --repo-id repo1 --feed https://repos.fedorapeople.org/repos/pulp/pulp/fixtures/rpm/

pulp-admin rpm repo sync run --repo-id repo1

# Verify number of units in the directory.
ll /var/lib/pulp/content/units/rpm/ | wc -l

# Remove a unit
sudo rm -rf /var/lib/pulp/content/units/rpm/$(ls /var/lib/pulp/content/units/rpm/ | head -1)

pulp-admin rpm repo sync run --force-full --repo-id repo1

ll /var/lib/pulp/content/units/rpm/ | wc -l
