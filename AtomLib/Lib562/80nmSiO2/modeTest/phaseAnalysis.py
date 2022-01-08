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
            # while phase[i]<0:
            #     phase[i]+=1
            # while phase[i]>1:
            #     phase[i]-=1
    phase[0]=0
    return phase

# Read S4 transmission data
infTIR = "modeTestTIR_E.txt"
inf0 = "modeTest0_E.txt"
Phase_all_0 = np.loadtxt(inf0,dtype='complex_')
Phase_all_TIR = np.loadtxt(infTIR,dtype='complex_')
# Create radius and height array
hList = np.array([i for i in range(300,3030,30)])
RList = np.array([i for i in range(50,252,2)])
h_index = int((1200-300)/30)

Phase_0 = normalizePhase(EtoPhase(Phase_all_0[h_index,:]))
Phase_TIR = normalizePhase(EtoPhase(Phase_all_TIR[h_index,:]))

plt.figure()
plt.plot(RList,Phase_0,linewidth=2,label='normal')
plt.plot(RList,Phase_TIR,linewidth=2,label='TIR')
plt.legend()
plt.savefig('PhaseComparison.svg',format='svg',dpi=1200)
plt.show()




