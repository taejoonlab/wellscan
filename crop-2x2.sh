#!/bin/bash
WIDTH=8100
HEIGHT=12000
X1=250
Y1=2100
X2=8200
Y2=14500

for TIF in $(ls *-??.tif)
do
  echo $TIF
  P1=${TIF/.tif/.M01_P1.tif}
  P2=${TIF/.tif/.M01_P2.tif}
  P3=${TIF/.tif/.M01_P3.tif}
  P4=${TIF/.tif/.M01_P4.tif}
  THERMO=${TIF/.tif/.thermo.tif}
  HUMID=${TIF/.tif/.humid.tif}

  if [ ! -e $P1 ]; then
  convert $TIF -crop $WIDTH"x"$HEIGHT"+"$X1"+"$Y1 -compress lzw $P1
  convert $TIF -crop $WIDTH"x"$HEIGHT"+"$X2"+"$Y1 -compress lzw $P2
  convert $TIF -crop $WIDTH"x"$HEIGHT"+"$X1"+"$Y2 -compress lzw $P3
  convert $TIF -crop $WIDTH"x"$HEIGHT"+"$X2"+"$Y2 -compress lzw $P4
  convert $TIF -crop 1080x4200+16100+12000 -compress lzw $THERMO
  convert $TIF -crop 3000x1500+12030+450 -compress lzw $HUMID
  fi
done
