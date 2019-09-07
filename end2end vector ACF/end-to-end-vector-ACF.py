#!/usr/bin/python
from __future__ import division
import math,sys,os,subprocess
import string               
import numpy as np
import multiprocessing

##calculate the end-to-end vector autocorrelation function (ACF) for alternating copolymers

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

acfs,num = [0]*nframe, [0]*nframe
tot = int(nframe/2)
for i in range(tot):
    for j in range(i,i+tot):
        bin = j-i
        acf = (np.dot(Vees[i],Vees[j]))/(np.dot(Vees[i],Vees[i]))
        acfs[bin] = acfs[bin]+acf
        num[bin] += 1

for i in range(tot):
    if num[i] != 0:
       acfs[i] = acfs[i]/num[i]
       print >> fout, i*dt, acfs[i]
fout.close()
