#!/bin/bash

#export PYTHONPATH="/home1/00992/linusben/local/lib64/python2.6/site-packages/"

for TIF in $(ls *.tif)
do
  echo $TIF
  OUT=${TIF/.tif/.grid.jpg}
  if [ ! -e $OUT ]; then
    $HOME/git/wellscan/plate-to-well.py $TIF
  else
    echo "SKIP "$TIF
  fi
done
