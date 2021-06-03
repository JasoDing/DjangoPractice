# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 01:18:22 2021

@author: dingz

"""
from stock.models import *
import numpy as np
import pandas as pd
#from dtw import *            #DTW package is for validate result only.Not used in main code
import matplotlib.pyplot as plt
import time

class DTW:
    def compare(self,file1,file2,size,fast = False): 
        # DTW compare function, file1, file 2 are the input files, size is the input data size, fast is a boolean when True, run DTW with window; when false, run basic DTW
        
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)
        
        df1k = df1.head(size)
        df2k = df2.head(size)
        # print(type(df1k))

        x = df1k[['attr_x', 'attr_y', 'attr_z']].values[:,:]
        #print(x.shape)
        y = df2k[['attr_x', 'attr_y', 'attr_z']].values[:,:]
        #print(y.shape)
        
        # Select different DTW method:
        if fast:  
            res = self.faster_dtw(x, y)
            print('DTW with window: Distance = ',res)
        else:
            res = self.do_dtw(x,y)
            print('Basic DTW: Distance = ',res)
        #cmp = dtw(x,y)
        #print('cmp ',cmp.distance)
        #return res
        
    '''
    # a validate function used when producing the figures in PPT, for presentation only.
    def validate(self,size):
        idx = np.linspace(0,12.56,num=size)
        query = np.sin(idx) + np.random.uniform(size=size)/10.0
        perfect = np.sin(idx)
        notperfect = np.cos(idx)
        
        euclidean_distance =  lambda x,y: np.linalg.norm(x-y)
        d = dtw(query,perfect , dist_method="euclidean")
        print("DTW D=",d.distance)
        
        res = self.do_dtw(query,perfect)
        print("HandCode D =",res)
        #return res
    '''
    # Basic DTW method:
    def do_dtw(self,x,y):
        lenx = len(x)
        leny = len(y)
        
        # Initialization:
        c = np.zeros(shape=(lenx,leny))
        for i in range (lenx):
            for j in range (leny):
                c[i][j] = 999999999
        c[0][0] = 0
        
        # Compute the base roll value:
        for i in range(1,leny):
            c[0,i] = np.linalg.norm(x[0]-y[i])+c[0,i-1]
        for j in range(1,lenx):
            c[j,0] = np.linalg.norm(x[j]-y[0])+c[j-1,0]
        
        # Main loop:
        for i in range (1,lenx):        # For Each Row
            for j in range(1,leny):     # For Each Column
                dist = np.linalg.norm(x[i]-y[j])    # ED distance
                #dist = abs(a[i]-b[j])
                c[i,j] = dist + min(c[i-1,j], c[i,j-1],c[i-1,j-1])
        #res = c
        res = c[lenx-1,leny-1]
        #print("dtw",res)
        return res
    
    # DTW with window:
    def faster_dtw(self,x,y,w = 20):   # Change DTW Window Size HERE
        lenx = len(x)
        leny = len(y)
        w = max(w, abs(lenx-leny))     # adapt the window size
        print ('window : ', w )
        
        # Initialization:
        c = np.zeros(shape=(lenx,leny))
        for i in range (lenx):
            for j in range (leny):
                c[i][j] = 999999999
        
        c[0][0] = 0
        # Compute the base roll value:
        for i in range(1,leny):
            c[0,i] = np.linalg.norm(x[0]-y[i])+c[0,i-1]
        for j in range(1,lenx):
            c[j,0] = np.linalg.norm(x[j]-y[0])+c[j-1,0]
        
        # Window here
        for i in range(1,lenx):
            for j in range ((max(1,i-w)),(min(leny,i+w))):
                c[i][j] = 0
        
        # Main loop:
        for i in range (1,lenx):        # For Each Row
            for j in range((max(1,i-w)),(min(leny, i+w))):     # For Each Column
                dist = np.linalg.norm(x[i]-y[j])        # ED distance
                #dist = abs(a[i]-b[j])
                c[i,j] = dist + min(c[i-1,j], c[i,j-1],c[i-1,j-1])
        #res = c
        res = c[lenx-1,leny-1]
        #print("dtw",res)
        return res


# ==================================  MAIN Function, change INPUT from here =================================
file1 = "Data/acc_walking_csv/3_acc_walking_forearm.csv" # change input file here
file2 = "Data/acc_walking_csv/5_acc_walking_forearm.csv"
a = DTW()
size = 1000    # Change input size here


start = time.time()
a.compare(file1, file2, size) # Basic DTW example
end = time.time()
print('**Run Time: ' + str (end-start) +' s \n')

start2 = time.time()
a.compare(file1, file2, size, True) # DTW with window example, to change the window size, please go up to the main function where marked as "change window size here"
end2 = time.time()
print('**Run Time 2: ' + str (end2-start2) +' s \n')

'''
start = time.time()
a.compare(file1, file2, size)
end = time.time()
print('**Run Time: ' + str (end-start) +' s \n')
'''

# =========  Visualization for presentation only =============================

#print(a.validate(10))
'''
ldist = np.ones((6,6))
ldist[1,:] = 0; ldist[:,4] = 0;
ldist[1,4] = .01; 
print(ldist)
ds = dtw(ldist);  
print(ds.distance)
'''

# ====================== A DTW example presented in PPT where can be validate by hand =============

# Both test will return the colored DTW martrix for hand validation.

# The main DTW function in the previous part are developed based on these two hand computeable example.

def hand_test(a,b):         # Basic DTW without Window, will return a DTW matrix with DTW distance.
    c = np.zeros(shape=(len(a),len(b)))
    
    # Initialization :
    for i in range (len(a)):
        for j in range (len(b)):
            c[i][j] = 999999999
    c[0][0] = 0
    
    # Compute the base roll value:
    for i in range(1,len(b)):
        c[0,i] = np.linalg.norm(a[0]-b[i])+c[0,i-1]
    for j in range(1,len(a)):
        c[j,0] = np.linalg.norm(a[j]-b[0])+c[j-1,0]
        
    # Main DTW:
    for i in range (1,len(a)):      # For Each Row
        for j in range(1,len(b)):       
            dist = np.linalg.norm(a[i]-b[j])   #
            #print("dist",dist)
            #dist = (a[i]-b[j])**2
            c[i,j] = dist + min(c[i-1,j], c[i,j-1],c[i-1,j-1])
    print("dtw",c[len(a)-1,len(b)-1])
    
    # Generate DTW martix: 
    fig, ax = plt.subplots()
    inersection_matrix = c
    for i in range(len(a)):
        for j in range(len(b)):
            d = inersection_matrix[j,i]
            ax.text(i,j,str(d),va='center',ha='center')
    
    ax.matshow(c,cmap=plt.cm.Blues)
    
    '''
    d0 = dtw(a,b,keep_internals=True)
    print(d0.distance)
    d0.plot(type="threeway")
    '''

def hand_test_fast(a,b,w = 0):
    lenx = len(a)
    leny = len(b)
    c = np.zeros(shape=(len(a),len(b)))
    
    w = max(w, abs(lenx-leny)) # adapt the window size
    
    # Initialization :
    for i in range (len(a)):
        for j in range (len(b)):
            c[i][j] = 999999999
    c[0][0] = 0
    
     # Compute the base roll value:
    for i in range(1,len(b)):
        c[0,i] = np.linalg.norm(a[0]-b[i])+c[0,i-1]
    for j in range(1,len(a)):
        c[j,0] = np.linalg.norm(a[j]-b[0])+c[j-1,0]
        
    # Window here
    for i in range(1,lenx):
        for j in range ((max(1,i-w)),(min(leny,i+w))):
                c[i][j] = 0
        
    # DTW with window MAin:
    for i in range (1,len(a)):
        for j in range((max(1,i-w)),(min(leny, i+w))):
            dist = np.linalg.norm(a[i]-b[j])
            #print("dist",dist)
            #dist = (a[i]-b[j])**2
            c[i,j] = dist + min(c[i-1,j], c[i,j-1],c[i-1,j-1])
    print("dtw",c[len(a)-1,len(b)-1])
    
    # Generate DTW martix: 
    fig, ax = plt.subplots()
    inersection_matrix = c
    for i in range(len(a)):
        for j in range(len(b)):
            d = inersection_matrix[j,i]
            ax.text(i,j,str(d),va='center',ha='center')
    
    ax.matshow(c,cmap=plt.cm.Blues)
    '''
    # for graph generation in the presentation only: 
    d0 = dtw(a,b,keep_internals=True)
    print('DTW function:',d0.distance)
    d0.plot(type="threeway")
    '''
    
# ===============DTW simple example with visualization ============
# ============== Here are some simple hand computable examples for validation =====
a = [1,3,4,9,8,2,1,5,7,3]
b = [1,6,2,3,0,9,4,3,6,3]
c = [1,4,10,9,3,2,6,8,4,4]
d = [1,1,4,10,9,3,2,6,8,4]

# Uncomment following parts to see the actual DTW matrix.
'''
print('-------------------------------------------------------')
print('part 2, hand computeable DTW example, details refer to PPT:')
#  Basic DTW:
    
print('Basic DTW example with DTW martix:')
hand_test(a,b)

#----------------

# DTW with window, change w for window size:

print('Windowed DTW example with DTW martix:')
hand_test_fast(a,b,w=2)  

# ----------------

'''







