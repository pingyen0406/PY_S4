# Find the appropriate atom size for normal output
# by interpolation.
# Propagation phase bwtweeen 2 atoms(800nm) = 1.4245*2pi
import numpy as np
import os
from matplotlib import pyplot as plt
from Lib800.sweepAnalysis import fol_path

# For 800nm lattice : 167nm~255nm
script_dir = os.path.abspath(os.path.dirname(__file__))
fol_path = os.path.join(script_dir,"500nmAl2O3sweep")
phase_path = os.path.join(fol_path,'SweepPhase800.txt')
f = open(fol_path+'normalOutput.txt','w')


atom_lib = np.loadtxt(phase_path)[31]
tmp_W = [i for i in range(100,300,1)] #meta-atom width
tmp_theta1 = atom_lib#meta-atom phase library

d_W=[]
d_theta=[]
for i in range(66,156,1):
    d_W.append(tmp_W[i])
    d_theta.append(tmp_theta1[i])
for i in range(len(d_theta)):
    if i==0:
        pass        
    else:
        d_theta[i]-=d_theta[0]
d_theta[0]=0
for i in range(len(d_theta)):
    d_theta[i]-=1
print(d_theta)
d_phi = -(1.4245)
prop_phi=[]
W_list=[]
for i in range(100):    
    prop_phi.append(d_phi*i)
    while prop_phi[i]<-1:
        prop_phi[i]+=1
    w = np.interp(prop_phi[i],d_theta,d_W)
    W_list.append(round(w,3))
print(W_list)
"""mp2 = np.zeros(21)
for i in range(21):
    tmp2[i] = np.interp(W_list[i],d_W,d_theta)
plt.plot(tmp2)
plt.savefig(fol_path+'InversePhase.png')"""
for i in range(100):
    f.write(str(W_list[i])+'\n')
f.close()