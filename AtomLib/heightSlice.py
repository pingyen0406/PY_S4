import matplotlib.pyplot as plt
import numpy as np
import os
from numpy import dtype, linspace
from _operator import length_hint


Einf = np.loadtxt('Lib562/80nmSiO2/sweep562_E.txt',dtype='float')
Tinf = np.loadtxt('Lib562/80nmSiO2/sweep562_T.txt',dtype='float')

height = 1300
row_index = int((height-500)/10)
radii = linspace(100,250,75,endpoint=False)
Eslice = Einf[row_index,25:100]
for i in range(len(Eslice)):
    if i==0:
        pass
    else:
        Eslice[i] = Eslice[i]-Eslice[0]
        if Eslice[i]<0:
            Eslice[i]+=2*np.pi
Eslice[0]=0

plt.figure(1)
plt.plot(radii,Eslice)
plt.savefig('slice.png')