# PY_S4
The project is based on https://github.com/victorliu/S4. The S4 package with python API should be installed first.
This project is used for the sweep of cylinder-shaped meta-atom library. But it can be modified to other shape.
***
## Basic usage
### To run the sweep
$ python3 atom_sweep.py -i <input_parameters.yml>
### To analysis the data
$ python3 sweepAnalysis.py -i <input_parameters.yml>
***
## atom_sweep.py input parameters
The input argument or the structure can be easily modified. Here is an example of mine.
Sweep of 562nm period meta-atom library with SiO2 hardmask.
All unit in "nm"
```
PY_S4:
        period: 562
        radii_range: [50,250,2]
        height_range: [500,1500,10]
        wavelength: 1550
        h_mask: 60 # thickness of the mask
        epsilon: 2.09771 # mask permitivity
        top_mask: True # top mask or not
        angle: 35.236 # Input plane wave angle
        outputPath: <The_path_you_want_to_save_the_E&T_datas>
        outputName: <Output_filename> # Output .txt file of electric and transmission datas
```
## Analysis.py input argument
The analysis input argument can be modified. My example here plot the phase and transmission data and output the transmission and phase data.
Unit in "nm"
```
PY_S4_Analysis:
        radii_range: [50,250,2]
        height_range: [500,1500,10]
        inputFile_T: <The_transmission_data_from_atom_sweep>
        inputFile_E: <The_electric_field_data_from_atom_sweep>
        outputPath: <The_path_you_want_to_save_the_plots>
        outputName: <Output_filename> # Output .txt file of phase and transmission datas
```
