# 3D meta-atom TIR Library Simulation
# This is for 800nm lattice
# Ping-Yen 
import S4
import numpy as np
import time
import optparse
import yaml
import sys
#
class PY_S4_Config:
    """
    PY_S4 configuration class
    """
    # class variables
    sectionName='PY_S4'
    options={'period': (int,True),
             'radii_range': (list,True),
             'height_range': (list,True),
             'wavelength': (int,True),
             'h_alumina': (int,True),
             'angle': (float,True),
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

def PY_S4(cfg):
    outfT = open(cfg.outputPath+cfg.outputName+"_T.txt",'w')
    outfE = open(cfg.outputPath+cfg.outputName+"_E.txt",'w')      
    t_start = time.time() 
    for h in range (cfg.height_range[0],cfg.height_range[1],cfg.height_range[2]):
        print('H_atom = '+str(h)+'nm')
        h = h/1000
        tmid1 = time.time()
        for hole_radius in range(cfg.radii_range[0],cfg.radii_range[1],cfg.radii_range[2]):        
            hole_radius = hole_radius/1000
            S=S4.New(Lattice=((cfg.period/1000,0),(0,cfg.period/1000)), NumBasis=100)
            
            # Material definition
            S.SetMaterial(Name = 'Si', Epsilon = 12.0647)
            S.SetMaterial(Name = 'a-Si', Epsilon = 12.1891)
            # 12.0647 from Lumerical
            # Use 11.7649 for repeating Faraon's paper, 
            # Use 12.1891 from my ellipsometer 20191204 
            S.SetMaterial(Name = 'Fusedsilica', Epsilon = 2.0851)
            S.SetMaterial(Name = 'Vacuum', Epsilon = 1)
            # epsilon of SiO2 -> 2.09771, Al2O3-> 3.04852
            # I don't chane the name for simplicity
            S.SetMaterial(Name = 'Al2O3', Epsilon=2.09771) 
                                   
            # Layer definition
            S.AddLayer(
                Name = 'SiBelow', 
                Thickness = 0, 
                Material = 'Si')
            S.AddLayer(
                Name = 'Alumina_lower', 
                Thickness = cfg.h_alumina/1000, 
                Material = 'Al2O3')       
            S.AddLayer(
                Name = 'Atom', 
                Thickness = h, 
                Material = 'Vacuum')
            S.AddLayer(
                Name = 'Alumina_upper', 
                Thickness = cfg.h_alumina/1000, 
                Material = 'Al2O3')   
            S.AddLayer(
                Name = 'AirAbove', 
                Thickness = 0, 
                Material = 'Vacuum')
            
        # Incident Wave Definition
        # Slab mode effective index=2.862458 for 500nm Al2O3, theta=37.586
        # Slab mode effective index=2.857184 for 100nm Al2O3, theta=37.67
        # Slab mode effective index=2.851360 for 60nm Al2O3, theta=37.76
        # Slab mode effective index=2.846334 for 40nm Al2O3, theta=37.83
            S.SetExcitationPlanewave(
                IncidenceAngles=(cfg.angle,0),# (polar in [0,180],azimuthal in [0,360)
                sAmplitude=1,
                pAmplitude=0,
                Order=0)        
        # Calculation of Spectrum
            freq = 1/cfg.wavelength*1000
            S.SetFrequency(freq)
        # Radius sweep loop
          
            S.SetRegionCircle(
                Layer = 'Atom',
                Material = 'a-Si',
                Center = (0,0),
                Radius = hole_radius)
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
            outfT.write(str(totalT)+' ')
            outfE.write(str(forw_A[s])+' ')
            #print(s,x[s])
            #print(totalT,forw_A[s])
        tmid2 = time.time()-tmid1
        print('Elasped time for this loop:',tmid2,'s')  
        outfT.write('\n')
        outfE.write('\n')     
    outfT.close()
    outfE.close()
    t_stop=time.time()-t_start
    print('Total elapsed time:',t_stop,'s')
    

         
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
        cfg=PY_S4_Config(options.inputFileName)
    
        #print config params
        print(cfg)
                    
        #run PY_S4
        PY_S4(cfg)
        
        if not options.quietMode:                    
            print('PY_S4 Completed!')    
    
    except Exception as info:
        if 'options' in vars() and options.debugMode:
            from traceback import print_exc
            print_exc()
        else:
            print(info)
    

if __name__ == '__main__':
    main()

