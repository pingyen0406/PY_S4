# Convert the real and imaginary to phase angle
# This is for 800nm lattice (1 diffraction order)
# Ping-Yen
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os

script_dir=os.path.abspath(os.path.dirname(__file__))
# Folder name and input data file name
fol_path = os.path.join(script_dir,'40nmAl2O3sweepTE')
E_path=os.path.join(fol_path,'Lib562sweep_E.txt')
T_path=os.path.join(fol_path,'Lib562sweep_T.txt')
#fEnew = open('100nmAl2O3sweepTE/Enew2.txt','w')
# Unwrapping and normalizing the phase data
def NorPhase(Edata):
    Er = np.real(Edata)
    Ei = np.imag(Edata)
    theta = (np.arctan2(Ei,Er))
    """for i in range(len(theta)):
        if i ==0:
            theta[i]=theta[i]
        else:
            theta[i]=(theta[i]-theta[0])/2/np.pi
    theta[0]=0
    for i in range(len(theta)):
        while theta[i]>1:
            theta[i]-=1
        while theta[i]<0:
            theta[i]+=1"""
    return(theta)
    
inf1 = np.loadtxt(T_path,dtype='complex_')
inf2 = np.loadtxt(E_path,dtype='complex_')

# Create radius and height array
x_axis=[]
y_axis=[]
for i in range(30,250,2):
    x_axis.append(i)
for i in range(500,1500,10):
    y_axis.append(i)

# Plotting transmission data
T=np.array(inf1)
print(T.shape)
plt.figure(1)
plt.imshow(np.abs(T),vmin=0.00000,vmax=0.01,cmap='jet',extent=[30,250,1500,500],aspect='auto')
plt.colorbar()
plt.savefig(os.path.join(fol_path,'SweepT2.png'))


# Plotting phase data
E=np.array(inf2)
Enew = np.zeros(shape=E.shape,dtype='complex_')
phase=np.zeros(shape=E.shape)
count=0
print(np.shape(E))
#for i in range(np.shape(E)[0]):
#    for k in range(np.shape(E)[1]):
#        fEnew.write(str(E[i,k].real)+str(E[i,k].imag)+'j ')
#    fEnew.write('\n')
#print(Enew[1])
for line in E:
    phase[count]=NorPhase(line)
    count+=1
plt.figure(2)
plt.imshow(phase,cmap='jet',extent=[30,250,1500,500],aspect='auto')
plt.colorbar()
plt.savefig(os.path.join(fol_path,'SweepPhase2.png'))
"""
E_tmp=[]
T_tmp=[]
for i in range(0,100,1):
    E_tmp.append(E[i,i])
    T_tmp.append(np.abs(T[i,i]))
E_test = NorPhase(E_tmp)
plt.figure(3)
plt.plot(x_axis[:100],E_test)
plt.savefig(os.path.join(fol_path,'SweepPhaseTest.png'))
plt.figure(4)
plt.plot(x_axis[:100],T_tmp)
plt.savefig(os.path.join(fol_path,'SweepTTest.png'))"""

# Save transmission & phase data
outT_path = os.path.join(fol_path,'SweepT562_2.txt')
outPhase_path=os.path.join(fol_path,'SweepPhase562_2.txt')
np.savetxt(outT_path,np.abs(T))
np.savetxt(outPhase_path,phase)
# Delete the parentheses in the original output E and T datas
#fEnew.close()





