import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import math

def EtoPhase(Edata):
    Er = np.real(Edata)
    Ei = np.imag(Edata)
    theta = (np.arctan2(Ei,Er))
    return(theta)
def normalizePhase(phase):
    phase = np.unwrap(phase)
    phase = phase/(2*np.pi)
    for i in range(len(phase)):
        if i==0:
            pass
        else:
            phase[i]-=phase[0]
            while phase[i]<0:
                phase[i]+=1
            # while phase[i]>1:
            #     phase[i]-=1
    phase[0]=0
    return phase

inf_T = np.loadtxt('angleTest_faraon_T0.txt',dtype='complex_')
inf_E = np.loadtxt('angleTest_faraon_E0.txt',dtype='complex_')
RList = np.array([i for i in range(100,275,1)])

plt.figure(1)
count=0
for line in inf_E:
    tmpPhase = normalizePhase(EtoPhase(line))
    plt.plot(RList,tmpPhase,linewidth=2,label=str(count))
    count+=10
plt.xlabel('radius(nm)')
plt.legend()
plt.title('Phase shift of different radius')
plt.savefig('angleTest0_faraon_phase.svg',format='svg',dpi=1200)


plt.figure(2)
count=0
for line in inf_T:
    tmpT = np.abs(line)
    plt.plot(RList,np.log10(tmpT),linewidth=2,label=str(count))
    count+=10
plt.xlabel('radius(nm)')
plt.legend()
plt.title('Transmission of different radius')
plt.savefig('angleTest0_faraon_T.svg',format='svg',dpi=1200)
plt.show()
