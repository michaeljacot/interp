# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 12:21:40 2020

@author: Michael
"""

import numpy as np 
import matplotlib.pyplot as plt
from interp import interp

x = np.linspace(0,50,num = 1000)


y1 = np.sin(x)
y2 = np.cos(x)

plt.plot(x,y1)
plt.plot(x,y2)

y1 = list(y1)
y2 = list(y2)

interpObj = interp(y1,y2)




polygons  = interpObj.polygons
angles = interpObj.angles
diff = interpObj.diff
index = interpObj.result




plt.plot(interpObj.sma50)
plt.plot(interpObj.sma200)
#plots the individual intersections points in red on the graph with the data sets
for i in interpObj.intersections:
    plt.plot(i,interpObj.sma50[i], marker='o', markersize=3, color="red")
plt.show()

angleTitle = "Angle difference: " , len(interpObj.diff) 
plt.title(angleTitle)
plt.plot(interpObj.diff)
plt.show()
polyTitle = "Polygon area: ", len(interpObj.polygon_areas)
plt.title(polyTitle)
plt.plot(interpObj.polygon_areas)
plt.show()
plt.plot(interpObj.result)
plt.title("Interp Index")
plt.plot(interpObj.result)