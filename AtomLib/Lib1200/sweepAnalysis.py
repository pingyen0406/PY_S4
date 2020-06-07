# Convert the real and imaginary to phase angle
# This is for 800nm lattice (1 diffraction order)
# Ping-Yen
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from cmath import phase


# Unwrapping and normalizing the phase data
def NorPhase(Edata):
    Er = np.real(Edata)
    Ei = np.imag(Edata)
    theta = np.unwrap(np.arctan2(Ei,Er))
    for i in range(len(theta)):
        if i ==0:
            theta[i]=theta[i]
        else:
            theta[i]=(theta[i]-theta[0])/2/np.pi
    theta[0]=0
    for i in range(len(theta)):
        while theta[i]>1:
            theta[i]-=1
        
    return(theta)
    
inf1 = np.loadtxt('atomLib1200sweep_E1.txt',dtype='complex_')
inf2 = np.loadtxt('atomLib1200sweep_T1.txt',dtype='complex_')

# Create radius and height array
R_atom=[]
H_atom=[]

# Plotting transmission data
T=np.array(inf2)
plt.figure(1)
plt.imshow(T.real,vmin=0,vmax=0.00002,cmap='jet',extent=[100,500,1500,500],aspect='auto')
plt.colorbar()
plt.savefig('SweepT1.png')

# Plotting phase data
E=np.array(inf1)
phase=np.zeros(shape=E.shape)
count=0
for line in E:
    phase[count]=NorPhase(line)
    count+=1
plt.figure(2)
plt.imshow(phase,cmap='jet',vmin=0,vmax=1,extent=[100,500,1500,500],aspect='auto')
plt.colorbar()
plt.savefig('SweepPhase1.png')

r=[]
for i in range(100,500,1):
    r.append(i)

plt.figure(3)
plt.plot(r,phase[51])
plt.savefig('test.png')
# Save transmission & phase data
np.savetxt('SweepT1200_1.txt',T.real)
np.savetxt('SweepPhase1200_1.txt',phase)






