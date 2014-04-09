#!/bin/bash
for TIF in $(ls *P?.tif)
do
  echo $TIF
  OUT=${TIF/.tif/.grid.jpg}
  if [ ! -e $OUT ]; then
    $HOME/git/wellscan/plate-to-well.py $TIF
  else
    echo "SKIP "$TIF
  fi
done
