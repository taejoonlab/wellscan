#!/bin/bash
for COL in A B C D E F G H
do
  for ROW in 01 02 03 04 05 06 07 08 09 10 11 12
  do
    ADDRESS=$COL$ROW
    echo $ADDRESS
    cd $ADDRESS
    $HOME/git/wellscan/make-movie.sh
    cd ../
  done
done
