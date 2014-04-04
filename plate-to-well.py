#!/usr/bin/env python
import os
import sys
import json

from PIL import Image, ImageDraw
import numpy as np

filename_tif = sys.argv[1]
filename_base = filename_tif.replace('.tiff','').replace('.tif','')

filename_conf = 'plate-to-96.json'
if( not os.access(filename_conf, os.R_OK) ):
    sys.stderr.write('%s does not exist.\n'%filename_conf)
    sys.exit()

conf_param = ['rotate_angle','x0','y0','width','height','flip_vertical','flip_horizontal']
f_conf = open(filename_conf,'r')
conf = json.loads(f_conf.read())
for tmp_param in conf.keys():
    if( not conf.has_key(tmp_param) ):
        sys.stderr.write('%s parameter does not exist. Please check the format.\n')
        sys.exit(1)
f_conf.close()

im = Image.open(filename_tif)
x_max, y_max = im.size

rotate_angle = float(conf['rotate_angle'])
x1 = int(conf['x0'])
x2 = int(conf['x0'])+int(conf['width'])
y1 = int(conf['y0'])
y2 = int(conf['y0'])+int(conf['height'])
cols = int(conf['columns'])
rows = int(conf['rows'])

## Manupulate
if( int(conf['flip_horizontal']) > 0 ):
    im = im.transpose(Image.FLIP_LEFT_RIGHT)
if( int(conf['flip_vertical']) > 0 ):
    im = im.transpose(Image.FLIP_TOP_BOTTOM)
if( rotate_angle != 0 ):
    im = im.rotate(rotate_angle)
im = im.crop( (x1,y1,x2,y2) )

x_max, y_max = im.size
x_well_size = float(x_max)/cols
y_well_size = float(y_max)/rows

im_draw = im.copy()
draw = ImageDraw.Draw(im_draw)
for col in range(0,cols+1):
    x_well_step = int(x_well_size*col)
    draw.line((x_well_step,0,x_well_step,y_max),fill=200, width=5)

for row in range(0,rows+1):
    y_well_step = int(y_well_size*row)
    draw.line((0,y_well_step,x_max,y_well_step),fill=200, width=5)

im_draw = im_draw.resize((int(x_max*0.10),int(y_max*0.10)),  Image.ANTIALIAS)
im_draw.save('%s.grid.jpg'%filename_base,'jpeg', quality=50)

row_list = ['A','B','C','D','E','F','G','H']
for col in range(0,cols):
    for row in range(0,rows):
        x1 = int(x_well_size * col)
        y1 = int(y_well_size * row)
        x2 = int(x_well_size * (col+1))
        y2 = int(y_well_size * (row+1))
        dir_name = '%s%02d'%(row_list[row],col+1)
        if( not os.access(dir_name, os.R_OK) ):
            os.mkdir(dir_name,0755)
        im_well = im.crop( (x1, y1, x2, y2) )
        im_well.save(os.path.join(dir_name, '%s_%s%02d.tif'%(filename_base,row_list[row],col+1)),'tiff')
