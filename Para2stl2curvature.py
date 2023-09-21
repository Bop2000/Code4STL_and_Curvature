import trimesh
from trimesh.curvature import discrete_gaussian_curvature_measure, discrete_mean_curvature_measure, sphere_ball_intersection
import numpy as np
import time
from numpy import sin, cos, pi
from skimage import measure
import pycork

def tpms_D(x,y,z,para):
    #TPMS_Diamond
    d=abs(np.cos(2*pi*x/para[0])*np.cos(2*pi*y/para[0])*np.cos(2*pi*z/para[0]) + np.sin(2*pi*x/para[0])*np.sin(2*pi*y/para[0])*np.sin(2*pi*z/para[0]) + np.sin(2*pi*x/para[0])*np.cos(2*pi*y/para[0])*np.sin(2*pi*z/para[0]) + np.cos(2*pi*x/para[0])*np.sin(2*pi*y/para[0])*np.sin(2*pi*z/para[0]))-para[1]
    return d

def tpms_G(x,y,z,para):
    #TPMS_Gyroid
    d=abs(np.sin(2*pi*x/para[0])*np.cos(2*pi*y/para[0])+ np.sin(2*pi*y/para[0])*np.cos(2*pi*z/para[0])+ np.sin(2*pi*z/para[0])*np.cos(2*pi*x/para[0]))-para[1]
    return d

def tpms_LG(x,y,z,para):
    #TPMS_Gyroid
    d=np.sin(2*pi*x/para[0])*np.cos(2*pi*y/para[0])+ np.sin(2*pi*y/para[0])*np.cos(2*pi*z/para[0])+ np.sin(2*pi*z/para[0])*np.cos(2*pi*x/para[0])-para[1]
    return d

n_accu=30j    
accu = n_accu.imag
deviation=0.05
a_cell=6

#Input geometry
##################################################################################################
#Basic cube (Comment this block if external geometry is to be used)
total_l = 6e-3  # [m] Length of the prism
total_w = 6e-3  # [m] Width of the prism
total_h = 6e-3  # [m] Height of the prism

#Size and unit corrections
total_l = 1000 * total_l  # Factor to get the correct size
total_w = 1000 * total_w  # Factor to get the correct size
total_h = 1000 * total_h  # Factor to get the correct size
# meshgg=trimesh.primitives.Box(extents=([total_l,total_w,total_h]))
meshgg=trimesh.primitives.Cylinder(radius=3,height=6,section=2000)
meshg = trimesh.parent.Geometry.apply_translation(meshgg,[3.6,3.6,3.6])
total_l = meshg.extents[0]*1.2
total_w = meshg.extents[1]*1.2
total_h = meshg.extents[2]*1.2

##################################################################################################

nx = total_l / a_cell  
ny = total_w / a_cell 
nz = total_h / a_cell 

res = 100j  # 155j ##Resolution of a single unit cell. Number of voxels
reso = res.imag  # Take imaginary part of the "res" variable
#creation with marching cubes
xi, yi, zi = np.mgrid[-total_l/2:total_l/2:res * nx, -total_w/2:total_w/2:res * ny, -total_h/2:total_h/2:res * nz]
xi2, yi2, zi2 = np.mgrid[-3:3:60j,-3:3:60j,-3:3:60j]

def To_stl(para,name):
    if name == 'SD':
        vol= tpms_D(xi,yi,zi,para)
        vol2 = tpms_D(xi2,yi2,zi2,para)
    elif name == 'SG':
        vol= tpms_G(xi,yi,zi,para)
        vol2 = tpms_G(xi2,yi2,zi2,para)
    elif name == 'LG':
        vol= tpms_LG(xi,yi,zi,para)
        vol2 = tpms_LG(xi2,yi2,zi2,para)
    volume=np.where(vol2>=0,0,1)
    mat_RD2=np.sum(volume!=0)/(60*60*60)
    RD=0
    while abs(RD-mat_RD2)/mat_RD2>=deviation:
        #####mesh
        verts, faces, normals, values = measure.marching_cubes(vol,0, spacing=(total_l / (int(nx * reso)-1 ), total_w / (int(ny * reso)-1 ), total_h / (int(nz * reso)-1 )))  # 
        meshf = trimesh.Trimesh(vertices=verts[:], faces=faces[:], vertex_normals=normals[:])
    
        vertsA = meshg.vertices
        trisA = meshg.faces
        vertsB = meshf.vertices
        trisB = meshf.faces
        vertsD, trisD = pycork.intersection(vertsA, trisA,vertsB, trisB)
        meshC = trimesh.Trimesh(vertices=vertsD, faces=trisD, process=False)
        
        # Apply the rotation matrix to the mesh vertices
        meshC.apply_transform(trimesh.transformations.rotation_matrix(np.radians(-90), [0, 0, 1]))##Z
        #Mirror the mesh by scaled the mesh by -1
        meshC.apply_scale([1, -1, 1])
    
        #properties
        area=round((meshC.area),4) #[mm^2] Total surface 
        volume=round((meshC.volume),4) #[mm^2] Total volume 
        RD=meshC.volume/meshg.volume #[%] Volume fraction 
        print("surface area: ",area,"Volume fraction: ",RD,'; dev:',(RD-mat_RD2)/mat_RD2)
        if abs(RD-mat_RD2)/mat_RD2<deviation:
            meshC.export(f'{name}.stl')


###sheet-diamond
para=np.array([2.8,0.32])
name="SD"
To_stl(para,name)
###sheet-gyroid
para=np.array([2.25,0.47])
name="SG"
To_stl(para,name)
###lattice-gyroid
para=np.array([1.1,-0.6])
name="LG"
To_stl(para,name)

radii = 0.1
def curvature_measure(mesh):
    start=time.time()
    mean= discrete_mean_curvature_measure(mesh, mesh.vertices, radii)/sphere_ball_intersection(1, radii)#mean
    end=time.time()
    print("spend time:",(end-start)/60,' min')
    mean=mean.reshape(-1)
    return mean

###curvature of sheet-diamond
mesh1=trimesh.load_mesh("SD.stl", process=True)
cur_SD=curvature_measure(mesh1)

###curvature of sheet-gyroid
mesh2=trimesh.load_mesh("SG.stl", process=True)
cur_SG=curvature_measure(mesh2)

###curvature of lattice-gyroid
mesh3=trimesh.load_mesh("LG.stl", process=True)
cur_LG=curvature_measure(mesh3)
