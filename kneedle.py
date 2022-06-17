#!/usr/bin/env python
# coding: utf-8
# VML

import os
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import glob
import kneed #name for kneedle algorithm
from kneed import KneeLocator


#Inputs to Change
def filepath():
    FilePath = f'/home/dderedge/Desktop/ENDOS2/ENDOS_Model_A_b_30_optB_{j}x10^{i}_work.dat' #set file path to be used in the rest of the file
    return FilePath
name=("ENDOS2_A") 






























#DON'T TOUCH!... Please :)
li = []
for i in np.arange(-1, 1): # Select the range of gamma (i in j*10^i)
    for j in np.arange(1, 10): # Select the range of gamma (j in j*10^i)
            # Read files containing work values from the smallest to the biggest gamma
            try:
                work = os.path.expandvars(filepath()) #calling the file path function for the directory
                df = pd.read_csv(work, comment='#', header=None, sep='\s+')#reading in the value as listed above
                li.append(df) #appending the data frame
                df = pd.concat(li, axis=0, ignore_index=True) #turning the data frame into a concrete value table
                df.columns = ['gamma', 'MSE', 'RMSE', 'work'] #naming the columns in the data frame as ordered/formated in the .dat files read above
                kneed_x = df['MSE'].values.tolist()#converting the MSE column of the pandas data frame into a list value to be imported into kneedle
                kneed_y = df['work'].values.tolist()#conerting the work column of the pandas data frame into a list value to be imported into kneedle
            except FileNotFoundError:
                pass
print(kneed_x) #quick check to ensure that the list values are correct, and in the proper format
print(kneed_y)

#Creation of the gamma_graph using the kneedle knee locator. Here the important parts are teh sensitivity, curse, direction, and interpolation method.

gamma_graph = KneeLocator(kneed_x, kneed_y, S=1.0, curve="convex", direction="decreasing", interp_method="interp1d") #KneeLocator(x values, y values, sensitivity = , curve = '', direction of curve = '', interp_method='interp1d' or 'polynomial' )

#Creation of Variables for use in the matplotlib ggplot style.

knee_x = gamma_graph.knee
knee_y = gamma_graph.knee_y
z = df.loc[(df['MSE'] == knee_x) & (df['work'] == knee_y)]
ztext = (z['gamma'].to_string(index=False))
xtext = round(gamma_graph.knee, 3)
ytext = round(gamma_graph.knee_y, 3)
gvalue = ("Gamma = " + str(ztext) + " at " + str( [xtext,ytext]))

#Specification of the plot styles, lables, and size.

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
plt.title(str(name) + " Normalized and Difference Decision Graph")
plt.xlabel('MSE')
plt.ylabel('Work Kj/mol')
plt.plot(gamma_graph.x_normalized, gamma_graph.y_normalized, '-o', linewidth=2.5, Label="Normalized")
plt.plot(gamma_graph.x_difference, gamma_graph.y_difference, '-o', linewidth=2.5, Label="Difference")
colors = ["r", "g"]
for k,c,o in zip(
    [gamma_graph.norm_knee], ["black"], ["Knee"]):
    plt.vlines(k, 0, gamma_graph.y_normalized, linestyles="--", colors=c, linewidth=2, label=o)
    plt.legend()
plt.savefig(str(name) + '_Gamma_Norm-Diff.png')

plt.style.use("classic")
plt.figure(figsize=(8, 6))
plt.title(str(name) + " Decission Graph")
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
plt.savefig(str(name) + '_Gamma.png')
