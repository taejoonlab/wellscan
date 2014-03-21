#!/bin/bash
rm -rf tmp
mkdir tmp

i=1
for TIF in $(ls *tif)
do
  DATA_NAME=${TIF/.tif/}
  TMP=$(printf "tmp/image%03d.bmp" $i)
  echo $TIF "-->" $TMP
  convert $TIF label:\"$DATA_NAME\" -gravity Center -append $TMP
  i=$(($i + 1))
done
DATA_NAME=$(ls $TIF | awk -F"_" '{print $1}')
WELL_ADDRESS=$(ls $TIF | awk -F"." '{print $2}')
MOVIE_NAME=$DATA_NAME"."$WELL_ADDRESS".avi"
mencoder "mf://tmp/*.bmp" -mf fps=5 -o $MOVIE_NAME -ovc lavc
