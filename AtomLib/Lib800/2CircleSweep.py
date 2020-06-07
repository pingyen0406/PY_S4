# 3D meta-atom TIR Library Simulation
# This is for 800nm lattice
# Circular post, fix edge to edge gap = 200nm
# TE
# 
# Ping-Yen 
import S4
import numpy as np
import os
import time
script_dir = os.path.abspath(os.path.dirname(__file__))
fol_path = os.path.join(script_dir,"2CircleTMsweep")
outf1 = open(os.path.join(fol_path,'2CircleSweep_T.txt'),'w')
outf2 = open(os.path.join(fol_path,'2CircleSweep_E.txt'),'w')
PC_period = 0.8
wavelength=1.55  
gap=0.2 # edge to edge gap of 2 posts
# H_atom sweep loop

t_start = time.time()   
for H_post in range(500,1500,10): 
    tmid1 = time.time()  
    print('Height = ',str(H_post),'nm')
    for radius in range(50,350,2):
        
        
            
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
        t_Si = H_post/1000 # thickness of silicon layer
            
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

        r= radius/1000 # Change unit to um
        S.SetRegionCircle(
            Layer = 'Atom',
            Material = 'Si',
            Center = (0,0.5*(2*r+gap)),
            Radius = r
            )
        S.SetRegionCircle(
            Layer = 'Atom',
            Material = 'Si',
            Center = (0,-0.5*(2*r+gap)),
            Radius = r
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
    print('Elasped time for',str(H_post),'nm :',tmid2,'s')    
outf1.close()
outf2.close()
t_stop=time.time()-t_start
print('Total elapsed time:',t_stop,'s')


