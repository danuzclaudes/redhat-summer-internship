#!/bin/sh
cd ~

# overwrite all historic timing logs
echo "Begin reset and upload:" | tee timing-reset timing-upload

for attempt in `seq 0 1`; do

  echo "Attempt: ${attempt}" | tee -a timing-reset # need to both write to file and on screen
  echo "timing reset db:" | tee -a timing-reset
  (time ./reset-db.sh /home/backup/20150520-clean) >> timing-reset 2>&1 # only write to file

  # Display subscriptions before hand
  hammer -u admin -p changeme subscription list --organization-id 1 | tee -a timing-upload

  #echo "downloading manifest:" >> timing-upload 2>&1
  #wget http://perf1.perf.lab.eng.bos.redhat.com/akrzos/satellite6/manifests/omaciel-manifest.zip

  echo "timing uplaod manifest:" | tee -a timing-upload
  (time hammer -u admin -p changeme subscription upload --file /root/omaciel-manifest.zip --organization-id 1) >> timing-upload 2>&1
  # Display subscriptions after
  hammer -u admin -p changeme subscription list --organization-id 1 | tee -a timing-upload
  echo "reset db and upload process done" | tee -a timing-upload
done

echo "repository list is empty:"
h repository list --organization-id 1
echo "NOTE: should enable repositories on web GUI"
