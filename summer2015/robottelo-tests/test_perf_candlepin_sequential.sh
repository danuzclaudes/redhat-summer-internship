#!/bin/bash

if [ ! $# == 1 ]; then
   echo "Usage: ./test_perf_candlepin_sequential.sh <subscription method>"
   echo "Choose the approach that you want vm to register to satellite server:"
   echo "0 - time register by activation key only"
   echo "1 - time register by attach only"
   echo "2 - time both methods"
else
   export OPTION=$1
   echo "You choose method $OPTION:"

   if [ $OPTION == 0 ]; then 
      echo "Start timing candlepin subscription by activation key."
      python test_perf_candlepin_standup.py
      python test_perf_candlepin_ak.py

   elif [ $OPTION == 1 ]; then
      echo "Start timing candlepin subscription by attach."
      python test_perf_candlepin_attach.py

   else
      echo "Start timing candlepin on both ways sequentially."
      python test_perf_candlepin_standup.py
      python test_perf_candlepin_ak.py 
      sleep 10 
      python test_perf_candlepin_attach.py

   fi
fi

