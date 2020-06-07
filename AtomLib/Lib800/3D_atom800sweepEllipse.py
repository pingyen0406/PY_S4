# 3D meta-atom TIR Library Simulation
# This is for 800nm lattice
# Ellipse post, fix one half width = 400nm
# TE
# 
# Ping-Yen 
import S4
import numpy as np
import os
import time
script_dir = os.path.abspath(os.path.dirname(__file__))
fol_path = os.path.join(script_dir,"500nmAl2O3EllipseTMsweep")
outf1 = open(os.path.join(fol_path,'EllipseLib800sweep_T2.txt'),'w')
outf2 = open(os.path.join(fol_path,'EllipseLib800sweep_E2.txt'),'w')
PC_period = 0.8

wavelength=1.55  
# H_atom sweep loop

t_start = time.time()   
for major in range(100,300,2): 
    tmid1 = time.time()
    print('Half major axis = ',str(major),'nm')
    
        
    S=S4.New(Lattice=((PC_period,0),(0,PC_period)), NumBasis=100)
        
    # Material definition
    S.SetMaterial(Name = 'Si', Epsilon = 12.0647)
    # 12.0647 from Lumerical
    # Use 11.7649 for repeating Faraon's paper, 
    # Use 11.2114 from my ellipsometer 20180422 
    S.SetMaterial(Name = 'Fusedsilica', Epsilon = 2.0851)
    S.SetMaterial(Name = 'SU8', Epsilon = 2.4649)
    S.SetMaterial(Name = 'Vacuum', Epsilon = 1)
    S.SetMaterial(Name = 'Al2O3', Epsilon=3.04852)
    # Material Structure Definition
    t_Si = 0.8 # thickness of silicon layer
        
    # Layer definition
    S.AddLayer(
        Name = 'SiBelow', 
        Thickness = 0, 
        Material = 'Si')
    S.AddLayer(
        Name = 'Alumina', 
        Thickness = 0.5, 
        Material = 'Al2O3')       
    S.AddLayer(
        Name = 'Atom', 
        Thickness = t_Si, 
        Material = 'Vacuum')
    S.AddLayer(
        Name = 'AirAbove', 
        Thickness = 0, 
        Material = 'Vacuum')
        
    # Incident Wave Definition
    # For 500nm Alumina, theta=52.544
    S.SetExcitationPlanewave(
        IncidenceAngles=(52.544,0),# (polar in [0,180],azimuthal in [0,360)
        sAmplitude=0,
        pAmplitude=1,
        Order=0)        
    # Calculation of Spectrum
    freq = 1/wavelength
    S.SetFrequency(freq)
    # Radius sweep loop
        
        
    
    for minor in range(300,100,-2):
        a = major/1000
        b = minor/1000 # Change unit to um
        S.SetRegionEllipse(
            Layer = 'Atom',
            Material = 'Si',
            Center = (0,0),
            Angle=0,
            Halfwidths = (a,b)   # halfwidth of (x-axis,y-axis)
            ) 
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
    outf1.write('\n')
    outf2.write('\n') 
    print('Elasped time for this cycle:',tmid2,'s')    
outf1.close()
outf2.close()
t_stop=time.time()-t_start
print('Total elapsed time:',t_stop,'s')


