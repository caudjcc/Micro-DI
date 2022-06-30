#!/usr/bin/env python
# coding: utf-8
import os
import numpy as np
import pandas as pd
from numba import jit
from PIL import Image



label_path = r'E:\sensors\result\E3_PST_A\pseudo_color_prediction'
picture_list=os.listdir(label_path)
total_picture=len(picture_list)
#Rust class value: 2
#Healthy class value: 1
#Other class value: 0

@jit
def cal_md(img, crop_size):
    n_row = img.shape[0]//crop_size
    n_col = img.shape[1]//crop_size
    wheats_exists= 0
    pst_exists = 0
    level_1 = 0
    level_2 = 0
    level_3 = 0
    level_4 = 0
    level_5 = 0
    level_6 = 0
    level_7 = 0
    level_8 = 0
    for i in range(n_row):
        for j in range(n_col):
            img_crop = img[i*crop_size:(i+1)*crop_size,
                           j*crop_size:(j+1)*crop_size]
            if 1 in img_crop and 2 not in img_crop:
                wheats_exists += 1#Count the number of tiles that contain only the Healthy class
            if 2 in img_crop:
                pst_exists += 1#Count the number of tiles that contain the Rust class
                
                md = (img_crop == 2).sum() / ((img_crop == 1).sum()+(img_crop == 2).sum())
                #Percentage of rust class: Rust/(rust+healthy wheat)
                if md < 0.025:
                    #1%
                    level_1 +=1
                    continue
                if md < 0.075:
                    #5%
                    level_2 +=1
                    continue
                if md < 0.15:
                    #10%
                    level_3 +=1
                    continue
                if md < 0.3:
                    #20%
                    level_4 +=1
                    continue
                if md < 0.5:
                    #40%
                    level_5 +=1
                    continue
                if md < 0.7:
                    #60%
                    level_6 +=1
                    continue
                if md < 0.9:
                    #80%
                    level_7 +=1
                    continue
                if md <= 1:
                    #100%
                    level_8 +=1
                continue

    wheats_exists=wheats_exists+pst_exists
    #MF:Incidence;MS: Severity; MDI:Macro Disease Index 
    MF=round(pst_exists/wheats_exists,4) if pst_exists>0 else 0 
    MS=round((level_1*0.01+level_2*0.05+level_3*0.1+level_4*0.2+level_5*0.4+level_6*0.6+level_7*0.8+level_8)/pst_exists,4) if pst_exists>0 else 0
    MDI=round((level_1*0.01+level_2*0.05+level_3*0.1+level_4*0.2+level_5*0.4+level_6*0.6+level_7*0.8+level_8)/wheats_exists,4) if pst_exists>0 else 0
    return  MF, MS, MDI

out = []
Tiles_size=100 #

for item in picture_list :
    src = os.path.join(os.path.abspath(label_path), item)
    lbl_crop = np.array(Image.open(src))
    result = cal_md(lbl_crop,Tiles_size) + (item,)
    out.append(result)   
   
column=[ 'Incidenc', 'Severity', 'MDI', 'Name']
df=pd.DataFrame(columns=column,data=out)
save_path=os.path.join(os.path.abspath(label_path), 'result.csv')
df.to_csv(save_path,encoding='utf-8')



















   
        




