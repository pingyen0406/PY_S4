# Modify from the simulation by A. Arbabi, A. FAraon et al., Nature Comm. 8069 (2015) Fig. 1d
import S4

PC_period = 0.8

for hole_radius_nm in range(100, 300, 1):
    hole_radius = hole_radius_nm/1000   # Change unit to um
    wavelength=1.55
    
    S=S4.New(Lattice=((PC_period,0),(PC_period/2,PC_period/2*(3**0.5))), NumBasis=100)
    
    # Material definition
    S.SetMaterial(Name = 'Si', Epsilon = 11.2114)
        # Use 11.7649 for repeating Faraon's paper, 
        # Use 11.2114 from my ellipsometer 20180422 
    S.SetMaterial(Name = 'Fusedsilica', Epsilon = 2.0851)
    S.SetMaterial(Name = 'SU8', Epsilon = 2.4649)
    S.SetMaterial(Name = 'Vacuum', Epsilon = 1)
    
    # Material Structure Definition
    t_Si = 0.99 # thickness of silicon layer
    
    # Layer definition
    S.AddLayer(
            Name = 'AirAbove', 
            Thickness = 0, 
            Material = 'Vacuum')
    S.AddLayer(
            Name = 'Si', 
            Thickness = t_Si, 
            Material = 'Vacuum')
            
    S.SetRegionCircle(
            Layer = 'Si',
            Material = 'Si',
            Center = (0,0),
            Radius = hole_radius)
        
    S.AddLayer(
            Name = 'Bottom', 
            Thickness = 0, 
            Material = 'Fusedsilica')
    
    #Incident Wave Definition    
    S.SetExcitationPlanewave(
            IncidenceAngles=(0,0),   # (theta,phi) in degree
            sAmplitude=0,
            pAmplitude=1,
            Order=0)        
    # Calculation of Spectrum
    freq = 1/wavelength
    S.SetFrequency(freq)
    
    # Calculation
    Glist = S.GetBasisSet()
    (forw_P,back_P) = S.GetPowerFlux(Layer = 'Bottom', zOffset = 0)
    (forw_A,back_A) = S.GetAmplitudes(Layer = 'Bottom', zOffset = 0)
    
    print(str(hole_radius)+ " "+ str(forw_A[0]))
    #print(hole_radius, forw_P)
    #for ix in range(1, len(forw_A)):
    #    print(ix, forw_A[ix-1])
    