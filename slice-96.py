#!/usr/bin/env python
import os
import sys
from PIL import Image, ImageDraw

filename_tif = sys.argv[1]
filename_base = filename_tif.replace('.tiff','').replace('.tif','')

im = Image.open(filename_tif)
x_max, y_max = im.size

x_well_size = float(x_max)/12
y_well_size = float(y_max)/8

im_draw = im.copy()
draw = ImageDraw.Draw(im_draw)
for col in range(0,13):
    x_well_step = int(x_well_size*col)
    draw.line((x_well_step,0,x_well_step,y_max),fill=(255,255,0), width=3)
for row in range(0,9):
    y_well_step = int(y_well_size*row)
    draw.line((0,y_well_step,x_max,y_well_step),fill=(255,255,0), width=3)

im_draw = im_draw.resize((int(x_max*0.10),int(y_max*0.10)),  Image.ANTIALIAS)
im_draw.save('%s.grid.jpg'%filename_base,'jpeg', quality=50)

row_list = ['A','B','C','D','E','F','G','H']
for col in range(0,12):
    for row in range(0,8):
        x1 = int(x_well_size * col)
        y1 = int(y_well_size * row)
        x2 = int(x_well_size * (col+1))
        y2 = int(y_well_size * (row+1))
        dir_name = '%s%02d'%(row_list[row],col+1)
        if( not os.access(dir_name, os.R_OK) ):
            os.mkdir(dir_name,0755)
        im_well = im.crop( (x1, y1, x2, y2) )
        im_well.save(os.path.join(dir_name, '%s_%s%02d.tif'%(filename_base,row_list[row],col+1)),'tiff')
