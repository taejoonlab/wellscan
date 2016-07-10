#!/bin/bash
for COL in A B C D E F G H
do
  for ROW in 01 02 03 04 05 06 07 08 09 10 11 12
  do
    ADDRESS=$COL$ROW
    if [ -d $ADDRESS ]; then
      TAR_NAME=$(basename $PWD)"."$ADDRESS".tar"
      if [ ! -e $TAR_NAME ]; then
        echo $TAR_NAME
        tar cvf $TAR_NAME $ADDRESS
      fi
    fi
  done
done

ADDRESS='grid'
if [ -d $ADDRESS ]; then
  TAR_NAME=$(basename $PWD)"."$ADDRESS".tar"
  if [ ! -e $TAR_NAME ]; then
    echo $TAR_NAME
    tar cvf $TAR_NAME $ADDRESS
  fi
fi
