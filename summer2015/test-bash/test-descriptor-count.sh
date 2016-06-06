#!/usr/bin/env sh


while (true) do

  date | tee -a fd-count
  ls -l /proc/31489/fd/ | wc -l | tee -a fd-count
  sleep 1

done
