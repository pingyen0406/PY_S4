# 3D meta-atom Library Simulation example
# This example bases on Nat. Commun. 6:7069 doi:10.1038/ncomms8069(2015)
# Ping-Yen
import S4
import numpy as np
import os 
import time
import math

S = S4.New(Lattice=((0,0),(0,0)),NumBasis=100)
wavelength=1.55  # operating wavelength 
# H_atom sweep loop
# Material definition
S.SetMaterial(Name = 'Si', Epsilon = 12.0647) # From Lumerical
S.SetMaterial(Name = 'a-Si', Epsilon = 11.7649) # From paper       
S.SetMaterial(Name = 'Vacuum', Epsilon = 1)
S.SetMaterial(Name = 'glass', Epsilon=2.08514)# SiO2 



input_wave = "s"
print("Current input type: ",input_wave,"-wave")
n_glass = math.sqrt(2.08514)
theta_i = math.radians(30)
sin_t = math.sin(theta_i)/n_glass
theta_t = math.asin(sin_t)


# Layer definition(from bottom to top)
S.AddLayer(
    Name = 'Air', 
    Thickness = 0, 
    Material = 'Vacuum')     
S.AddLayer(
    Name = 'Glass', 
    Thickness = 0, 
    Material = 'glass')
if input_wave == "s":
        
    S.SetExcitationPlanewave(
        IncidenceAngles=(math.degrees(theta_i),67),
        sAmplitude=1,
        pAmplitude=0,
        Order=0)       
else:

    S.SetExcitationPlanewave(
        IncidenceAngles=(math.degrees(theta_i),0),
        sAmplitude=0,
        pAmplitude=1,
        Order=0)       
# Calculation of Spectrum
freq = 1/wavelength
S.SetFrequency(freq)
Glist = S.GetBasisSet()
(forw_P1,back_P1) = S.GetPowerFlux(Layer = 'Glass', zOffset = 0)
(forw_P2,back_P2) = S.GetPowerFlux(Layer = 'Air', zOffset = 0)
(forw_A,back_A) = S.GetAmplitudes(Layer = 'Glass', zOffset = 0)
(forw_B,back_B) = S.GetAmplitudes(Layer = 'Air',zOffset=0)
Trans = forw_P1/forw_P2 # Transmitance   
Refl = back_P2/forw_P1 # Reflectance
# Finding out the index of the maximum forw_A 
tmp=[]
for ix in range(len(forw_A)):
    tmp.append(forw_A[ix])
x = np.abs(tmp)
s = np.argmax(x)

# Analytical solution for S-wave
T_coe_s = (2*math.cos(theta_i)/(math.cos(theta_i)+n_glass*math.cos(theta_t)))
T_ana_s = n_glass*math.cos(theta_t)/math.cos(theta_i)*T_coe_s**2

T_coe_p = (2*math.cos(theta_i)/(n_glass*math.cos(theta_i)+math.cos(theta_t)))
T_ana_p = n_glass*math.cos(theta_t)/math.cos(theta_i)*T_coe_p**2

print("p-wave transmission coefficient",T_coe_p)
print("s-wave transmission coefficient",T_coe_s)


print("(forw_glass,back_glass,forw_air,back_air)=  ",forw_P1,back_P1,forw_P2,back_P2)
print("Transmittance= ",Trans)
print("Analytical Transmittance of p-wave= ",T_ana_p)
print("Analytical Transmittance of s-wave= ",T_ana_s)
print("Reflectance= ",Refl)
#print("Trans_E= ",forw_A[s])
#print("Back_E= ",back_A)

    
