#!/bin/bash
DATA_NAME=$1

if [ ! $DATA_NAME ]; then
  echo "Usage: rename-Scan.sh <data_name>"
  exit
fi

for TIF in $(ls Scan*.tif)
do
  DATE=$(stat --format="%y" $TIF | awk '{print $1}')
  TIME=$(stat --format="%y" $TIF | awk '{print $2}' | awk -F"." '{print $1}')
  TIME=${TIME//:/-}
  NEW_NAME=$DATA_NAME"_"$DATE"_"$TIME".tif"
  if [ -e $NEW_NAME ]; then
    echo "SKIP. "$TIF"-->"$NEW_NAME
  else
    echo $TIF" --> "$NEW_NAME
    mv $TIF $NEW_NAME
  fi
done
