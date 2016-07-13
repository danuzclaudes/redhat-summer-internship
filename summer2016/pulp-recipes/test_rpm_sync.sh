#!/usr/bin/env bash
#
# Attempt to trigger https://github.com/PulpQE/pulp-smash/issues/243.
#

pulp-admin rpm repo create --repo-id repo1 --feed https://repos.fedorapeople.org/repos/pulp/pulp/fixtures/rpm/
pulp-admin rpm repo sync run --repo-id repo1
pulp-admin rpm repo content rpm --str-eq "name=penguin" --repo-id repo1
pulp-admin rpm repo remove rpm --repo-id repo1 --str-eq "name=penguin"
pulp-admin rpm repo sync run --repo-id repo1
pulp-admin rpm repo content rpm --str-eq "name=penguin" --repo-id repo1
# Verify that the deleted package should have returned.
