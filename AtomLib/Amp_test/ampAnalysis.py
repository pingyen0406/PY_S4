import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os


def EtoPhase(Edata):
    Er = np.real(Edata)
    Ei = np.imag(Edata)
    theta = (np.arctan2(Ei,Er))
    return(theta)
def normalizePhase(phase):
    phase = np.unwrap(phase)
    for i in range(len(phase)):
        if i==0:
            pass
        else:
            phase[i]-=phase[0]
            while phase[i]<0:
                phase[i]+=1
    phase[0]=0
    return phase


