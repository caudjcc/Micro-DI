import os
from numba import jit
from PIL import Image
import numpy as np
import random
import shutil
Image.MAX_IMAGE_PIXELS = None


picture_path=r"E:\sensors\data\Image"
label_path=r"E:\sensors\data\Label"

new_picture_path=r"E:\sensors\data\select\Image"
new_label_path=r"E:\sensors\data\select\Label"

picture_list=os.listdir(label_path)
total_picture=len(picture_list)

if __name__ == '__main__':  
  
    
    pstlist = []
    wheatlist = []
    pstlist_2 = []
    backgroundlist = []
    all_list =[]
    for item in picture_list:
      src = os.path.join(os.path.abspath(label_path), item)
      print("start: %s "%item)
      total_picture-=1
     
      lbl_crop = np.array(Image.open(src))
      if (lbl_crop == 2).sum()/lbl_crop.size >0.3 : #Get the filename of the tiles with rust class ratio greater than 0.3
          pstlist.append(item)
          
      elif (lbl_crop == 2).sum()/lbl_crop.size >0.1 : 
          pstlist_2.append(item)
          
      elif (lbl_crop == 1).sum()/lbl_crop.size >0.2 :
          wheatlist.append(item)
          
      else:
          backgroundlist.append(item)          

      #随机选取图片
    all_list+=pstlist
    all_list+=pstlist_2
    all_list+=random.sample(wheatlist, 3000)
    all_list+=random.sample(backgroundlist, 2000)
    #拷贝图片
   
    for i in all_list:
       
       old_label=os.path.join(os.path.abspath(label_path), i)
       new_label=os.path.join(os.path.abspath(new_label_path), i)
       shutil.copyfile(old_label, new_label)
       name, _ = i.rsplit('.png')       
       name = name + ".jpg"
       old_image=os.path.join(os.path.abspath(picture_path), name)
       new_image=os.path.join(os.path.abspath(new_picture_path), name)
       shutil.copyfile(old_image, new_image)
       print(i)
       print(name)
      
 
    

