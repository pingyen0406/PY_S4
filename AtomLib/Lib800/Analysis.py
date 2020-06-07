# Convert the real and imaginary to phase angle
# This is for 800nm lattice (1 diffraction order)
# Ping-Yen
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os
#outf = open('PhaseLib800.txt','w')

script_dir=os.path.abspath(os.path.dirname(__file__))
fol_path = os.path.join(script_dir,'500nmAl2O3EllipseTEsweep')
E_path='atomLib800E.txt'
T_path='atomLib800T.txt'
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
    theta[0]=0"""
    return(theta)
    
inf1 = np.loadtxt(T_path,dtype='complex_')
inf2 = np.loadtxt(E_path,dtype='complex_')
r =[]
for radius in range(100,300,2):
    r.append(radius)
tmp=inf1
t=np.zeros(tmp.shape)
for i in range(len(t)):
    t[i]=np.abs(tmp[i])    
for i in range(len(r)):
    print(r[i],t[i])
E1 = inf2# 1st order diffraction
theta1 = NorPhase(E1)
plt.figure()
plt.subplot(1,2,1)
plt.plot(r,t)
plt.title('Transmission')
plt.subplot(1,2,2)
plt.plot(r,theta1,'tab:orange')
plt.title('Phase')

plt.savefig('circleTest.png')
#for i in range(len(r)):
#    outf.write(str(r[i])+' '+str(theta1[i])+' '+str(t[i])+'\n')
#outf.close()



