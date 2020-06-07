# Read data of certain H_atom and plotting the figures
import os
import numpy as np
import matplotlib.pyplot as plt

script_dir = os.path.abspath(os.path.dirname(__file__))
fol_path = os.path.join(script_dir,"500nmAl2O3EllipseTEsweep")
phase_path = os.path.join(fol_path,'EllipseLib800sweep_T.txt.txt')
T_path = os.path.join(fol_path,'EllipseLib800sweep_T.txt')


all_T = np.loadtxt(T_path,dtype='complex_')
all_Phase = np.loadtxt(phase_path)
tmp_T = np.zeros(all_T.shape)
for i in range(all_T.shape[0]):
    tmp_T[i] = np.abs(all_T[i])
print(tmp_T)



radius =[]
for r in range(100,300,1):
    radius.append(r)
"""for h in range(900,900,10):
    
    T,Phase = Slicing(h,300)
    plt.figure()
    plt.subplot(121)
    plt.title('Transmission')
    plt.plot(radius,abs(T))

    plt.subplot(122)
    plt.title('Phase')
    plt.plot(radius,Phase,'tab:orange')
    plt.savefig(os.path.join(fol_path,'Slice'+str(h)+'.png'))"""
T = tmp_T
plt.figure()
plt.subplot(121)
plt.title('Transmission')
plt.plot(radius,abs(T))
plt.subplot(122)
plt.title('Phase')
plt.plot(radius,Phase,'tab:orange')
plt.savefig(os.path.join(fol_path,'Slice'+str(500)+'.png'))    
