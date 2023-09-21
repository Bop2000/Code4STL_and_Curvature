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

## CItation

If you find this work interesting, welcome to cite our paper!

```

```
