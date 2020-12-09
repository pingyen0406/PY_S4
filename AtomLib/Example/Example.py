# 3D meta-atom Library Simulation example
# This example bases on Nat. Commun. 6:7069 doi:10.1038/ncomms8069(2015)
# Ping-Yen
import S4
import numpy as np
import os 
import time
import math

# Define some current path
script_dir = os.path.abspath(os.path.dirname(__file__))
fol_path = script_dir
outf1 = open(os.path.join(fol_path,'Example_T.txt'),'w')
outf2 = open(os.path.join(fol_path,'Example_E.txt'),'w')

# Some parameters
PC_period = 0.8 # period
wavelength=1.55  # operating wavelength 
t_start = time.time() # timer start
# H_atom sweep loop
for h in range (940,942,2):
    print('H_atom = '+str(h)+'nm')
    tmid1 = time.time() # timer of each height loop
    for hole_radius_nm in range(100,275,5):
        hole_radius = hole_radius_nm/1000   # Change unit to um  
    
        S=S4.New(Lattice=((PC_period,0),(PC_period*0.5,PC_period*math.sqrt(3)*0.5)), NumBasis=100) # square lattice
        # Note: NumBasis determines the accuracy and the computation time. 100 is a good start point.
        
        # Material definition
        S.SetMaterial(Name = 'Si', Epsilon = 12.0647) # From Lumerical
        S.SetMaterial(Name = 'a-Si', Epsilon = 11.7649) # From paper       
        S.SetMaterial(Name = 'Vacuum', Epsilon = 1)
        S.SetMaterial(Name = 'glass', Epsilon=2.08514)# SiO2 
        # Material Structure Definition
        t_Si = h/1000 # thickness of silicon layer
        
        # Layer definition(from bottom to top)
        S.AddLayer(
            Name = 'Substrate', 
            Thickness = 0, 
            Material = 'glass')     
        S.AddLayer(
            Name = 'Atom', 
            Thickness = t_Si, 
            Material = 'Vacuum')
        S.AddLayer(
            Name = 'AirAbove', 
            Thickness = 0, 
            Material = 'Vacuum')
        
    # Incident Wave Definition
    # The incident angle is obtain through the Snell's law: n_si*k_0*sin(theta) = n_eff*k_0        
        
        # Note about the "IncidentAngles": 
        # (pair of numbers) Of the form (phi,theta) with angles in degrees. 
        # phi and theta give the spherical coordinate angles of the planewave k-vector. 
        # For zero angles, the k-vector is assumed to be (0, 0, kz), 
        # while the electric field is assumed to be (E0, 0, 0), 
        # and the magnetic field is in (0, H0, 0). 
        # The angle phi specifies first the angle by which the E,H,k frame should be rotated (CW) about the y-axis, 
        # and the angle theta specifies next the angle by which the E,H,k frame should be rotated (CCW) about the z-axis. 
        # Note the different directions of rotations for each angle.
        S.SetExcitationPlanewave(
            IncidenceAngles=(0,0),
            sAmplitude=1,
            pAmplitude=0,
            Order=0)        
    # Calculation of Spectrum
        freq = 1/wavelength
        S.SetFrequency(freq)
    # Set the meta-atom layer have circular post    
        S.SetRegionCircle(
            Layer = 'Atom',
            Material = 'a-Si',
            Center = (0,0),
            Radius = hole_radius)
        # Pick out the transmission and the complex electric field data
        Glist = S.GetBasisSet()
        (forw_P1,back_P1) = S.GetPowerFlux(Layer = 'AirAbove', zOffset = 0)
        (forw_P2,back_P2) = S.GetPowerFlux(Layer = 'Substrate', zOffset = 0)
        (forw_A,back_A) = S.GetAmplitudes(Layer = 'AirAbove', zOffset = 0)
        totalT = forw_P1/forw_P2 # Top emission intensity
              
        # Finding out the index of the maximum forw_A 
        tmp=[]
        for ix in range(len(forw_A)):
            tmp.append(forw_A[ix])
        x = np.abs(tmp)
        s = np.argmax(x)
        outf1.write(str(totalT)+' ')
        outf2.write(str(forw_A[s])+' ')
    tmid2 = time.time()-tmid1 # timer of each height loop
    print('Elasped time for this loop:',tmid2,'s')  
    outf1.write('\n')
    outf2.write('\n')     

outf1.close()
outf2.close()
t_stop=time.time()-t_start # total time
print('Total elapsed time:',t_stop,'s')
    
