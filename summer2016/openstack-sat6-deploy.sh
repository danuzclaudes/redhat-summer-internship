#!/bin/bash
set +e
# http://docs.openstack.org/user-guide/cli_cheat_sheet.html
#
# The script aims to prepare OpenStack Environment and create a new RHEL 7.2 instance.
# Prerequisite: must have a valid OS account;
#   must have OS RC File downloaded at current directory.

. bin/activate
sudo yum install redhat-rpm-config -y
sudo yum install python-devel -y

rm -f requirements.txt
wget https://raw.githubusercontent.com/SatelliteQE/5minute/master/requirements.txt
pip install -r requirements.txt

# Download Openstack RC file. It lets you generate files that you can source in your shell to populate the environment variables. The command-line tools require to know where your service endpoints and your authentication information are
if [ ! -f ./US.ENG\ Perf\ R\&D-openrc.sh ]; then
    echo "Error: OpenStack RC file not found!"
    return
fi
cp $PWD/US.ENG\ Perf\ R\&D-openrc.sh config
. config
# Enter OpenStack password
echo "OpenStack account verified!"

KEY_NAME=pulp-jenkins
IMAGE_ID=`glance image-list | grep '| rhel-guest-image-7.2' | awk '{ print $2 }'`
INSTANCE_NAME=$KEY_NAME-sat6-tester

echo "Uploading the public key..."
rm $KEY_NAME*
ssh-keygen -t rsa -f $KEY_NAME -N ""
if [[ -z `nova keypair-list | grep $KEY_NAME | awk '{ print $2 }'` ]]; then
    nova keypair-add --pub-key $KEY_NAME.pub $KEY_NAME
fi

echo "Setup firewall rules"
SECURITY_GROUP_NAME=pulp-jenkins
SECURITY_GROUP_DESC="Security group for Satellite6-Pulp testing"

if [[ -z `nova secgroup-list | grep $SECURITY_GROUP_NAME` ]]; then
    nova secgroup-create $SECURITY_GROUP_NAME "$SECURITY_GROUP_DESC"
fi
nova secgroup-list
if [[ -z `nova secgroup-list-rules $SECURITY_GROUP_NAME | grep "0.0.0.0/0"` ]]; then
    nova secgroup-add-rule $SECURITY_GROUP_NAME icmp -1 -1 0.0.0.0/0
    for tcp_port in 22 80 443 5000 5646 5647 5671 8000 8140 8443 9090; do
        nova secgroup-add-rule $SECURITY_GROUP_NAME tcp $tcp_port $tcp_port 0.0.0.0/0
    done
    for udp_port in 53 69; do
        nova secgroup-add-rule $SECURITY_GROUP_NAME udp $udp_port $udp_port 0.0.0.0/0
    done
fi
nova secgroup-list-rules $SECURITY_GROUP_NAME

nova boot --flavor 'c3.xlarge' \
    --image $IMAGE_ID \
    --key-name $KEY_NAME \
    --security-groups $SECURITY_GROUP_NAME \
    $INSTANCE_NAME

INSTANCE_IP=
while [[ -z "${INSTANCE_IP}" ]]; do
    echo "The network is not yet ready..."
    sleep 1
    INSTANCE_IP=`nova list | grep $INSTANCE_NAME | awk {' print $13 '} | head -1`
done
echo "The network is ready! The floating-IP of this instance is: $INSTANCE_IP"

INSTANCE_ID=`nova list | grep $INSTANCE_NAME | awk {' print $2 '} | head -1`

nova delete $INSTANCE_ID
sleep 15
nova secgroup-delete $SECURITY_GROUP_NAME

