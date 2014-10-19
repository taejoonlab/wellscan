#!/usr/bin/env python
import os
import sys

from PIL import Image, ImageDraw, ImageChops
import math, operator

dir_name = sys.argv[1]

filename_list = []
for filename in os.listdir(dir_name):
    if( not filename.endswith('.tif') ):
        continue
    filename_list.append( os.path.join(dir_name, filename) )

filename_list = sorted(filename_list)
## http://effbot.org/zone/pil-comparing-images.htm
## http://code.activestate.com/recipes/577630-comparing-two-images/
def rmsdiff(im1, im2):
    tmp_diff = ImageChops.difference(im1, im2)
    tmp_hist = tmp_diff.histogram()
    tmp_sq = (value*((idx%256)**2) for idx, value in enumerate(tmp_hist))
    sum_of_squares = sum(tmp_sq)
    rms = math.sqrt(sum_of_squares/float(im1.size[0] * im1.size[1]))
    return rms

f_out = open('%s.rms_diff.txt'%dir_name.replace('/','_'),'w')
prev_im = Image.open(filename_list[0])
for i in range(1,len(filename_list)):
    curr_im = Image.open(filename_list[i])
    tmp_rms = rmsdiff(prev_im.convert('RGB'), curr_im.convert('RGB'))
    #tmp_rms = rmsdiff(prev_im.convert('L'), curr_im.convert('L'))
    #print filename_list[i-1], filename_list[i], tmp_rms
    f_out.write('%s\t%.3f\n'%(filename_list[i], tmp_rms)
    prev_im = curr_im
f_out.close()
