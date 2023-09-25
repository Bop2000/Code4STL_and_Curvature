# Code4STL_and_Curvature
Code for the paper entitled "...".

## Packages

The following libraries are necessary for running the codes.

```shell
trimesh == 3.20.2
pycork
scikit-image == 0.19.3
numpy == 1.19.2
```
Please install requirements using below command.
```
pip install -r requirements.txt
```
which should install in about few minutes.

## Environements
The developmental version of the package has been tested on the following systems and drivers.
- Ubuntu 18.04
- CUDA 11.4
- cuDNN 8.1
- RTX3090 Ti

## Pipeline

To generate three TPMS structures (namely Sheet-Diamond, Sheet-Gyroid, Lattice-Gyroid) in STL format, and estimate the curvature of the corresponding meshes.
Please run the following line in terminal:

```shell
python Para2stl2curvature.py
```
This code is used to create three kinds of TPMS structures and evaluate the curvature of 3D objects with STL file format.
This code can print the information on the surface area and volume fraction with your created TPMS structures. 
To create a TPMS structure with a specific surface area and a specific porosity, you need to change the parameters in such as this line "para=np.array([2.8,0.32])", 
where 2.8 indicates the unit cell size and 0.32 means the isosurface that controls the porosity of the structure.


## CItation

If you find this work interesting, welcome to cite our paper!

```

```
