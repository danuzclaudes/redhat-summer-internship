#!/usr/bin/env sh
#
# Run this script to install pulp-rpm and pulp-puppet after fresh `vagrant up`.
#
# View the log of pulp: http://paste.fedoraproject.org/374223/46498206/raw/
# sudo journalctl -f -l SYSLOG_IDENTIFIER=pulp | grep -v worker[\-,\.]heartbeat

# In case that the vagrant was closed unexpectedly
# If mongo gives you a random connection error, try 
# sudo rm /var/lib/mongodb/mongod.lock
# sudo systemctl start mongod
# sudo -u apache pulp-manage-db
# sudo systemctl start httpd

# Set up plugin directories

read -p "What is the location of plugins to be installed? [$HOME/devel] " LOCATION
if [ "$LOCATION" = "" ]; then
    LOCATION="$HOME/devel"
fi
echo "Choosing $LOCATION as your directory to install the plugins..."


# Install pulp-rpm
cd $LOCATION
sudo yum install pulp-rpm-plugins
git clone https://github.com/pulp/pulp_rpm.git
cd pulp_rpm
sudo ./manage_setup_pys.sh develop
sudo python ./pulp-dev.py -I

# Install pulp-puppet
cd $LOCATION
sudo yum install pulp-puppet-plugins
git clone https://github.com/pulp/pulp_puppet.git
cd pulp_puppet
sudo ./manage_setup_pys.sh develop
sudo python ./pulp-dev.py -I

# Must update database after installing the plugins
sudo -u apache pulp-manage-db
# That command might have some errors; then clean db and restart httpd service
pclean
sudo system ctl restart httpd

# Verify pulp-rpm by the following commands:
pulp-admin rpm repo create --repo-id zoo --relative-url zoo --feed http://repos.fedorapeople.org/repos/pulp/pulp/demo_repos/zoo/
pulp-admin rpm repo sync run --repo-id zoo
pulp-admin rpm repo delete --repo-id zoo

# Verify pulp-puppet by the following commands:
pulp-admin puppet repo list
pulp-admin puppet repo create --repo-id=repo1 --feed=http://forge.puppetlabs.com --queries=torssh
pulp-admin puppet repo sync run --repo-id=repo1
pulp-admin puppet repo delete --repo-id repo1
pulp-admin puppet repo list --repo-id repo1 --fields content_unit_counts

# The command to uninstall the plugins
# sudo python ./pulp-dev.py -U


# Install pulp-smash
cd $LOCATION
git clone https://github.com/PulpQE/pulp-smash.git
cd pulp-smash
sudo pip install -r requirements.txt -r requirements-dev.txt
python -m pulp_smash

# Set up configuration file
CONFIG_FILE="/home/vagrant/.config/pulp_smash/settings.json"
VERSION=`pulp-admin status | grep "Platform Version" | awk '{ print $3 }'`
touch $CONFIG_FILE
echo '{
    "pulp": {
        "auth": [
            "admin",
            "admin"
        ],
        "base_url": "https://dev",
        "cli_transport": "local",
        "verify": true,
        "version": "'$VERSION'"
    }
}' | python -m json.tool > $CONFIG_FILE
cat $CONFIG_FILE
python -m unittest2 discover pulp_smash.tests
