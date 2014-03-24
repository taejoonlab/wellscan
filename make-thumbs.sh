#!/bin/bash
## Create thumbnails using  ImageMagick
THUMBS_PATH="./thumbs"

if [ ! -e $THUMBS_PATH ]; then
  mkdir $THUMBS_PATH
fi

for TIF in $(ls ./*.tif)
do
  echo $TIF
  JPG=${TIF/.tif/.jpg}
  #mogrify -format jpg -path $THUMBS -thumbnail 320x320 $TIF
  convert $TIF -thumbnail 800x800 -unsharp 0x.8 $THUMBS_PATH"/"$JPG
done
#find -name '*.tif ' -print0 | xargs -0 mogrify -format jpg -path $THUMBS -thumbnail
