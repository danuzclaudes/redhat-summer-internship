
#!/usr/bin/env sh
set -euo pipefail

katello-service stop
katello-backup /root/backup-after-fresh-build/
rpm -qa | grep pulp
cd /etc/yum.repos.d

# Upgrade to 2.9-stable:
# wget https://repos.fedorapeople.org/repos/pulp/pulp/rhel-pulp.repo
# yum install -y http://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm

# Upgrade to 2.8-z:
# Currently stable is 2.8.5, beta is 2.8.6 and nightly is 2.8.6. 
yum-config-manager --add-repo https://repos.fedorapeople.org/pulp/pulp/beta/2.8/7Server/x86_64/
yum repolist enabled | grep pulp

yum update -y pulp-*
rpm -qa | grep pulp

katello-service restart

sudo -u apache pulp-manage-db

easy_install pip
pip install httpie
http https://$HOSTNAME/pulp/api/v2/status/

UPDATE_PULP_VERSOIN=`http https://$HOSTNAME/pulp/api/v2/status/`
UPDATE_PULP_VERSOIN=${UPDATE_PULP_VERSOIN%\"*}
UPDATE_PULP_VERSION=${UPDATE_PULP_VERSOIN##*\ \"} 
echo "Current version of Pulp is: $UPDATE_PULP_VERSION."
