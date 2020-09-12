# 3D meta-atom TIR Library Simulation
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
             'h_mask': (int,True),
             'epsilon': (float,True),
	         'top_mask': (bool,True),
             'angle': (float,True),
             'outputPath': (str,True),
            'outputName':(str,True)}
    #constructor
    def __init__(self, inFileName):
        #read YAML config and get EC_Engine section
        infile=open(inFileName,'r')
        ymlcfg=yaml.load(infile)
        infile.close()
        pycfg=ymlcfg.get(self.sectionName,None)
        if pycfg is None: raise Exception('Missing PY_S4 section in cfg file')
         
        #iterate over options
        for opt in self.options:
            if opt in pycfg:
                optval=pycfg[opt]
 
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
            S.SetMaterial(Name = 'Si', Epsilon = 12.0647) # From Lumerical
            S.SetMaterial(Name = 'a-Si', Epsilon = 12.1891)# From my ellipsometer 20191204             
            S.SetMaterial(Name = 'Fusedsilica', Epsilon = 2.0851)
            S.SetMaterial(Name = 'Vacuum', Epsilon = 1)
            # epsilon of SiO2 -> 2.09771, Al2O3-> 3.04852
            # I don't chane the name for simplicity
            S.SetMaterial(Name = 'mask', Epsilon=cfg.epsilon) 
                                   
            # Layer definition
            S.AddLayer(
                Name = 'SiBelow', 
                Thickness = 0, 
                Material = 'Si')
            S.AddLayer(
                Name = 'mask_lower', 
                Thickness = cfg.h_mask/1000, 
                Material = 'mask')       
            S.AddLayer(
                Name = 'Atom', 
                Thickness = h, 
                Material = 'Vacuum')
            if (cfg.top_mask==True):
                S.AddLayer(
                    Name = 'mask_upper', 
                    Thickness = cfg.h_mask/1000, 
                    Material = 'mask')   
            S.AddLayer(
                Name = 'AirAbove', 
                Thickness = 0, 
                Material = 'Vacuum')
            
        # Incident Wave Definition
            # Note about the "IncidentAngles": 
            # (pair of numbers) Of the form (phi,theta) with angles in degrees. 
            # phi and theta give the spherical coordinate angles of the planewave k-vector. 
            # For zero angles, the k-vector is assumed to be (0, 0, kz), 
            # while the electric field is assumed to be (E0, 0, 0), 
            # and the magnetic field is in (0, H0, 0). 
            # The angle phi specifies first the angle by which the E,H,k frame should be rotated (CW) about the y-axis, 
            # and the angle theta specifies next the angle by which the E,H,k frame should be rotated (CCW) about the z-axis. 
            # Note the different directions of rotations for each angle.
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

