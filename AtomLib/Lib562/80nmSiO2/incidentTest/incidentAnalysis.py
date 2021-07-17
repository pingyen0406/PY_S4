import numpy as np
import matplotlib.pyplot as plt
import math

phaseList600=np.ndarray((9,100))
phaseList1200=np.ndarray((9,100))
rList = np.array([i for i in range(50,250,2)])

def norPhase(data):
    data-=data[0]
    data/=2*np.pi
    for i in range(len(data)):
        while data[i]<0:
            data[i]+=1
        while data[i]>1:
            data[i]-=1
    return data
            


for i in range(9):
    inf_name = 'incident'+str(i*10)+'_Phase.txt'
    inf = np.loadtxt(inf_name)
    phaseList600[i] = norPhase(inf[10])
    phaseList1200[i] = norPhase(inf[70])
count=0
plt.figure(1)
for line in phaseList1200:
    plt.plot(rList,line,linewidth=2,label=str(10*count))
    plt.title("Height = 1200nm")
    count+=1
plt.legend()
plt.savefig("incident1200.png")
plt.show()
count=0
plt.figure(2)
for line in phaseList600:
    plt.plot(rList,line,linewidth=2,label=str(10*count))
    plt.title("Height = 600nm")
    count+=1
plt.legend()
plt.savefig("incident600.png")
plt.show()