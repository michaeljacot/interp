# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 23:22:15 2020

@author: Michael
"""

import numpy as np
import matplotlib.pyplot as plt
from lineCalc import *
from shapely.geometry import Polygon
from SupportResistanceMethod import getData



class interp:



    def __init__(self,ticket,domain):
        sma50,sma200,prices = self.get50and200(ticket, domain)
        sma50 = sma50[:len(sma200)]
        
        
        
        result,angles,intersections,polygon_areas,polygons,diff = self.getAnalysis(sma200,sma50)
        
        self.ticket = ticket
        self.domain = domain
        self.sma50 = sma50
        self.sma200 = sma200
        self.prices = prices
        self.result = result
        self.angles = angles
        self.intersections = intersections
        self.polygon_areas = polygon_areas
        self.polygons = polygons
        self.diff = diff
        
        


        
    
    
    
    def SMA(self, x, w):
        return np.convolve(x, np.ones(w), 'valid') / w
    
    
    def get50and200(self, ticket,domain):
        
        prices = getData(ticket, domain)
        
        sma50 = self.SMA(prices,50)
        sma200 = self.SMA(prices,200)
        
        return sma50,sma200,prices
        
        
    
    
    
    
    
    
    """
    Think of ways to make indicators to see if the stock is a good buy.
    
    
    Idea 1 : Project the data onto other scales (log,x^2,2^x,poly) and see which one looks most like a straight line (best fit)
    
    Idea 2 : Idea for estimating the amount of money put into each position. Use the angle between the two moving averages as an indicator to 
        how much money should be placed into the position.
        
        
    
    """
    
    
    
    #this method takes in two plots and returns the intersection points of the curves as well as the angle at which they intersect
    
    
    
    
    
    
    
    #input: two lists
    #output: list of indicies which are the intersection points
    
    
    def getIntersections(self, shortMa, longMa):
         
        intersections = []
        
        #have to find which moving average is above at the start of the data set
        #highest = 1 : short list starts on top    
        #highest = 0 : long list starts on top
        
        highest = None
        
        if shortMa[0] > longMa[0]: 
            highest = 1 
        else: 
            highest = 0
    
        # count through the data sets and check to see when the points intersect
        for i in range(len(shortMa)-1):
            
            if highest == 1:
                if shortMa[i] < longMa[i]:
                    print(i)
                    intersections.append(int(i))
                    highest = 0 #reset the highest so that the longerlist is on top
                
                
            elif highest == 0:
                if longMa[i] < shortMa[i]:
                    intersections.append(int(i))
                    highest = 1
                
            else:
                print("Highest not set at index " , i)
                break
        return intersections
    
    
    #method that finds the angle of intersection of each of the intersection points
    def getAngles(self, shortMa,longMa,intersections):
        
        angles = []
        
        
        localRange = 5
        
        x = np.arange(0,len(shortMa),1)
        
        for i in intersections:
            
            #case for when the intersection point is too close to the start of the data set
            if i < localRange:
                
                #checks to make sure that the function at least has some data points to make a line
                if i <= 2:
                    pass
                else:
                    #get average intersection lines for this intersection
                    mShort,bShort = np.polyfit(x[:i],shortMa[:i],1)
                    mLong,bLong = np.polyfit(x[:i],longMa[:i],1)
                    
                    #convert to angle relative to x axis 
                    mShort = np.arctan(mShort)
                    mLong = np.arctan(mLong)
                    
                    angles.append((mShort,mLong,i))
                    
            
            else:
                #get average intersection lines for this intersection
                mShort,bShort = np.polyfit(x[i-localRange:i],shortMa[i-localRange:i],1)
                mLong,bLong = np.polyfit(x[i-localRange:i],longMa[i-localRange:i],1)
                angles.append((mShort,mLong,i))
    
     
        return angles
    
    
    
      
    def areaAnalysis(self, shortMa,longMa,intersections):
        
        
        #makes them the same length (idk if we need this but its here)
        #basically the idea for this is to return a list of the areas between the curves for each interval (between intersection points)
        
        
    
    
        
        
        polygon_areas = []
        polygons = []
        
    
        
        for i in range(len(intersections)-1):
            
            
            thisPolygon = []
            
            #go to the actual x position (time)
            
            
            if intersections[i] < 1:
                pass
            else:
                
                """
                start = intersections[i-1]
                end = intersections[i]
                """
                
                
                start = intersections[i]
                end = intersections[i+1]
                
                
                
                
                
                #runs foreward through the subsection, taking the whichever value is on top first
                for f in range(start,end+1,):
                    
                    if shortMa[f] >= longMa[f]:
                    
                        thisPoint = [f,shortMa[f]]
                        
                    else:
                        
                        thisPoint = [f,longMa[f]]
                        
                    thisPolygon.append(thisPoint)
            
                #once you hit the end of this subset, loop backwards and get all of the data points on the bottom plot
                for b in range(end,start-1,-1):
                    
                
                    if shortMa[b] <= longMa[b]:
                    
                        thisPoint = [b,shortMa[b]]
                        
                    else:
                        
                        thisPoint = [b,longMa[b]]
                        
                    thisPolygon.append(thisPoint)
    
                polygons.append(thisPolygon)
    
            
                
                
            
            polygon = Polygon(thisPolygon)
            area = polygon.area
            polygon_areas.append(area)
            
            
            
            
        return polygon_areas,polygons
    
    
    
    def getAnalysis(self, shortMa,longMa):
        
    
        
        
        """
             ##Things I want this method to return##
        
            1. Number of intersections of the data set
            2. Total area above/beneath plots
            
            
            #interpretation of results#
            
            a large area before intersection and a steep intersection angle result in the highest confidence
            a small area before intersection and small intersection angle result in the lowest confidence
        """
        
        #makes them the same length
        if len(shortMa) < len(longMa):
            longMa = longMa[:len(shortMa)]
        elif len(longMa) < len(shortMa):
            shortMa = shortMa[:len(longMa)]

        
        intersections = self.getIntersections(shortMa,longMa)
        
        
        lines = self.getAngles(shortMa,longMa,intersections)
        plt.show()
        
        diff = []
        
        for l in lines:
            diff.append(l[0]-l[1])
            print("The intersection at " , l[2], " has a slope difference of " , abs(l[0]-l[1]))
        
        
        
        polygon_areas,polygons = self.areaAnalysis(shortMa, longMa, intersections)
    
        
        i = 0
        for p in polygon_areas:
            print("The polygon at intrval ", i, " has \nArea ", p)
            i+=1
        
        
        #normalzie both data sets
            
        diff = self.normalizeData(diff)
        polygon_areas = self.normalizeData(polygon_areas)
        
        compare = self.relationship(diff,polygon_areas)
        
        
        return compare,lines,intersections, polygon_areas,polygons,diff
    
    
    def normalizeData(self, data):
        return (data - np.min(data)) / (np.max(data) - np.min(data))
    
    def relationship(self, diff,polygon_areas):
        
        result = []
        
        
        """
        *thing to rememeber about this*
        
        we want to compare the angle to the area of the section that 
        came directly before the intersection. this means that when adding them
        in index form (like below) you cant just add a[i]+b[i], one of the indexes 
        probbably has to be staggered
        
        """
        
        
        for i in range(len(polygon_areas)):
        
            #ACTUAL EQUATION GOES HERE
            """
                R = (A+D)/2
            """
            result.append((polygon_areas[i]+diff[i+1])/2)
            
        return result
    

ticket = "DJI"
interpObj = interp(ticket,2000)



polygons  = interpObj.polygons
angles = interpObj.angles
diff = interpObj.diff
index = interpObj.result



plt.title(ticket)
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


#maybe make a method outside of this class(or in this class) to display the info graphically instead of doing this bullshit
