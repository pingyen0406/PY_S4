# 3D meta-atom TIR Library Simulation
# Lattice = 1200nm
# Ping-Yen 
import S4
import numpy as np

outf = open('atomLib1200.txt','w')
PC_period = 1.2

wavelength=1.55  
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
t_Si = 1 # thickness of silicon layer
    
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
# For 1200nm lattice
# maximum E field is in 99th & 100th and 118th & 120th order diffraction
# For 800nm lattice
# maximum E field is in 99th order diffraction
for hole_radius_nm in range(100, 500, 1):
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
    outf.write(str(hole_radius)+' '+str(totalT)+' '+ str(forw_A[107])+' '+str(forw_A[125])+'\n')
    print(hole_radius,totalT,forw_A[107])
    tmp=[]
    """for ix in range(len(forw_A)):
        print(ix,forw_A[ix])
        tmp.append(forw_A[ix])
    x = np.real(tmp)
    s = np.argmax(x)
    print(s,x[s])
    y = np.delete(x,s)
    print(y[s])
    print(np.argmax(y),y[np.argmax(y)])"""
outf.close()
    