import open3d as o3d
import numpy as np
from scipy.spatial import Delaunay


def reconstruire_3D(progress_callback):
    progress_callback.emit(0)

    # Create point cloud from X, Y, Z
    X = np.loadtxt('X_scan.txt')
    Y = np.loadtxt('Y_scan.txt')
    Z = np.loadtxt('Z_scan.txt')

    points = np.array(list(zip(X, Y, Z)))
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)

    # Optional: estimate normals (needed for most reconstruction)
    pcd.estimate_normals()
    mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
        pcd, depth=8
    )

    points_2d = np.column_stack((X, Y))
    tri = Delaunay(points_2d)

    # Use the 3D points for actual mesh vertices
    points_3d = np.column_stack((X, Y, Z))
    triangles = tri.simplices
    # Optionally crop low-density noise
    bbox = pcd.get_axis_aligned_bounding_box()
    mesh = mesh.crop(bbox)

    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(points_3d)
    mesh.triangles = o3d.utility.Vector3iVector(triangles)
    progress_callback.emit(50)

    # Optional cleanup
    mesh.remove_duplicated_vertices()
    mesh.remove_degenerate_triangles()
    mesh.compute_vertex_normals()

    # Save to file
    o3d.io.write_triangle_mesh("output_mesh.obj", mesh)
    progress_callback.emit(80)

    o3d.visualization.draw_geometries([mesh])
    progress_callback.emit(100)



class callback():
   def emit(self, value):
      print(value)


if __name__ == '__main__':
    import os
    basedir = os.path.dirname(__file__)
    os.chdir(basedir)
    os.chdir('..')
    os.chdir('..')
    print(os.getcwd())
    os.chdir('active_files')
    reconstruire_3D(callback())