# Find the appropriate atom size for normal output
# by interpolation.
# Propagation phase bwtweeen 2 atoms(1200nm) = 2.13675*2pi
import numpy as np

# For 800nm lattice : 167nm~255nm
f = open('atom1200Normal2.txt','w')

atom_lib = np.loadtxt('PhaseLib1200.txt')
tmp_W = np.transpose(atom_lib)[0] #meta-atom width
tmp_theta1 = np.transpose(atom_lib)[2] #meta-atom phase library
#tmp_theta2 = np.transpose(atom_lib)[2]
d_W=[]
d_theta=[]
for i in range(0,163,1):
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
d_phi = -(2.13675)
prop_phi=[]
W_list=[]
for i in range(100):    
    prop_phi.append(d_phi*i)
    while prop_phi[i]<-1:
        prop_phi[i]+=1
    w = np.interp(prop_phi[i],d_theta,d_W)
    W_list.append(round(w,3))
print(W_list)

for i in range(100):
    f.write(str(W_list[i])+'\n')
f.close()