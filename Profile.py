# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 08:59:48 2022

@author: KOCI
"""

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from profile_func import spiral_coord
from profile_func import spiral_coord2
from profile_func import curve_coord

InputData = pd.read_excel('Modelling_input.xlsx')

ID = InputData['ID'] 
Ltype = InputData['type'] 
STA = InputData['Station PK']
L_dat = InputData['Lc/Ls'].astype(float)
Rc_dat = InputData['R']
dirc_dat = InputData['direction']
CE_id = InputData['CE_id']
V_veh = InputData['Vd']

# Plan profile
dL = 2; # Length increment [m]

# 선형 초기 값 설정
L = np.array([0]);  # 길이
x = np.array([0]);  # x 좌표
y = np.array([0]);  # y 좌표
beta = np.array([0]); # beta 각도

for i in range(0,len(Ltype)-1):
    if Ltype[i] == "Straight":
        # print('straight')
        Lt1 = L_dat[i]      # 직선구간 길이
        Ltmp = np.append(np.arange(0,Lt1,dL), Lt1); # 정의한 구간길이로 길이array 생성
        xt2 = Ltmp # 선형의 x좌표 (직선이라 길이와 같음)
        yt2 = np.zeros(len(xt2)) #선형의 y좌표 (직선이라 0)
        beta_tmp = np.zeros(len(xt2)) # 선형의 beta 각도
        theta = beta[-1] # 선형의 마지막 점의 beta 각도
        R_mat = [[math.cos(theta), -math.sin(theta)],
                 [math.sin(theta),  math.cos(theta)]]
        xyt2 = np.matmul(np.column_stack((xt2,yt2)),R_mat)
        xtmp = xyt2[:,0]
        ytmp = xyt2[:,1]
    elif Ltype[i] == "Spiral":
        # print('spiral')
        Rc = Rc_dat[i]
        Ls = L_dat[i]
        direction = dirc_dat[i]
        Ltmp, xs1, ys1, beta_tmp = spiral_coord(Rc, Ls, dL, direction);
        theta = beta[-1] # 선형의 마지막 점의 beta 각도
        R_mat = [[math.cos(theta), -math.sin(theta)],
                 [math.sin(theta),  math.cos(theta)]]
        xys1 = np.matmul(np.column_stack((xs1,ys1)),R_mat)
        xtmp = xys1[:,0]
        ytmp = xys1[:,1]
        
    elif Ltype[i] == "Spiral2":
        # print('spiral2')
        Rc = Rc_dat[i]
        Ls = L_dat[i]
        direction = dirc_dat[i]
        Ltmp, xs1, ys1, beta_tmp = spiral_coord2(Rc, Ls, dL, direction);
        theta = beta[-1] # 선형의 마지막 점의 beta 각도
        R_mat = [[math.cos(theta), -math.sin(theta)],
                 [math.sin(theta),  math.cos(theta)]]
        xys1 = np.matmul(np.column_stack((xs1,ys1)),R_mat)
        xtmp = xys1[:,0]
        ytmp = xys1[:,1]
    elif Ltype[i] == "Curve":
        # print('curve')
        Rc = Rc_dat[i]
        Lc = L_dat[i]
        direction = dirc_dat[i]
        Ltmp, xc1, yc1, beta_tmp = curve_coord(Rc, Lc, dL, direction);
        theta = beta[-1] # 선형의 마지막 점의 beta 각도
        R_mat = [[math.cos(theta), -math.sin(theta)],
                 [math.sin(theta),  math.cos(theta)]]
        xyc1 = np.matmul(np.column_stack((xc1,yc1)),R_mat)
        xtmp = xyc1[:,0]
        ytmp = xyc1[:,1]
    else:
        print('check line type')
        
    L = np.append(L, L[-1]+Ltmp[1:len(Ltmp)])
    x = np.append(x, x[-1]+xtmp[1:len(xtmp)])
    y = np.append(y, y[-1]+ytmp[1:len(ytmp)])
    beta = np.append(beta, beta[-1]+beta_tmp[1:len(Ltmp)])
    
    L, indx = np.unique(L, return_index = True)
    x = x[indx]
    y = y[indx]
    beta = beta[indx]
    
# create figure and axis objects with subplots()
fig,ax = plt.subplots()
# make a plot
ax.plot(x, y)
# set x-axis label
ax.set_xlabel("x[m]", fontsize = 14)
# set y-axis label
ax.set_ylabel("y[m]", fontsize = 14)

# create figure and axis objects with subplots()
fig,ax2 = plt.subplots()
# make a plot
ax2.plot(L, beta)
# set x-axis label
ax2.set_xlabel("L[m]", fontsize = 14)
# set y-axis label
ax2.set_ylabel("beta[rad]", fontsize = 14)


