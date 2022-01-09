import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import math

# Analysis of the mode
# Some values:
# radii_range: [50,252,2]
# height_range: [300,3030,30]

# Consider meta-atom as a FB cavity, and use height difference to find the Neff
def findNeff(T,rList,dr,hList,dh):
    neff=[]
    for r in rList:
        r_index  = int((r-rList[0])/dr)
        TList = T[:,r_index]
        index_peak, _ = scipy.signal.find_peaks(TList) 
        index_diff = np.diff(index_peak)
        avg_diff = 1550/2/np.average(dh*index_diff)
        neff.append(avg_diff)
    return neff

# Read S4 transmission data
infTIR = "modeTestTIR_T.txt"
inf0 = "modeTest0_T.txt"
T_all_0 = np.loadtxt(inf0,dtype='complex_')
T_all_0 = np.abs(np.array(T_all_0))
T_all_TIR = np.loadtxt(infTIR,dtype='complex_')
T_all_TIR = np.abs(np.array(T_all_TIR))
# Create radius and height array
hList = np.array([i for i in range(300,3030,30)])
RList = np.array([i for i in range(50,252,2)])

# Find the Neff of different incident angle
neff_0 = findNeff(T_all_0,RList,2,hList,30)
neff_TIR = findNeff(T_all_TIR,RList,2,hList,30)

# Show the transmission of the 2D sweep(height and radius)
fig = plt.figure(figsize=[8,8])
ax = fig.add_subplot(111)
mainimage = ax.imshow((T_all_0),origin='lower',extent=[RList[0],RList[-1],hList[0]/1000,hList[-1]/1000],cmap=plt.cm.jet,aspect='auto')
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
#plt.savefig('0_mode_sweep.svg',format='svg',dpi=1200)

# Import eigenMode Neff from MODE Solution and compare
inf_Neff = np.loadtxt('eigenMode_sweep.txt',skiprows=1)
eigenRList = np.array([50+3*i for i in range(51)])

# Plot the radius v.s. Neff
plt.figure()
plt.plot(RList,neff_0,linewidth=2,label='normal')
plt.plot(RList,neff_TIR,linewidth=2,label='TIR')
plt.plot(eigenRList,inf_Neff,linewidth=2,label='MODE solution')
plt.xlabel('radius(nm)')
plt.legend()
plt.title('Neff of different radius')
plt.savefig('Neff_compare.svg',format='svg',dpi=1200)
plt.show()

