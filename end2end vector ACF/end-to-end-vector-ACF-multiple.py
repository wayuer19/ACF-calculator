#!/usr/bin/python
from __future__ import division
import math,sys,os,subprocess
import string               
import numpy as np
import multiprocessing

##calculate the end-to-end vector autocorrelation function (ACF) for alternating copolymers

##define the calculatin function   ##apart all the Vees into 50 parts for 50 processes 
def acf_cal(frames):
    acfs,num = [0]*nframe, [0]*nframe
    for i in range(frames,frames+int(tot/n_proc)):
        for j in range(i,i+tot):
            bin = j-i
            acf = (np.dot(Vees[i],Vees[j]))/(np.dot(Vees[i],Vees[i]))
            acfs[bin] = acfs[bin]+acf
            num[bin] += 1
    for i in range(tot):
        if num[i] != 0:
           acfs[i] = acfs[i]/num[i]
    return acfs

##read files and definite varibles
nframe = 50000
dt = 0.02    ##0.02*1000 = 0.02 ns
f = open('acf.xyz','r')
fout = open('acf.dat','w')

## read all the points
lines = []
for line in f.readlines():
    lines.append(line)

Vees = []
for i in range(nframe):
    idx1 = i*4 + 2
    idx2 = idx1 + 1
    line1 = lines[idx1].split()
    line2 = lines[idx2].split()
    Vee = np.array([float(line1[1])-float(line2[1]), float(line1[2])-float(line2[2]), float(line1[3])-float(line2[3])])
    Vees.append(Vee)
f.close()

tot = int(nframe/2)
##multiprocess to calculate acf for each part
n_proc = 50
p = multiprocessing.Pool(processes=n_proc)
frames = []
for i in range(n_proc):
    frame = i*int((tot/n_proc))
    frames.append(frame)
acfs_all = p.map(acf_cal, frames)
p.close()
p.join()

acfs = [0]*tot
for i in range(tot):
    for j in range(n_proc):
        acfs[i] = acfs[i] + acfs_all[j][i]
    acfs[i] = acfs[i]/n_proc
    print >> fout, i*dt, acfs[i]
fout.close()
