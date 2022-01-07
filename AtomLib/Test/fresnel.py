# Use Fresnel equation to test the polarization setting
# The light incidents from air to glass
# Ping-Yen
import S4
import numpy as np
import os 
import time
import math
import matplotlib.pyplot as plt

S = S4.New(Lattice=((0,0),(0,0)),NumBasis = 100)
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

n_glass = math.sqrt(2.08514)
phi =90 
Tp_ana = np.zeros(91)
Tp=np.zeros(91)
Rp=np.zeros(91)
Rp_ana=np.zeros(91)
Ts_ana=np.zeros(91)
Ts=np.zeros(91)
Rs=np.zeros(91)
Rs_ana=np.zeros(91)
for i in range(2):
    if i==0:
        input_wave="s"
    else:
        input_wave="p"
    for j in range(91):
        theta_i_deg = j    
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
        (forw_P1,back_P1) = S.GetPowerFlux(Layer = 'Air', zOffset = 0)
        (forw_P2,back_P2) = S.GetPowerFlux(Layer = 'Glass', zOffset = 0)
        (forw_A,back_A) = S.GetAmplitudes(Layer = 'Glass', zOffset = 0)
        (forw_B,back_B) = S.GetAmplitudes(Layer = 'Air',zOffset=0)
        Trans = forw_P2/forw_P1# Transmitance   
        Refl = abs(back_P1/forw_P1) # Reflectance
        # Finding out the index of the maximum forw_A 
        tmp=[]
        for ix in range(len(forw_A)):
            tmp.append(forw_A[ix])
        x = np.abs(tmp)
        s = np.argmax(x)
        
        # Analytical solution for S-wave
        
        if input_wave=="s":
    
            T_coe_s = (2*math.cos(theta_i)/(math.cos(theta_i)+n_glass*math.cos(theta_t)))
            T_ana_s = n_glass*math.cos(theta_t)/math.cos(theta_i)*T_coe_s**2
            Ts[j]= np.real(Trans)
            Rs[j] = np.real(Refl)
            Ts_ana[j] = T_ana_s
            Rs_ana[j] = 1-Ts_ana[j]
        else:
    
            T_coe_p = (2*math.cos(theta_i)/(n_glass*math.cos(theta_i)+math.cos(theta_t)))
            T_ana_p = n_glass*math.cos(theta_t)/math.cos(theta_i)*T_coe_p**2   
            Tp[j] = np.real(Trans)
            Rp[j] = np.real(Refl)
            Tp_ana[j] = T_ana_p
            Rp_ana[j] = 1-Tp_ana[j]
        
theta_list = np.linspace(0,90,91)
plt.figure()
plt.plot(theta_list,Tp,label='Tp-wave')
plt.plot(theta_list,Tp_ana,'--',label='Tp-wave_ana')
plt.plot(theta_list,Rp,label='Rp-wave')
plt.plot(theta_list,Rp_ana,'--',label='Rp-wave_ana')
plt.legend()
axes = plt.gca()
axes.set_xlim([0,90])
axes.set_ylim([0,1])
plt.savefig("Pwave90.png")

plt.figure()
plt.plot(theta_list,Ts,label='Ts-wave')
plt.plot(theta_list,Ts_ana,'--',label='Ts-wave_ana')
plt.plot(theta_list,Rs,label='Rs-wave')
plt.plot(theta_list,Rs_ana,'--',label='Rs-wave_ana')
plt.legend()
axes = plt.gca()
axes.set_xlim([0,90])
axes.set_ylim([0,1])
plt.savefig("Swave90.png")
plt.show()
print(Ts)
print(Rs)

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

    
