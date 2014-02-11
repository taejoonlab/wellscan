#!/usr/bin/env python
import sys
from PIL import Image, ImageDraw
import numpy as np
import scipy.stats as stats
import math

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#filename_tif = '/work/taejoon/Dropbox/Public/pub/XenopusIn96_2014feb04_day3.tif'
filename_tif = sys.argv[1]
filename_base = filename_tif.replace('.tiff','').replace('.tif','')

scan_diff_range = 200
scan_ratio_list = [tmp*0.01 for tmp in range(1,100,5)]

im = Image.open(filename_tif)
x_max, y_max = im.size
print im.format, im.size, im.mode
im_array = np.array(im) ## transpose x&y

#### Rotate
def get_xscan(tmp_array):
    rv = dict()
    for x_ratio in scan_ratio_list:
        x = int(x_max * x_ratio)
        tmp_sum_list = [sum(tmp_array[y][x]) for y in range(0,y_max)]
        rv[x] = tmp_sum_list
    return rv 

def get_yscan(tmp_array):
    rv = dict()
    for y_ratio in scan_ratio_list:
        y = int(y_max * y_ratio)
        tmp_sum_list = [sum(tmp_array[y][x]) for x in range(0,x_max)]
        rv[y] = tmp_sum_list
    return rv

x_scan_sum_list = get_xscan(im_array)
rotate_angle_list = []
for i in range(1,len(scan_ratio_list)):
    x0 = int(x_max * scan_ratio_list[i-1])
    x1 = int(x_max * scan_ratio_list[i])
    x0_scan_sum_list = x_scan_sum_list[x0][scan_diff_range:scan_diff_range*-1]
    x1_scan_sum_list = x_scan_sum_list[x1][scan_diff_range:scan_diff_range*-1]
    
    min_delta = 0
    min_diff = -1
    for tmp_delta in range(scan_diff_range*-1+1, scan_diff_range-1):
        tmp_diff = 0
        for i in range(scan_diff_range, int(y_max*0.10)):
            tmp_diff += abs(x_scan_sum_list[x0][i] - x_scan_sum_list[x1][i+tmp_delta])
        if( min_diff == -1 or (min_diff > tmp_diff) ):
            min_diff = tmp_diff
            min_delta = tmp_delta
    
    rotate_angle_list.append( math.atan( float(min_delta)/(x1-x0) )/math.pi*180.0 )

mean_angle = sorted(rotate_angle_list)[int(len(rotate_angle_list)*0.5)]
im = im.rotate(mean_angle)
im.save('%s.rotate.jpg'%filename_base,'jpeg')
x_max, y_max = im.size
im_array = np.array(im) ## transpose x&y

x_scan_sum_list = get_xscan(im_array)
y1_list = []
y2_list = []
for tmp_x in x_scan_sum_list.keys():
    max_y1 = -1
    max_sum = -1
    for tmp_y in range(0,int(y_max*0.1)):
        if( max_sum == -1 or (x_scan_sum_list[tmp_x][tmp_y] > max_sum) ):
            max_sum = x_scan_sum_list[tmp_x][tmp_y]
            max_y1 = tmp_y
    max_y2 = -1
    max_sum = -1
    for tmp_y in range(int(y_max*0.9),y_max):
        if( max_sum == -1 or (x_scan_sum_list[tmp_x][tmp_y] > max_sum) ):
            max_sum = x_scan_sum_list[tmp_x][tmp_y]
            max_y2 = tmp_y
    y1_list.append(max_y1)
    y2_list.append(max_y2)
    
y_scan_sum_list = get_yscan(im_array)
x1_list = []
x2_list = []
for tmp_y in y_scan_sum_list.keys():
    max_x1 = -1
    max_sum = -1
    for tmp_x in range(0,int(x_max*0.1)):
        if( max_sum == -1 or (y_scan_sum_list[tmp_y][tmp_x] > max_sum) ):
            max_sum = y_scan_sum_list[tmp_y][tmp_x]
            max_x1 = tmp_x
    max_x2 = -1
    max_sum = -1
    for tmp_x in range(int(x_max*0.9),x_max):
        if( max_sum == -1 or (y_scan_sum_list[tmp_y][tmp_x] > max_sum) ):
            max_sum = y_scan_sum_list[tmp_y][tmp_x]
            max_x2 = tmp_x
    x1_list.append(max_x1)
    x2_list.append(max_x2)

idx_Q50 = int(len(scan_ratio_list)*0.5)
y1 = sorted(y1_list)[idx_Q50]
y2 = sorted(y2_list)[idx_Q50]
x1 = sorted(x1_list)[idx_Q50]
x2 = sorted(x2_list)[idx_Q50]
print "Crop: X=%d(%d-%d), Y=%d(%d-%d)"%(x2-x1,x2,x1, y2-y1, y2,y1) 
im = im.crop( (x1,y1,x2,y2) )
im_array = np.array(im)
print im.format, im.size, im.mode
x_max, y_max = im.size

corner_x_width = int(x_max*0.05)
corner_right_start = int(x_max*0.94)
corner_left_start = int(x_max*0.01)
corner_y_width = int(y_max*0.07)
corner_top_start = int(y_max*0.02)
corner_bottom_start = int(y_max*0.90)

corner_top_right = 0
corner_top_left = 0
corner_bottom_right = 0
corner_bottom_left = 0
for x in range(corner_right_start, corner_right_start+corner_x_width):
    for y in range(corner_top_start, corner_top_start+corner_y_width):
        corner_top_right += sum(im_array[y][x])
    for y in range(corner_bottom_start, corner_bottom_start+corner_y_width):
        corner_bottom_right += sum(im_array[y][x])
for x in range(corner_left_start, corner_left_start+corner_x_width):
    for y in range(corner_top_start, corner_top_start+corner_y_width):
        corner_top_left += sum(im_array[y][x])
    for y in range(corner_bottom_start, corner_bottom_start+corner_y_width):
        corner_bottom_left += sum(im_array[y][x])

im_draw = im.copy()
draw = ImageDraw.Draw(im_draw)
draw.rectangle((corner_left_start,corner_top_start,corner_left_start+corner_x_width,corner_top_start+corner_y_width),fill=255)
draw.rectangle((corner_right_start,corner_top_start,corner_right_start+corner_x_width,corner_top_start+corner_y_width),fill=255)
draw.rectangle((corner_left_start,corner_bottom_start,corner_left_start+corner_x_width,corner_bottom_start+corner_y_width),fill=255)
draw.rectangle((corner_right_start,corner_bottom_start,corner_right_start+corner_x_width,corner_bottom_start+corner_y_width),fill=255)
im_draw.save('%s.crop_corner.jpg'%filename_base,'jpeg')
print "Corner TL=%d, TR=%d, BL=%d, BR=%d"%(corner_top_left, corner_top_right, corner_bottom_left, corner_bottom_right)

if( corner_top_left < corner_top_right ):
    im = im.transpose(Image.FLIP_LEFT_RIGHT)
x_max, y_max = im.size
im_array = np.array(im)

x_scan_sum_list = get_xscan(im_array)
y_scan_sum_list = get_yscan(im_array)
y3_list = []
y4_list = []
for tmp_x in x_scan_sum_list.keys():
    max_y3 = -1
    max_sum = -1
    for tmp_y in range(int(y_max*0.05),int(y_max*0.15)):
        if( max_sum == -1 or (x_scan_sum_list[tmp_x][tmp_y] > max_sum) ):
            max_sum = x_scan_sum_list[tmp_x][tmp_y]
            max_y3 = tmp_y
    max_y4 = -1
    max_sum = -1
    for tmp_y in range(int(y_max*0.85),int(y_max*0.95)):
        if( max_sum == -1 or (x_scan_sum_list[tmp_x][tmp_y] > max_sum) ):
            max_sum = x_scan_sum_list[tmp_x][tmp_y]
            max_y4 = tmp_y
    y3_list.append(max_y3)
    y4_list.append(max_y4)
    
x3_list = []
x4_list = []
for tmp_y in y_scan_sum_list.keys():
    max_x3 = -1
    max_sum = -1
    for tmp_x in range(int(x_max*0.05),int(x_max*0.10)):
        if( max_sum == -1 or (y_scan_sum_list[tmp_y][tmp_x] > max_sum) ):
            max_sum = y_scan_sum_list[tmp_y][tmp_x]
            max_x3 = tmp_x
    max_x4 = -1
    max_sum = -1
    for tmp_x in range(int(x_max*0.90),int(x_max*0.95)):
        if( max_sum == -1 or (y_scan_sum_list[tmp_y][tmp_x] > max_sum) ):
            max_sum = y_scan_sum_list[tmp_y][tmp_x]
            max_x4 = tmp_x

    x3_list.append(max_x3)
    x4_list.append(max_x4)

draw = ImageDraw.Draw(im)
idx_Q10 = int(len(scan_ratio_list)*0.10)
idx_Q25 = int(len(scan_ratio_list)*0.25)
idx_Q75 = int(len(scan_ratio_list)*0.75)
y3 = sorted(y3_list)[idx_Q50]
y4 = sorted(y4_list)[idx_Q50]
x3 = sorted(x3_list)[idx_Q50]
print x3_list
x4 = sorted(x4_list)[idx_Q50]
print x4_list
x_margin = int((x4-x3)*0.02)
x3 -= x_margin
x4 += x_margin
y_margin = int((y4-y3)*0.04)
y3 -= y_margin
y4 += y_margin
print "Well area: X=%d(%d-%d), Y=%d(%d-%d)"%(x4-x3,x4,x3, y4-y3, y4,y3) 

x_well_size = float(x4-x3)/12
y_well_size = float(y4-y3)/8
print x_well_size, y_well_size
#well_size = int(0.5*( (y4-y3)/8 + (x4-x3)/12 ))
for col in range(0,13):
    x_well_step = int(x_well_size*col)
    draw.line((x3+x_well_step,y3,x3+x_well_step,y4),fill=(255,255,0), width=3)
for row in range(0,9):
    y_well_step = int(y_well_size*row)
    draw.line((x3,y3+y_well_step,x4,y3+y_well_step),fill=(255,255,0), width=3)

im.save('%s.flip_grid.jpg'%filename_base,'jpeg')
sys.exit(1)

bw_array = np.zeros((y_max, x_max))
row_list = ['A','B','C','D','E','F','G','H']
for col in range(0,12):
    for row in range(0,8):
        im_well = im.crop( (x_start+well_size*col,y_start+well_size*row,x_start+well_size*(col+1),y_start+well_size*(row+1)) )
        im_well.save('%s_%s%02d.tif'%(filename_base,row_list[row],col+1),'tiff')
#plt.gray()
#plt.imshow(bw_array)
#plt.savefig('gray.png')
