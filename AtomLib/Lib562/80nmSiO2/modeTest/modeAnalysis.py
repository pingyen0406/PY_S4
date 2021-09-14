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

TList100 = T_all[:,25]
TList150 = T_all[:,50]
index_peak100, _ = scipy.signal.find_peaks(TList100) 
index_peak150, _ = scipy.signal.find_peaks(TList150)
peak100 = 30*index_peak100+300
peak150 = 30*index_peak150+300

print(peak100)
print(peak150)
plt.figure()
plt.plot(hList,TList100,linewidth=2,label='radius=100')
plt.plot(hList,TList150,linewidth=2,label='radius=150')
plt.xlabel('height(nm)')
plt.legend()
#plt.savefig('0_mode.png')
plt.show()

