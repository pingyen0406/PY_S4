# Convert the real and imaginary to phase angle
# This is for 1200nm lattice (2 diffraction orders)
# Ping-Yen
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from builtins import len
outf = open('PhaseLib1200.txt','w')
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
    return(theta)
    
inf = np.loadtxt('atomLib1200.txt',dtype='complex_')
r = np.real(np.transpose(inf)[0])
tmp = np.transpose(inf)[1]
t = np.zeros(shape=len(tmp))
for i in range(len(tmp)):
    t[i]=np.real(tmp[i])
E1 = np.transpose(inf)[2]# 1st order diffraction
E2 = np.transpose(inf)[3]# 2rd order diffraction
theta1 = NorPhase(E1)
theta2 = NorPhase(E2)
plt.figure()
plt.subplot(1,2,1)
plt.plot(r,t)
plt.title('Transmission')
plt.subplot(1,2,2)
plt.plot(r,theta1,'tab:orange')
plt.title('Phase')
plt.savefig('1200phase1.png')
plt.figure()
plt.subplot(1,2,1)
plt.plot(r,t)
plt.title('Transmission')
plt.subplot(1,2,2)
plt.plot(r,theta2,'tab:orange')
plt.title('Phase')
plt.savefig('1200phase2.png')
for i in range(len(r)):
    outf.write(str(r[i])+' '+str(theta1[i])+' '+str(theta2[i])+' '+str(t[i])+'\n')
outf.close()



