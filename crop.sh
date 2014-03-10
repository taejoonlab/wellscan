#!/bin/bash
for TIF in $(ls *-??.tif)
do
  echo $TIF
  P1=${TIF/.tif/.P1.tif}
  P2=${TIF/.tif/.P2.tif}
  P3=${TIF/.tif/.P3.tif}
  if [ ! -e $P1 ]; then
  convert $TIF -crop 12432x8150+0+0 -compress lzw $P1
  convert $TIF -crop 12432x8150+0+8050 -compress lzw $P2
  convert $TIF -crop 12432x8150+0+16100 -compress lzw $P3
  fi
done
