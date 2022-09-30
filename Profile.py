# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 08:59:48 2022

@author: KOCI
"""

import pandas as pd

InputData = pd.read_excel('Modelling_input.xlsx')

Ltype = InputData[['ID','type']] 
STA = InputData['Station PK']
L_dat = InputData['Lc/Ls']
Rc_dat = InputData['R']
dirc_dat = InputData['direction']
CE_id = InputData['CE_id']
V_veh = InputData['Vd']