import open3d as o3d
import numpy as np
from scipy.spatial import Delaunay
from mpl_toolkits.mplot3d import Axes3D

def reconstruire_3D(progress_callback):
    progress_callback.emit(0)

    X = np.loadtxt('X_scan.txt')
    Y = np.loadtxt('Y_scan.txt')
    Z = np.loadtxt('Z_scan.txt')
    
    # Remove aberrant points using Z-score filtering

    points = np.column_stack((X, Y, Z))

# Keep points where all coordinates are within 3 std deviations
    """


    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(X, Y, Z, c='b', marker='o', s=5)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.title('3D Points')
    plt.show()


    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(X, Y, np.zeros_like(Z), c='b', marker='o', s=5)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.title('3D Points')
    plt.show()
    progress_callback.emit(20)
    """
    points_3d = np.column_stack((X, Y, Z))
    points_2d = np.column_stack((X, Y))
    tri = Delaunay(points_2d)
    triangles = tri.simplices
    """
    # Create a version of the mesh where all points are projected onto Z=0
    points_3d_flat = np.column_stack((X, Y, np.zeros_like(Z)))
    mesh_flat = o3d.geometry.TriangleMesh()
    mesh_flat.vertices = o3d.utility.Vector3dVector(points_3d_flat)
    mesh_flat.triangles = o3d.utility.Vector3iVector(triangles)
    progress_callback.emit(50)

    mesh_flat.remove_duplicated_vertices()
    mesh_flat.remove_degenerate_triangles()
    mesh_flat.compute_vertex_normals()

    o3d.io.write_triangle_mesh("output_mesh_flat.obj", mesh_flat)
    progress_callback.emit(80)

    # Visualize the flat mesh with triangle edges
    mesh_flat.compute_vertex_normals()
    # Create a LineSet for triangle edges
    lines = []
    for tri in triangles:
        lines.append([tri[0], tri[1]])
        lines.append([tri[1], tri[2]])
        lines.append([tri[2], tri[0]])
    line_set = o3d.geometry.LineSet(
        points=o3d.utility.Vector3dVector(points_3d_flat),
        lines=o3d.utility.Vector2iVector(lines)
    )
    line_set.colors = o3d.utility.Vector3dVector([[1, 0, 0]] * len(lines))  # Red edges

    o3d.visualization.draw_geometries([mesh_flat, line_set])
    progress_callback.emit(100)
    """
    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(points_3d)
    mesh.triangles = o3d.utility.Vector3iVector(triangles)
    progress_callback.emit(50)

    mesh.remove_duplicated_vertices()
    mesh.remove_degenerate_triangles()
    mesh.compute_vertex_normals()

    o3d.io.write_triangle_mesh("output_mesh.obj", mesh)
    progress_callback.emit(80)

    o3d.visualization.draw_geometries([mesh])
    progress_callback.emit(100)

class callback():
    def emit(self, value):
        print(value)

if __name__ == '__main__':
    import os
    from scipy.stats import zscore
    basedir = os.path.dirname(__file__)
    os.chdir(basedir)
    os.chdir('..')
    os.chdir('..')
    print(os.getcwd())
    os.chdir('active_files')
    reconstruire_3D(callback())
