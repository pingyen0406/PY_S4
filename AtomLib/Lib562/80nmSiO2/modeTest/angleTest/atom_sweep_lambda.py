# 3D meta-atom Library Simulation with different incident angle
# Ping-Yen 
import S4
import numpy as np
import time
import math
#
period = 562
h_mask = 80
h_atom = 1200
wavelength = 1550
t_start = time.time() 
angle = [10*i for i in range(11)]
for theta in angle:
    tmid1 = time.time()
    outfT = open('thetaTest_'+str(angle)+'_T.txt','w')
    outfE = open('thetaTest_'+str(angle)+'_E.txt','w')      
    
    for hole_radius in range(50,252,2):        
        hole_radius = hole_radius/1000
        S=S4.New(Lattice=((period/1000,0),(0,period/1000)), NumBasis=100)
        
        # Material definition
        S.SetMaterial(Name = 'Si', Epsilon = 12.0647) # From Lumerical
        S.SetMaterial(Name = 'a-Si', Epsilon = 12.1891)# From my ellipsometer 20191204             
        S.SetMaterial(Name = 'Fusedsilica', Epsilon = 2.0851)
        S.SetMaterial(Name = 'Vacuum', Epsilon = 1)
        # epsilon of SiO2 -> 2.09771, Al2O3-> 3.04852
        # I don't chane the name for simplicity
        S.SetMaterial(Name = 'mask', Epsilon=cfg.epsilon) 
                            
        # Layer definition
        S.AddLayer(
            Name = 'SiBelow', 
            Thickness = 0,
    Material = 'Si')
        S.AddLayer(
            Name = 'mask_lower', 
            Thickness = h_mask/1000, 
            Material = 'mask')       
        S.AddLayer(
            Name = 'Atom', 
            Thickness = h_atom/1000, 
            Material = 'Vacuum')
        S.AddLayer(
            Name = 'mask_upper', 
            Thickness = h_mask/1000, 
            Material = 'mask')   
        S.AddLayer(
            Name = 'AirAbove', 
            Thickness = 0, 
            Material = 'Vacuum')
        
    # Incident Wave Definition
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
            IncidenceAngles=(angle,0),# (polar in [0,180],azimuthal in [0,360)
            sAmplitude=1,
            pAmplitude=0,
            Order=0)        
    # Calculation of Spectrum
        freq = 1/wavelength*1000
        S.SetFrequency(freq)
    # Radius sweep loop
    
        S.SetRegionCircle(
            Layer = 'Atom',
            Material = 'a-Si',
            Center = (0,0),
            Radius = hole_radius)
        # Calculation
        Glist = S.GetBasisSet()
        (forw_P1,back_P1) = S.GetPowerFlux(Layer = 'AirAbove', zOffset = 0)
        (forw_P2,back_P2) = S.GetPowerFlux(Layer = 'SiBelow', zOffset = 0)
        (forw_A,back_A) = S.GetAmplitudes(Layer = 'AirAbove', zOffset = 0)
        totalT = forw_P1/forw_P2
            
        # Finding out the index of the maximum forw_A 
        tmp=[]
        for ix in range(len(forw_A)):
            #print(ix,forw_A[ix])
            tmp.append(forw_A[ix])
        
        x = np.abs(tmp)
        s = np.argmax(x)
        #print(forw_A[s])
        outfT.write(str(totalT)+' ')
        outfE.write(str(forw_A[s])+' ')
        
        #print(s,x[s])
        #print(totalT,forw_A[s])
    tmid2 = time.time()-tmid1
    print('Elasped time for this loop:',tmid2,'s')  
    outfT.write('\n')
    outfE.write('\n')     
outfT.close()
outfE.close()
t_stop=time.time()-t_start
print('Total elapsed time:',t_stop,'s')
    

    
