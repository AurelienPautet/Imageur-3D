import open3d as o3d
import numpy as np

# Create point cloud from X, Y, Z
X = np.loadtxt(r'C:\Users\aurel\OneDrive\Bureau\imageur 3D\qt_app\active_files\X_scan.txt')
Y = np.loadtxt(r'C:\Users\aurel\OneDrive\Bureau\imageur 3D\qt_app\active_files\Y_scan.txt')
Z = np.loadtxt(r'C:\Users\aurel\OneDrive\Bureau\imageur 3D\qt_app\active_files\Z_scan.txt')

points = np.array(list(zip(X, Y, Z)))
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)

# Optional: estimate normals (needed for most reconstruction)
pcd.estimate_normals()
mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
    pcd, depth=8
)

# Optionally crop low-density noise
bbox = pcd.get_axis_aligned_bounding_box()
mesh = mesh.crop(bbox)
o3d.io.write_triangle_mesh("output_mesh.ply", mesh)

#o3d.visualization.draw_geometries([mesh])
