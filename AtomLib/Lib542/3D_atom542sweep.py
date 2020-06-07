# 3D meta-atom TIR Library Simulation
# Ping-Yen 
import S4
import numpy as np
import os 
import time

script_dir = os.path.abspath(os.path.dirname(__file__))
fol_path = os.path.join(script_dir,"60nmAl2O3sweepTE")
outf1 = open(os.path.join(fol_path,'Lib542sweep_T.txt'),'w')
outf2 = open(os.path.join(fol_path,'Lib542sweep_E.txt'),'w')
PC_period = 0.542
h_alumina = 0.06
wavelength=1.55  
t_start = time.time() 
# H_atom sweep loop
for h in range (500,1500,10):
    print('H_atom = '+str(h)+'nm')
    tmid1 = time.time()
    for hole_radius_nm in range(30, 250, 2):
        hole_radius = hole_radius_nm/1000   # Change unit to um  
    
        S=S4.New(Lattice=((PC_period,0),(0,PC_period)), NumBasis=100)
        
        # Material definition
        S.SetMaterial(Name = 'Si', Epsilon = 12.0647)
        S.SetMaterial(Name = 'a-Si', Epsilon = 12.1891)
        # 12.0647 from Lumerical
        # Use 11.7649 for repeating Faraon's paper, 
        # Use 12.1891 from my ellipsometer 20191204 
        S.SetMaterial(Name = 'Fusedsilica', Epsilon = 2.0851)
        S.SetMaterial(Name = 'Vacuum', Epsilon = 1)
        S.SetMaterial(Name = 'Al2O3', Epsilon=3.04852)
        # Material Structure Definition
        t_Si = h/1000 # thickness of silicon layer
        
        # Layer definition
        S.AddLayer(
            Name = 'SiBelow', 
            Thickness = 0, 
            Material = 'Si')
        S.AddLayer(
            Name = 'Alumina_lower', 
            Thickness = h_alumina, 
            Material = 'Al2O3')       
        S.AddLayer(
            Name = 'Atom', 
            Thickness = t_Si, 
            Material = 'Vacuum')
        S.AddLayer(
            Name = 'Alumina_upper', 
            Thickness = h_alumina, 
            Material = 'Al2O3')   
        S.AddLayer(
            Name = 'AirAbove', 
            Thickness = 0, 
            Material = 'Vacuum')
        
    # Incident Wave Definition
    # Slab mode effective index=2.862458 for 500nm Al2O3, theta=37.586
    # Slab mode effective index=2.857184 for 100nm Al2O3, theta=37.67
    # Slab mode effective index=2.851360 for 60nm Al2O3, theta=37.76
    # Neff derived from far field in FDTD is 2.858
        S.SetExcitationPlanewave(
            IncidenceAngles=(37.66,0),# (polar in [0,180],azimuthal in [0,360)
            sAmplitude=1,
            pAmplitude=0,
            Order=0)        
    # Calculation of Spectrum
        freq = 1/wavelength
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
        outf1.write(str(totalT)+' ')
        outf2.write(str(forw_A[s])+' ')
        #print(s,x[s])
        #print(totalT,forw_A[s])
    tmid2 = time.time()-tmid1
    print('Elasped time for this loop:',tmid2,'s')  
    outf1.write('\n')
    outf2.write('\n')     
outf1.close()
outf2.close()
t_stop=time.time()-t_start
print('Total elapsed time:',t_stop,'s')
    