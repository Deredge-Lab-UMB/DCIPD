#!/usr/bin/env python
# coding: utf-8
# VML
# In[1]:
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import kneed #name for kneedle algorithm
from kneed import KneeLocator
import csv


# In[54]:
def filepath():
    FilePath = f'/home/dderedge/Desktop/ENDOS2/ENDOS_Model_A_b_30_optB_{j}x10^{i}_work.dat' #set file path to be used in the rest of the file
    return FilePath
name=("ENDOS2_A") #Set Name to be used in graph title, file naming, ect

def kneed_plot():
    knee_x = gamma_graph.knee
    knee_y = gamma_graph.knee_y
    z = df.loc[(df['MSE'] == knee_x) & (df['work'] == knee_y)]
    ztext = (z['gamma'].to_string(index=False))
    xtext = round(gamma_graph.knee, 3)
    ytext = round(gamma_graph.knee_y, 3)
    gvalue = ("Gamma = " + str(ztext) + " at " + str( [xtext,ytext]))

    plt.rcParams['axes.labelweight'] = 'bold'
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['axes.titlesize'] = 10
    plt.rcParams['xtick.labelsize'] = 8
    plt.rcParams['ytick.labelsize'] = 8
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['figure.titlesize'] = 12

    plt.style.use("classic")
    plt.figure(figsize=(8, 6))
    plt.title(str(name) + " Snapshot " + "#" + str(count) + " Graph")
    plt.xlabel('MSE')
    plt.ylabel('Work Kj/mol')
    plt.plot(gamma_graph.x, gamma_graph.y,'-o', linewidth=2.5)
    plt.annotate([gvalue], (knee_x, knee_y))
    plt.xlim([gamma_graph.x[-1],gamma_graph.x[0]])
    colors = ["r"]
    for n,t,p in zip(
        [knee_x], ["black"], ["Knee"]):
        plt.vlines(n, 0, gamma_graph.y[-1], linestyles="--", colors=t, linewidth=2, label=p)
        plt.legend()


# In[366]:
count=0

li = []

for j in np.arange(1,10):# Select the range of gamma (j in j*10^i)
    if j <= 10:
        i = -1
        work = os.path.expandvars(filepath()) #directory with the reweighted gamma values
        df = pd.read_csv(work, comment='#', header=None, sep='\s+')#reading in the value as listed above
        li.append(df) #appending the data frame
        df = pd.concat(li, axis=0, ignore_index=True) #turning the data frame into a concrete value table
        df.columns = ['gamma', 'MSE', 'work'] #naming the columns in the data frame as ordered/formated in the .dat files read above
        kneed_x = df['MSE'].values.tolist()#converting the MSE column of the pandas data frame into a list value to be imported into kneedle
        kneed_y = df['work'].values.tolist()#conerting the work column of the pandas data frame into a list value to be imported into kneedle
        t = list([i, j])
        count +=1
    try:
        gamma_graph = KneeLocator(kneed_x[:j], kneed_y[:j], S=1, curve="convex", direction="decreasing", interp_method="interp1d") #KneeLocator(x values, y values, sensitivity = , curve = '', direction of curve = '', interp_method='interp1d' or 'polynomial' )
        knee_x = gamma_graph.knee
        knee_y = gamma_graph.knee_y
        n = df.loc[(df['MSE'] == knee_x) & (df['work'] == knee_y)]
        ntext = (n['gamma'].values.tolist())
        dupli = []
        dupli.append(ntext)
        duplist = []
        for items in dupli:
            duplist.append(items[0])
        kneed_plot()
        plt.savefig(str(name) + "_Snapshot-{}.png".format(t))
    except:
        count -=1
        pass


# In[385]:

count=(count-9)
li2 = []

for i in np.arange(-1,1):
    for j in np.arange(1,10):# Select the range of gamma (j in j*10^i)
        if j <= 10:
            work = os.path.expandvars(filepath()) #directory with the reweighted gamma values
            df = pd.read_csv(work, comment='#', header=None, sep='\s+')#reading in the value as listed above
            li2.append(df) #appending the data frame
            df = pd.concat(li2, axis=0, ignore_index=True) #turning the data frame into a concrete value table
            df.columns = ['gamma', 'MSE', 'work'] #naming the columns in the data frame as ordered/formated in the .dat files read above
            kneed_x = df['MSE'].values.tolist()#converting the MSE column of the pandas data frame into a list value to be imported into kneedle
            kneed_y = df['work'].values.tolist()#conerting the work column of the pandas data frame into a list value to be imported into kneedle
            p = list([i, j])
            count +=1
        try:
            gamma_graph = KneeLocator(kneed_x, kneed_y, S=1, curve="convex", direction="decreasing", interp_method="interp1d") #KneeLocator(x values, y values, sensitivity = , curve = '', direction of curve = '', interp_method='interp1d' or 'polynomial' )
            knee_x = gamma_graph.knee
            knee_y = gamma_graph.knee_y
            n2 = df.loc[(df['MSE'] == knee_x) & (df['work'] == knee_y)]
            ntext2 = (n2['gamma'].values.tolist())
            dupli2 = []
            dupli2.append(ntext2)
            for items in dupli2:
                duplist.append(items[0])
            res = []
            for idx in range(0, len(duplist) - 1):
                  
                # getting Consecutive elements 
                if duplist[idx] == duplist[idx + 1]:
                    res += 1
                else:
                    res = 1  
            if res == 5:
                kneed_plot()
                plt.savefig(str(name) + "_Snapshot-{0}.png".format(p))
                print("5-Rep Gamma Theory Reached")
                sys.exit('5-Rep Gamma Theory Reached')
            elif res < 5:
                kneed_plot()
                plt.savefig(str(name) + "_Snapshot-{0}.png".format(p))
        except:
            pass

                 




