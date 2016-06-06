#!/bin/bash
timingsfile=$1

product[0]=gen1
product[1]=gen2
product[2]=gen3
product[3]=gen4
product[4]=gen5
product[5]=gen6
product[6]=gen7
product[7]=gen8

echo "[$(date -R)] Outputing to ${timingsfile}"
for proid in 0 1 2 3 4 5 6 7 
do
  for fsize in 0256KiB 0512KiB 1024KiB
  do
    #for fnum in 00032 00064 00128 00256 00512 01024 02048 08192
    for fnum in 00032 00064 00128 00256 00512 01024 02048
    do
      actual_productid=`expr ${proid} + 1`
      echo "[$(date -R)] Adding Repo: content/${product[$proid]}/gen-${fnum}-${fsize}" | tee -a ${timingsfile}
      #echo "[$(date -R)] Product ID: ${actual_productid}" | tee -a ${timingsfile}
      (time hammer -u admin -p changeme repository create --organization-id 1 --product-id ${actual_productid} --content-type yum --name ${product[${proid}]}-${fnum}-${fsize} --url http://perfc-380g8-02.perf.lab.eng.rdu.redhat.com/pub/content/${product[${proid}]}/gen-${fnum}-${fsize}/) >> ${timingsfile} 2>&1
    done
  done
done
