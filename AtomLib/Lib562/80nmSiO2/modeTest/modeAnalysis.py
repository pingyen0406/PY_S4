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
RList = np.array([i for i in range(50,250,2)])
for r in RList:
    r_index  = int((r-50)/2)
    TList = T_all[:,r_index]
    index_peak, _ = scipy.signal.find_peaks(TList) 
    index_diff = np.diff(index_peak)
    avg_diff = 1550/2/np.average(30*index_diff)
    neff1.append(avg_diff)

fig = plt.figure(figsize=[8,8])
ax = fig.add_subplot(111)
mainimage = ax.imshow(np.log10(T_all),origin='lower',extent=[RList[0],RList[-1],hList[0]/1000,hList[-1]/1000],cmap=plt.cm.jet,aspect='auto')
ax.set_xlabel(xlabel='radius (nm)',fontsize=20)
ax.set_xticks([50,100,150,200,250])
ax.xaxis.set_tick_params(length=6,width=3)
plt.xticks(fontsize=18)
ax.set_ylabel(ylabel='height (\u03bcm)',fontsize=20)
ax.set_yticks([0.5,1,1.5,2,2.5,3])
ax.yaxis.set_tick_params(length=6,width=3)
plt.yticks(fontsize=18)
cbar = fig.colorbar(mainimage,aspect=40)
cbar.ax.set_title(label='Intensity(a.u.)',pad=20,size=16)
cbar.ax.tick_params(labelsize=16,length=5,width=2)
#plt.tight_layout()
#plt.show()
plt.savefig('0_mode_sweep.svg',format='svg',dpi=1200)


plt.figure()
plt.plot(RList,neff0,linewidth=2,label='normal')
plt.plot(RList,neff1,linewidth=2,label='TIR')
plt.xlabel('radius(nm)')
plt.legend()
plt.title('Neff of different radius')
plt.savefig('0_mode.svg',format='svg',dpi=1200)
plt.show()

