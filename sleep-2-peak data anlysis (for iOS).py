#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 18:19:02 2019

@author: anna
"""
#this cript is for sleep-2-peak data collected using iOS systems

import numpy as np
import pandas as pd
import os

path = '/Users/anna/Desktop/S2P_data_baseline/' #add folder path
folder = os.fsencode(path)
filenames = [] #get filenames
for file in os.listdir(folder):
    filename = os.fsdecode(file)
    if filename.endswith( ('.csv') ):
        filenames.append(filename)

#store results in dataframe "results"
results = pd.DataFrame(columns = ['csv', 'ID', 'lapse','validtrial', 'falsestarts', 'meanRT', 'meanRRT', 'fast10perRT', 'slow10perRRT'])
results['csv'] = pd.Series(filenames)
results['ID'] = results['csv'].astype(str).str[0:5] #your id, depends on how many characters you have

#RRT function
def RRT(x):
    return 1/(x)

# depends on how many data you got, here I have 133 data
for i in range(0,132): 
    infile = filenames[i]
    #read and seperate by ;
    data = pd.read_csv(infile)
    data1 = data[' all_RTs'].str.split(';',expand=True)
    #assign variables names
    data1.columns = ['RT1', 'RT2', 'RT3','RT4','RT5', 'RT6', 'RT7','RT8', 'RT9','RT10', 'RT11', 'RT12', 'RT13', 'RT14', 'RT15', 'RT16', 'RT17', 'RT18', 'ID']
    #drop extra column
    data1 = data1.drop(['ID'],axis=1)
    #extract only the first row(due to not clearing record before collection)
    data2 = data1.iloc[0,0:18].copy()
    #convert object to float
    data2 = data2.convert_objects(convert_numeric=True)
    #calculate mean RT 
    results['meanRT'][i] = data2[(data2<=0.5)&(data2>0.1)].mean() * 1000
    #calculate lapse
    results['lapse'][i] = data2[data2>0.5].count()
    #calculate valid trials
    results['validtrial'][i] = data2[(data2<=0.5)&(data2>0.1)].count()
    #calculate false starts
    results['falsestarts'][i] = data2[data2<=0.1].count()
    #RRT all trials
    RRTdata = RRT(data2)
    #meanRRT
    validata = data2[(data2<=0.5)&(data2>0.1)]
    results['meanRRT'][i] = RRT(validata).mean()
    
    # get fastest 10% RT
    data_t = pd.DataFrame(columns = ['RT','validtrial'])
    data_t['RT'] = data2[(data2<=0.5)&(data2>0.1)]
    data_t['validtrial'] = data2[(data2<=0.5)&(data2>0.1)].count()
    
    if data_t['validtrial'].mean() < 15:
        results['fast10perRT'][i] = data_t['RT'].min() * 1000
    elif data_t['validtrial'].mean() >= 15:
        gv = data_t['RT'].values * 1000
        gv2 = np.sort(gv)
        min2 = (gv2[0] + gv2[1])/2
        results['fast10perRT'][i] = min2
 
    # get slowest 10% RRT
    data_rrt = pd.DataFrame(columns = ['RRT','validtrial'])
    data_rrt['validtrial'] = data_t['validtrial']
    data_rrt['RRT'] = RRT(data2[(data2<=0.5)&(data2>0.1)])
    
    if data_rrt['validtrial'].mean() < 15:
        results['slow10perRRT'][i] = data_rrt['RRT'].min()
    elif data_rrt['validtrial'].mean() >= 15:
        rrtv =  data_rrt['RRT'].values
        rrt = np.sort(rrtv)
        rrt2 = (rrt[0]+rrt[1])/2
        results['slow10perRRT'][i] = rrt2
    
    
#drop column of filenames    
results = results.drop(['csv'],axis=1)


#COMBINE other participant information, optional
cd = '/Users/anna/Desktop/S2P_data_baseline/Add_data'
infile = 'child_CRSP_index.xlsx'
partidata = pd.read_excel(infile, 'Sheet1', index_col= None, na_values=['NA'])

results['ID'] = results['ID'].astype(np.float64)

combine = pd.merge(partidata, results, on='ID')

combine['ID'] = combine['ID'].astype(np.object)

#export csv files
combine.to_csv('results_APPLE_child.csv')
