#!/bin/sh
cd ~

echo "Time sub-mgr by register and attach:" | tee timing-reg

for attempt in `seq 0 999`; do

  # 20 rounds of testing for register and attach way
  # record timing of register into timing-reg
  echo "Attempt: ${attempt}" | tee -a timing-reg
  echo "Timing reg and attach subscription:" | tee -a timing-reg
  subscription-manager clean
  (time subscription-manager register --username=admin --password=333666 --org="Default_Organization" --environment="Library" ) >> timing-reg 2>&1
  # record timing of attach into timing-attach
  # subscription-manager list --available
  (time subscription-manager attach --pool=8a8c94aa4d814df7014d8156fce0038d) >> timing-attach 2>&1
done

echo "Time sub-mgr by registration and activating key:" | tee timing-ak

for attempt in `seq 0 999`; do

  # 20 rounds of testing for activating key way
  # record timing of register by ak into timing ak
  echo "Attempt: ${attempt}" | tee -a timing-ak
  echo "Timing register by ak:" | tee -a timing-ak
  subscription-manager clean
  (time subscription-manager register --activationkey=ak-1 --org="Default_Organization") >> timing-ak 2>&1
done

