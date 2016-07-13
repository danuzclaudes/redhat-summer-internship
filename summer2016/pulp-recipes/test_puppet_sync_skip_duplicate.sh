#!/usr/bin/env sh
#
# Attempt to trigger https://github.com/PulpQE/pulp-smash/issues/269.
#
set -euo pipefail

pulp-admin puppet repo create --repo-id repo1 --feed http://forge.puppetlabs.com --queries torssh
pulp-admin puppet repo sync run --repo-id repo1
pulp-admin puppet repo create --repo-id repo2 --feed http://forge.puppetlabs.com --queries torssh
pulp-admin puppet repo sync run --repo-id repo2
pulp-admin puppet repo list --repo-id repo1
pulp-admin puppet repo list --repo-id repo2
pulp-admin puppet repo list --repo-id repo1 --fields content_unit_counts
pulp-admin puppet repo list --repo-id repo2 --fields content_unit_counts
pulp-admin puppet repo delete --repo-id repo1
pulp-admin puppet repo delete --repo-id repo2
