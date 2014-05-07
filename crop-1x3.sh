#!/bin/bash
HEIGHT=8100
WIDTH=12000
X1=0
Y1=1800
Y2=10000
Y3=18000

THERMO_WIDTH=1080
THERMO_HEIGHT=4200
THERMO_X=11500
THERMO_Y=12500

HUMID_WIDTH=3000
HUMID_HEIGHT=1500
HUMID_X=7000
HUMID_Y=50

for TIF in $(ls *-??.tif)
do
  echo $TIF
  P1=${TIF/.tif/.M02_P4.tif}
  P2=${TIF/.tif/.M02_P5.tif}
  P3=${TIF/.tif/.M02_P6.tif}
  THERMO=${TIF/.tif/.thermo.tif}
  HUMID=${TIF/.tif/.humid.tif}

  if [ ! -e $P1 ]; then
  convert $TIF -crop $WIDTH"x"$HEIGHT"+"$X1"+"$Y1 -compress lzw $P1
  convert $TIF -crop $WIDTH"x"$HEIGHT"+"$X1"+"$Y2 -compress lzw $P2
  convert $TIF -crop $WIDTH"x"$HEIGHT"+"$X1"+"$Y3 -compress lzw $P3
  convert $TIF -crop $THERMO_WIDTH"x"$THERMO_HEIGHT"+"$THERMO_X"+"$THERMO_Y -compress lzw $THERMO
  convert $TIF -crop $HUMID_WIDTH"x"$HUMID_HEIGHT"+"$HUMID_X"+"$HUMID_Y -compress lzw $HUMID
  fi
done
