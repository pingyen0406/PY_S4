import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import math

# Analysis of the mode
# Some values:
# radii_range: [50,250,2]
# height_range: [300,3000,30]

#infName = "modeTest0_T.txt"
infName = "modeTestTIR_T.txt"
T_all = np.loadtxt(infName)
print(T_all.shape)
hList = np.array([i for i in range(300,3000,30)])
RList = np.array([i for i in range(50,250,2)])
print(RList)

neff0 = []
neff1=[]
for r in RList:
    r_index  = int((r-50)/2)
    TList = T_all[:,r_index]
    index_peak, _ = scipy.signal.find_peaks(TList) 
    index_diff = np.diff(index_peak)
    avg_diff = 1550/2/np.average(30*index_diff)
    neff0.append(avg_diff)
infName = "modeTestTIR_T.txt"
T_all = np.loadtxt(infName)
hList = np.array([i for i in range(300,3000,30)])
RList = np.array([i for i in range(50,210,10)])
for r in RList:
    r_index  = int((r-50)/2)
    TList = T_all[:,r_index]
    index_peak, _ = scipy.signal.find_peaks(TList) 
    index_diff = np.diff(index_peak)
    avg_diff = 1550/2/np.average(30*index_diff)
    neff1.append(avg_diff)


plt.figure()
plt.plot(RList,neff0,linewidth=2,label='normal')
plt.plot(RList,neff1,linewidth=2,label='TIR')
plt.xlabel('radius(nm)')
plt.legend()
plt.title('Neff of different radius')
#plt.savefig('0_mode.png')
plt.show()

