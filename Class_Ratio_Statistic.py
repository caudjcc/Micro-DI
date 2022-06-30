# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 00:36:50 2022

@author: Administrator
"""
import os
from numba import jit
from PIL import Image
import numpy as np
Image.MAX_IMAGE_PIXELS = None

label_path=r"E:\sensors\result\256crop\test_label"
picture_list=os.listdir(label_path)
total_picture=len(picture_list)

#Statistics set of each class share
@jit
def imgMin(img):
#This function is used to count the total number of pixel points in each class of the picture
  mat=Image.open(img)
  mat = np.array(mat)
  height=mat.shape[0]
  width=mat.shape[1]
  background=0
  wheat=0
  pst=0
  other=0
  for i in range(height):
    for j in range(width):
      if mat[i][j]==0 :
        background+=1
      elif mat[i][j]==1 :
        wheat+=1
      elif mat[i][j]==2 :
        pst+=1
      else:
        other+=1
  return(background, wheat, pst, other)

if __name__ == '__main__':  
    g_background=0
    g_wheat=0
    g_pst=0
    g_other=0

    for item in picture_list:
      src = os.path.join(os.path.abspath(label_path), item)
      print("start: %s "%item)
      total_picture-=1
      background, wheat, pst, other=imgMin(src)
      g_background+=background
      g_wheat+=wheat
      g_pst+=pst
      g_other+=other
      
    print("rust class ratio: %s "%(g_pst/(g_pst+g_wheat+g_background)))
    print("wheat class ratio: %s "%(g_wheat/(g_pst+g_wheat+g_background)))
    print("background class ratio: %s "%(g_background/(g_pst+g_wheat+g_background)))
      
      
      
      
      