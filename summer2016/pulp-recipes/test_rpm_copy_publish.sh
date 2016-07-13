#!/usr/bin/bash

yum clean all; pclean; clear

# Create repo and sync.
pulp-admin rpm repo create --repo-id repo1 --feed https://repos.fedorapeople.org/repos/pulp/pulp/fixtures/rpm/

pulp-admin rpm repo sync run --repo-id repo1

# Find the RPM that has two different versions in the repo.
pulp-admin rpm repo content rpm --repo-id repo1 --str-eq="name=walrus"

# Create a new repo2 and copy older of rpm version into it.
pulp-admin rpm repo create --repo-id repo2 --serve-http=true --serve-https=true

# Get a list of dependency packages of repo1
pulp-admin rpm repo content rpm --repo-id repo1 --str-eq=name=walrus --fields=version,requires
# Install dependency packages.
pulp-admin rpm repo copy rpm --from-repo-id repo1 --to-repo-id repo2 --str-eq="name=whale"
pulp-admin rpm repo copy rpm --from-repo-id repo1 --to-repo-id repo2 --str-eq="name=stork"
pulp-admin rpm repo copy rpm --from-repo-id repo1 --to-repo-id repo2 --str-eq="name=shark"
pulp-admin rpm repo copy rpm --from-repo-id repo1 --to-repo-id repo2 --str-eq="name=walrus" --str-eq="version=0.71"

# Verify the copy succeeded
pulp-admin rpm repo content rpm --repo-id repo2

# Setup the repo2 on a host and publish repo2.

pulp-admin rpm repo publish run --repo-id repo2
# Verify that no errors
# http://pulp.readthedocs.io/en/latest/user-guide/deferred-download.html
http https://dev/pulp/repos/repo2/


# Install the packages.
# yum clean all
# sudo yum-config-manager --add-repo <repo-url>
sudo yum-config-manager --add-repo https://dev/pulp/repos/repo2/

# ll /etc/yum.repos.d
yum repolist enabled
yum --disablerepo=* --enablerepo=dev_pulp_repos_repo2_ list available
sudo yum install -y --nogpgcheck walrus

# Copy a newer version into the repo2 and re-publish.
pulp-admin rpm repo copy rpm --from-repo-id repo1 --to-repo-id repo2 --str-eq="name=walrus" --str-eq="version=5.21"
pulp-admin rpm repo publish run --repo-id repo2
phttp https://dev/pulp/repos/repo2/

# Use same client to install packages both times.
sudo yum update --nogpgcheck walrus

sudo yum remove -y walrus
sudo rm /etc/yum.repos.d/dev_pulp_repos_repo2_.repo


# pulp-admin rpm repo delete --repo-id repo1
# pulp-admin rpm repo delete --repo-id repo2

