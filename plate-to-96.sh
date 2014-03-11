#!/bin/bash
for TIF in $(ls *P?.tif)
do
  echo $TIF
  OUT=${TIF/.tif/_96.tif}
  if [ ! -e $OUT ]; then
    ./plate-to-96.py $TIF
  else
    echo "SKIP "$TIF
  fi
done
