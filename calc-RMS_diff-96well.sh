#!/bin/bash

export PYTHONPATH="$HOME/local/lib64/python2.6/site-packages/"

for C in 01 02 03 04 05 06 07 08 09 10 11 12
do
  for R in A B C D E F G H
  do
    POS=$R$C
    if [ -d $POS ]; then
      echo $POS
      $HOME/git/wellscan/calc-RMS_diff.py $POS
    fi
  done
done
