# -*- coding: utf-8 -*-
"""
## information
# Bridge superstructure plan coordination in spiral/clothoid region
# Reference: https://en.wikipedia.org/wiki/Euler_spiral
# TS to SC

## input
# Rc = 1500 ;      # Curvature radius in meter     
# Ls = 24.576;   # Spiral length in meter
# dL = 2;       # length increment in meter
# direction = +1; # +1: clockwise, -1: counter clockwise

## Ouput
# x x-coordinates in meter
# y y-coordinates in meter
# delta tangential angle in radian (ve+ clockwise)

## Note
# origin of x,y, delta is 0,0,0. That means output values are the relative
# coordinates and tangential angle.
"""
import math
import numpy as np
import sympy as sp

def spiral_coord(Rc, Ls, dL, direction):
    
    ## normalize factor, a
    
    a = 1/math.sqrt(2*Rc*Ls)
    
    ## Define L
    
    L  = np.append(np.arange(0,Ls,dL), Ls);
    
    ## Map L of the original Euler spiral by multiplying with factor a to norm_L of the normalized Euler spiral
    norm_L = L*a;
    
    ## Find (xx, yy) from the Fresnel integrals; and
    xx = np.zeros((len(L),1));
    yy = np.zeros((len(L),1));
    
    x = sp.symbols('x') 
    s = sp.sin(x**2)
    c = sp.cos(x**2)
    
    for i in range(1,len(L)):
        LL = norm_L[i]
        xx[i] = sp.integrate(c,(x,0,LL))
        yy[i] = sp.integrate(s,(x,0,LL))*-direction
        
    x = 1/a*xx
    y = 1/a*yy
    delta = L**2/(2*Ls*Rc)*direction
    
    return L,x,y,delta

def spiral_coord2(Rc, Ls, dL, direction):
    
    ## normalize factor, a
    
    a = 1/math.sqrt(2*Rc*Ls)
    
    ## Define L
    
    L  = np.append(np.arange(0,Ls,dL), Ls);
    
    ## Map L of the original Euler spiral by multiplying with factor a to norm_L of the normalized Euler spiral
    norm_L = L*a;
    
    ## Find (xx, yy) from the Fresnel integrals; and
    xx = np.zeros((len(L),1));
    yy = np.zeros((len(L),1));
    
    x = sp.symbols('x') 
    s = sp.sin(x**2)
    c = sp.cos(x**2)
    
    for i in range(1,len(L)):
        LL = norm_L[i]
        xx[i] = sp.integrate(c,(x,0,LL))
        yy[i] = sp.integrate(s,(x,0,LL))*-direction
        
    x = 1/a*xx
    y = 1/a*yy
    delta = L**2/(2*Ls*Rc)*direction
    
    ## Edit x,y form from TS-SC to CS-ST
    # coordinates transformation
    x1 = x-x[-1];
    y1 = y-y[-1];
    theta = -delta[-1];
    R_mat = [[math.cos(theta), -math.sin(theta)],
             [math.sin(theta),  math.cos(theta)]]
    xy2 = np.matmul(np.column_stack((x1,y1)),R_mat)
    L2 = np.flipud(-1*(L-L[-1]));
    x2 = np.flipud(-xy2[:,0]);
    y2 = np.flipud(xy2[:,1]);
    delta2 = np.flipud(-1*(delta-delta[-1]));
    
    return L2,x2,y2,delta2

def curve_coord(Rc, Lc, dL, direction):
    
    ## Define L
    L  = np.append(np.arange(0,Lc,dL), Lc);
    
    ## calculate x,y,delta
    x = np.zeros((len(L),1));
    y = np.zeros((len(L),1));
    delta = np.zeros((len(L),1)); 
    
    for i in range(1,len(L)):
        d_delta = (L[i]-L[i-1])/Rc*direction;
        l_chord = abs(2*Rc*math.sin(d_delta/2));
        x[i] = x[i-1]+l_chord*math.cos(delta[i-1]+d_delta/2);
        y[i] = y[i-1]-l_chord*math.sin(delta[i-1]+d_delta/2);
        delta[i] = delta[i-1]+d_delta; 
            
    return L,x,y,delta
    


# Test

## input
# Rc = 1500 ;      # Curvature radius in meter     
# Ls = 24.576;   # Spiral length in meter
# dL = 2;       # length increment in meter
# direction = +1; # +1: clockwise, -1: counter clockwise

# a = 1/math.sqrt(2*Rc*Ls)
    
# ## Define L

# L  = np.append(np.arange(0,Ls,dL), Ls);

# ## Map L of the original Euler spiral by multiplying with factor a to norm_L of the normalized Euler spiral
# norm_L = L*a;

# ## Find (xx, yy) from the Fresnel integrals; and
# xx = np.zeros((len(L),1));
# yy = np.zeros((len(L),1));

# x = sp.symbols('x') 
# s = sp.sin(x**2)
# c = sp.cos(x**2)

# for i in range(1,len(L)):
#     LL = norm_L[i]
#     xx[i] = sp.integrate(c,(x,0,LL))
#     yy[i] = sp.integrate(s,(x,0,LL))*-direction
    
# x = 1/a*xx
# y = 1/a*yy
# delta = L**2/(2*Ls*Rc)*direction