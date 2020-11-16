# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 12:21:40 2020

@author: Michael
"""

import numpy as np 
import matplotlib.pyplot as plt

x = np.linspace(0,50,10000)


y1 = np.sin(x)
y2 = np.cos(x)

plt.plot(x,y1)
plt.plot(x,y2)