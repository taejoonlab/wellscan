#!/bin/bash
DEST=$1

for PREFIX in $(ls *tif | awk -F"_" '{print $1"_"$2}' | sort -u)
do
  FILENAME=$(ls $PREFIX* | head -n 1)
  echo $FILENAME
  cp $FILENAME $DEST
done
