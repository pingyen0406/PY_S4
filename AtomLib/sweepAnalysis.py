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
            'outputName':(str,True),
            'Data':(str,True)       }
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
    
def PY_S4_Analysis(cfg):
    infT = np.loadtxt(cfg.inputFile_T,dtype='complex_')
    infE = np.loadtxt(cfg.inputFile_E,dtype='complex_')
    r_max = cfg.radii_range[1]
    r_min = cfg.radii_range[0]
    h_max = cfg.height_range[1]
    h_min = cfg.height_range[0]
    N_height = (h_max-h_min)/cfg.height_range[2] 
    N_radii =  (r_max-r_min)/cfg.radii_range[2]
    radii_list = np.transpose(np.array([range(cfg.radii_range[0],cfg.radii_range[1],cfg.radii_range[2])]))
    print(radii_list.shape) 
    if cfg.Data=="2D":

        # plotting transmission data
        t=np.array(infT)
        print(t.shape)
        plt.figure(1)
        plt.imshow((np.abs(t)),cmap='jet',extent=[r_min,r_max,h_max,h_min],aspect='auto')
        c1 = plt.colorbar()
        c1.set_label("log scale(a.u.)",fontsize=20)
        c1.ax.tick_params(labelsize=20) 
        plt.xlabel("radius(nm)",fontsize=25)
        #plt.xticks([r_min,0.5*(r_min+r_max),r_max],fontsize=20)
        plt.ylabel("height(nm)",fontsize=25)
        #plt.yticks([500,750,1000,1250,1500],fontsize=20)
        plt.title("top emission intensity",fontsize=25)  
        plt.savefig(cfg.outputPath+cfg.outputName+'T.png',bbox_inches='tight')
 
        # plotting phase data
        e=np.array(infE)
        phase=np.zeros(shape=e.shape)
        count=0
        print(np.shape(e))
        for line in e:
            phase[count]=EtoPhase(line)
            count+=1
        plt.figure(2)
        plt.imshow(phase/np.pi,cmap='jet',extent=[r_min,r_max,h_max,h_min],aspect='auto')
        c2 = plt.colorbar()
        c2.set_label("rad",fontsize=20)
        #c2.ax.set_yticklabels(['-\u03c0',0,'\u03c0']) 
        c2.ax.tick_params(labelsize=20) 
        #plt.xticks([r_min,0.5*(r_min+r_max),r_max],fontsize=20)
        plt.xlabel("radius(nm)",fontsize=25)
        #plt.yticks([500,750,1000,1250,1500],fontsize=20)
        plt.ylabel("height(nm)",fontsize=25)
        plt.title("phase",fontsize=25)  
        plt.savefig(cfg.outputPath+cfg.outputName+'Phase.png',bbox_inches='tight')
    else:
        # plotting transmission data
        t=np.array(infT)
        print(t.shape)
        plt.figure(1)
        plt.plot(radii_list,(np.abs(t)))
        plt.xlabel("radius(nm)",fontsize=25)
        plt.ylabel("T",fontsize=25)
        plt.savefig(cfg.outputPath+cfg.outputName+'T.png',bbox_inches='tight')
 
        # plotting phase data
        e=np.array(infE)
        phase=np.zeros(shape=e.shape)
        
        count=0
        print(np.shape(e))
        for line in e:
            phase[count]=EtoPhase(line)
            count+=1
        phase = normalizePhase(phase)/2/np.pi
        #phase = np.unwrap(phase*2*np.pi)

        plt.figure(2)
        plt.plot(radii_list,phase)
        plt.xlabel("radius(nm)",fontsize=25)
        plt.title("phase",fontsize=25)  
        plt.savefig(cfg.outputPath+'sweepphase.png',bbox_inches='tight')
 
       
    # Save transmission & phase data
    np.savetxt(cfg.outputPath+cfg.outputName+"_T.txt",np.abs(t))
    np.savetxt(cfg.outputPath+cfg.outputName+"_Phase.txt",phase)
    
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
    
    
