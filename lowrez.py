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
name=("ENDOS2_A") #Set Name to be used in graph title, file naming, ect


optnum = 1 #What optomization number are you on, change with each run
first_j_values = [1, 4, 7] #start with 1, 4, 7
first_i_value = -1
second_j_values = [1, 4, 7] #start with 1, 4, 7
second_i_value = 0























#DONT TOUCH! YES YOU!
j_lst = first_j_values
df2= []
df4= []
for i in np.arange(first_i_value , (second_i_value+1)):
    if i == first_i_value: 
        for j in np.array(j_lst):
            try:
                work = os.path.expandvars(filepath()) 
                df1 = pd.read_csv(work, comment='#', header=None, sep='\s+')
                df2.append(df1)
                df = pd.concat(df2, axis=0, ignore_index=True)
                df.columns = ['gamma', 'MSE', 'work']
                kneed_x = df['MSE'].values.tolist()#converting the MSE column of the pandas data frame into a list value to be imported into kneedle
                kneed_y = df['work'].values.tolist()#conerting the work column of the pandas data frame into a list value to be imported into kneedle
            except FileNotFoundError:
                pass
    if i == second_i_value:
        j_lst2=second_j_values #specify the j values to test for the EXP(0), good to choose points that would build a simple curve, then adding to optomize
        for j in np.array(j_lst2):
            try:
                work = os.path.expandvars(filepath()) #directory with the reweighted gamma values, ensuring that {j} and {i} are left in for analysis
                df3 = pd.read_csv(work, comment='#', header=None, sep='\s+')#reading in the value as listed above
                df2.append(df3)
                df = pd.concat(df2, axis=0, ignore_index=True)
                df.columns = ['gamma', 'MSE', 'work']
                kneed_x = df['MSE'].values.tolist()#converting the MSE column of the pandas data frame into a list value to be imported into kneedle
                kneed_y = df['work'].values.tolist()#conerting the work column of the pandas data frame into a list value to be imported into kneedle
            except FileNotFoundError:
                pass

        gamma_graph = KneeLocator(kneed_x, kneed_y, S=1.0, curve="convex", direction="decreasing", interp_method="interp1d") #KneeLocator(x values, y values, sensitivity = , curve = '', direction of curve = '', interp_method='interp1d' or 'polynomial' )


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
        plt.title(str(name) + " Low-Rez Optomization " +str(optnum))
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
        plt.savefig(str(name) + '_Low_Rez_' + str(optnum) + '.png') #save the origial plot as a figure (Rename to the thing being analyzed)
        for q in z['gamma']:
            r = df.loc[(df['gamma'] == q)]
            test = np.absolute(np.subtract(r['gamma'], df['gamma']))
            idx = np.argmin(test)
            idx = np.where(df["gamma"][idx] > r, idx-1, idx+1)
            gamma_list1 = list(idx[0])
            gamma_list =gamma_list1[1:]

            for gam in gamma_list:
                New_Gamma_neg1 = []
                New_Gamma_0 = []
                if df['gamma'][gam] < 1.0:
                    if gam < r['gamma'].index.values:
                        coeff1 = 10*(df['gamma'][gam])+1
                        coeff1_2= 10*(df['gamma'][gam])+2
                        New_Gamma_neg1.append(coeff1)
                        New_Gamma_neg1.append(coeff1_2)
                    if gam > r['gamma'].index.values:
                        coeff2 = 10*(df['gamma'][gam])-1
                        coeff2_2 = 10*(df['gamma'][gam])-2
                        New_Gamma_neg1.append(coeff2)
                        New_Gamma_neg1.append(coeff2_2)
                print("New Coefficients for i = -1: " + str(New_Gamma_neg1))
                if df['gamma'][gam] > 1.0 :
                    if gam < r['gamma'].index.values:
                        coeff3 = (df['gamma'][gam])+1
                        coeff3_2= (df['gamma'][gam])+2
                        New_Gamma_0.append(coeff3)
                        New_Gamma_0.append(coeff3_2)
                    if gam > r['gamma'].index.values:
                        coeff4 = (df['gamma'][gam])-1
                        coeff4_2 = (df['gamma'][gam])-2
                        New_Gamma_0.append(coeff4)
                        New_Gamma_0.append(coeff4_2)
                print("New Coefficients for i = 0: " + str(New_Gamma_0))

print("List of All Gamma Values:\n" + df['gamma'].to_string(index=False))
print (gvalue)
