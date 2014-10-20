#!/bin/bash
WIDTH=8000
HEIGHT=11500
X1=700
Y1=2000
X2=8500
Y2=14300

THERMO_WIDTH=500
THERMO_HEIGHT=3000
THERMO_X=0
THERMO_Y=12000

HUMID_WIDTH=3000
HUMID_HEIGHT=1500
HUMID_X=2500
HUMID_Y=0

for TIF in $(ls *-??.tif)
do
  echo $TIF
  P1=${TIF/.tif/.P8.tif}
  P2=${TIF/.tif/.P10.tif}
  P3=${TIF/.tif/.P9.tif}
  P4=${TIF/.tif/.P11.tif}
  THERMO=${TIF/.tif/.thermo.jpg}
  HUMID=${TIF/.tif/.humid.jpg}

  if [ ! -e $P1 ]; then
  convert $TIF -crop $WIDTH"x"$HEIGHT"+"$X1"+"$Y1 -compress lzw $P1
  convert $TIF -crop $WIDTH"x"$HEIGHT"+"$X2"+"$Y1 -compress lzw $P2
  convert $TIF -crop $WIDTH"x"$HEIGHT"+"$X1"+"$Y2 -compress lzw $P3
  convert $TIF -crop $WIDTH"x"$HEIGHT"+"$X2"+"$Y2 -compress lzw $P4
  convert $TIF -crop $THERMO_WIDTH"x"$THERMO_HEIGHT"+"$THERMO_X"+"$THERMO_Y $THERMO
  convert $TIF -crop $HUMID_WIDTH"x"$HUMID_HEIGHT"+"$HUMID_X"+"$HUMID_Y $HUMID
  fi
done
