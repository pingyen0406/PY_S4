# Find the appropriate atom size for spherical wave output
# by interpolation.
# The formula is from "Metalenses at visible wavelengths:
# Diffraction-limited focusing and subwavelength resolution" by F.Capasso
# Propagation phase bwtweeen 2 atoms(800nm) = 1.4245*2pi
import numpy as np
from matplotlib import pyplot as plt
import math
import os
# For 800nm lattice : 167nm~255nm
f = open('atom800Spherical.txt','w')

script_dir = os.path.abspath(os.path.dirname(__file__))
fol_path = os.path.join(script_dir,"Circle/500nmAl2O3sweepTE/")
atom_lib = np.loadtxt('SweepPhase800.txt')
tmp_W = np.transpose(atom_lib)[0] #meta-atom width
tmp_theta1 = np.transpose(atom_lib)[1] #meta-atom phase library

def Slicing(data,height):
    row_index = (height-500)/10
    tmp_data = data[row_index:]
    phase_data=[]
    for i in tmp_data:
        if i<=1:
            phase_data.append(i)
        else:
            break
    return phase_data
    

d_W=[]
d_theta=[]
lib1 = Slicing(atom_lib,1400)

