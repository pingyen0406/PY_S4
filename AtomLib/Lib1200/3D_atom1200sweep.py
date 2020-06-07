# 3D meta-atom TIR Library Simulation
# Lattice = 1200nm
# Ping-Yen 
import S4
import numpy as np
import time
#outf1 = open('atomLib1200sweep_T1.txt','w')
#outf2 = open('atomLib1200sweep_E1.txt','w')
PC_period = 1.2
start= time.time()
wavelength=1.55 
for h in range (1000,1500,10): 
    print('H_atom = '+str(h)+'nm')
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
    t_Si = h/1000 # thickness of silicon layer
    
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
    
#Incident Wave Definition    
    S.SetExcitationPlanewave(
        IncidenceAngles=(52.544,0),# (polar in [0,180],azimuthal in [0,360)
        sAmplitude=0,
        pAmplitude=1,
        Order=0)        
# Calculation of Spectrum
    freq = 1/wavelength
    S.SetFrequency(freq)
# Running radius sweep and getting data
    for hole_radius_nm in range(500, 501, 1):
        hole_radius = hole_radius_nm/1000   # Change unit to um    
        S.SetRegionCircle(
            Layer = 'Atom',
            Material = 'Si',
            Center = (0,0),
            Radius = hole_radius)
    # Calculation
        Glist = S.GetBasisSet()
        (forw_P1,back_P1) = S.GetPowerFlux(Layer = 'AirAbove', zOffset = 0)
        (forw_P2,back_P2) = S.GetPowerFlux(Layer = 'SiBelow', zOffset = 0)
        (forw_A,back_A) = S.GetAmplitudes(Layer = 'AirAbove', zOffset = 0)
        totalT = forw_P1/forw_P2
        tmp=[]    
        for ix in range(len(forw_A)):
            #print(ix,forw_A[ix])
            tmp.append(forw_A[ix])
        x = np.abs(tmp)
        s = np.argmax(x)
        print(s,x[s])
        #y = np.delete(x,s)
        #print(y[s])
        #print(np.argmax(y),y[np.argmax(y)])
        #outf1.write(str(totalT) +' ')
        #outf2.write(str(forw_A[s])+' ')
        print(hole_radius,totalT,forw_A[s])
    #outf1.write('\n')
    #outf2.write('\n')
#outf1.close()
#outf2.close()
end=time.time()
print(end-)