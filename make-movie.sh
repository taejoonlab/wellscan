#!/bin/bash
FPS=10
i=1

DATA_NAME=$(basename $(dirname $PWD))
WELL_ADDRESS=$(basename $PWD)
MOVIE_NAME=$DATA_NAME"."$WELL_ADDRESS".avi"

if [ -e $MOVIE_NAME ]; then
  echo "$MOVIE_NAME exists. Skip."
else
  rm -rf tmp
  mkdir tmp

  for TIF in $(ls *.{tif,jpg})
  do
    TMP=$(printf "tmp/image%03d.bmp" $i)
    echo $TIF "-->" $TMP
    convert $TIF label:\"$DATA_NAME\" -gravity Center -append $TMP
    i=$(($i + 1))
  done

  #DATA_NAME=$(ls $TIF | awk -F"_" '{print $1}')
  #WELL_ADDRESS=$(ls $TIF | awk -F"." '{print $2}')
  mencoder "mf://tmp/*.bmp" -mf fps=$FPS -o $MOVIE_NAME -ovc lavc
  rm -rf tmp
fi
