#!/bin/bash
## Create thumbnails using  ImageMagick
THUMBS_PATH="./thumbs"

if [ ! -e $THUMBS_PATH ]; then
  mkdir $THUMBS_PATH
fi

mogrify -format jpg -path $THUMBS -thumbnail 320x320 *tif
