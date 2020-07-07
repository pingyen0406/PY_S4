# Convert the real and imaginary to phase angle
# This is for 800nm lattice (1 diffraction order)
# Ping-Yen
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os
import sys
import optparse
import yaml
from numpy import dtype

class PY_S4_Analysis_Config:
    """
    PY_S4 configuration class
    """
    # class variables
    sectionName='PY_S4_Analysis'
    options={'height_range': (list,True),
             'radii_range': (list,True),
             'inputFile_T': (str,True),
             'inputFile_E': (str,True),
             'outputPath': (str,True),
            'outputName':(str,True)}
    #constructor
    def __init__(self, inFileName):
        #read YAML config and get EC_Engine section
        infile=open(inFileName,'r')
        ymlcfg=yaml.load(infile)
        infile.close()
        eccfg=ymlcfg.get(self.sectionName,None)
        if eccfg is None: raise Exception('Missing PY_S4 section in cfg file')
         
        #iterate over options
        for opt in self.options:
            if opt in eccfg:
                optval=eccfg[opt]
 
                #verify parameter type
                if type(optval) != self.options[opt][0]:
                    raise Exception('Parameter "{}" has wrong type'.format(opt))
                 
                #create attributes on the fly
                setattr(self,opt,optval)
            else:
                if self.options[opt][1]:
                    raise Exception('Missing mandatory parameter "{}"'.format(opt))
                else:
                    setattr(self,opt,None)
     
    #string representation for class data    
    def __str__(self):
        return str(yaml.dump(self.__dict__,default_flow_style=False))
# Unwrap electric field data
def unwrapPhase(Edata):
    Er = np.real(Edata)
    Ei = np.imag(Edata)
    theta = (np.arctan2(Ei,Er))
    return(theta)
    
def PY_S4_Analysis(cfg):
    infT = np.loadtxt(cfg.inputFile_T,dtype='complex_')
    infE = np.loadtxt(cfg.inputFile_E,dtype='complex_')
    
    N_height = (cfg.height_range[1]-cfg.height_range[0])/cfg.height_range[0] 
    N_radii =  (cfg.radii_range[1]-cfg.radii_range[0])/cfg.radii_range[0]
    
    
    # Plotting transmission data
    T=np.array(infT)
    print(T.shape)
    plt.figure(1)
    plt.imshow(np.log(np.abs(T)),cmap='jet',extent=[100,450,1500,500],aspect='auto')
    plt.colorbar()  
    plt.savefig(cfg.outputPath+'SweepT.png')
 
    # Plotting phase data
    E=np.array(infE)
    phase=np.zeros(shape=E.shape)
    count=0
    print(np.shape(E))
    for line in E:
        phase[count]=unwrapPhase(line)
        count+=1
    plt.figure(2)
    plt.imshow(phase,cmap='jet',extent=[cfg.radii_range[0],cfg.radii_range[1],cfg.height_range[1],cfg.height_range[0]],aspect='auto')
    plt.colorbar()
    plt.savefig(cfg.outputPath+'SweepPhase.png')

    # Save transmission & phase data
    np.savetxt(cfg.outputPath+cfg.outputName+"_T.txt",np.abs(T))
    np.savetxt(cfg.outputPath+cfg.outputName+"_E.txt",phase)
    
def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        #
        # get command-line options
        #
        parser = optparse.OptionParser()
        parser.add_option("-i", "--input", action="store", dest="inputFileName", help="input filename", default=None)
        parser.add_option("-q", "--quiet", action="store_true", dest="quietMode", help="quiet mode", default=False)
        parser.add_option("-d", "--debug", action="store_true", dest="debugMode", help="debug mode", default=False)
        (options, args) = parser.parse_args(argv)
        
        #validate options
        if options.inputFileName is None:
            raise Exception("Must specify input file name using -i or --input option.")
        #Get PY_S4 config params
        cfg=PY_S4_Analysis_Config(options.inputFileName)
    
        #print config params
        print(cfg)
                    
        #run PY_S4
        PY_S4_Analysis(cfg)
        
        if not options.quietMode:                    
            print('PY_S4_Analysis Completed!')    
    
    except Exception as info:
        if 'options' in vars() and options.debugMode:
            from traceback import print_exc
            print_exc()
        else:
            print(info)
    

if __name__ == '__main__':
    main()
    
    
