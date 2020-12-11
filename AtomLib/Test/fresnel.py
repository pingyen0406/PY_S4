# Use Fresnel equation to test the polarization setting
# The light incidents from air to glass
# Ping-Yen
import S4
import numpy as np
import os 
import time
import math
import matplotlib.pyplot as plt

S = S4.New(Lattice=((0,0),(0,0)),NumBasis=100)
wavelength=1.55  # operating wavelength 
# H_atom sweep loop
# Material definition
S.SetMaterial(Name = 'Si', Epsilon = 12.0647) # From Lumerical
S.SetMaterial(Name = 'a-Si', Epsilon = 11.7649) # From paper       
S.SetMaterial(Name = 'Vacuum', Epsilon = 1)
S.SetMaterial(Name = 'glass', Epsilon=2.08514)# SiO2 





# Layer definition(from bottom to top)
S.AddLayer(
    Name = 'Air', 
    Thickness = 0, 
    Material = 'Vacuum')     
S.AddLayer(
    Name = 'Glass', 
    Thickness = 0, 
    Material = 'glass')

input_wave = "p"
n_glass = math.sqrt(2.08514)
theta_i_deg = -1
phi =180 
Tp_ana = []
Tp=[]

for i in range(90):
    theta_i_deg+=1

    print("Current input type: ",input_wave,"-wave","(theta,phi)= ("+str(theta_i_deg)+","+str(phi)+")")
    theta_i = math.radians(theta_i_deg)
    sin_t = math.sin(theta_i)/n_glass
    theta_t = math.asin(sin_t)
    if input_wave == "s":   
        S.SetExcitationPlanewave(
            IncidenceAngles=(theta_i_deg,phi),
            sAmplitude=1,
            pAmplitude=0,
            Order=0)       
    else:    
        S.SetExcitationPlanewave(
            IncidenceAngles=(theta_i_deg,phi),
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
    Refl = back_P2 # Reflectance
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
    
    
    Tp.append(Trans)
    Tp_ana.append(T_ana_p)

theta_list = np.linspace(0,89,90)
plt.figure()
plt.plot(theta_list,Tp,theta_list,Tp_ana)
plt.savefig("Test.png")

#print("(forw_glass,back_glass,forw_air,back_air)=  ",forw_P1,back_P1,forw_P2,back_P2,'\n')
#print("Transmittance= ",Trans,'\n')
#if input_wave=="s":
#
#    print("Analytical Transmittance of s-wave= ",T_ana_s,'\n')
#    print("s-wave transmission coefficient",T_coe_s,'\n')
#else:    
#    print("Analytical Transmittance of p-wave= ",T_ana_p,'\n')
#    print("p-wave transmission coefficient",T_coe_p,'\n')
#
#print("Reflectance= ",Refl)
#print("Trans_E= ",forw_A[s])
#print("Back_E= ",back_A)

    
