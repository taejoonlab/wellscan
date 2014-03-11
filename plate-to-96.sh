#!/bin/bash
for TIF in $(ls *P?.tif)
do
  echo $TIF
  GRID=${TIF/.tif/.grid.jpg}
  if [ ! -e $GRID ]; then
    $HOME/git/wellscan/plate-to-96.py $TIF
  else
    echo "SKIP "$TIF
  fi
done
