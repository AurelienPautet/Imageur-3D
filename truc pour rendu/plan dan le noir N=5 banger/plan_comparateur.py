import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.interpolate import griddata


def load_obj_vertices(filename):
    vertices = []
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('v '):
                parts = line.strip().split()
                x, y, z = map(float, parts[1:4])
                vertices.append((x, y, z))
    return np.array(vertices)

basedir = os.path.dirname(__file__)
os.chdir(basedir)
vertices = load_obj_vertices('output_mesh.obj')

x = vertices[:, 0]
y = vertices[:, 1]
z = vertices[:, 2]

#print(x)
#print(y)
#print(z)

res = 1024

xmin, xmax = x.min(), x.max()
ymin, ymax = y.min(), y.max()

xi = np.linspace(xmin, xmax, res)
yi = np.linspace(ymin, ymax, res)
xi, yi = np.meshgrid(xi, yi)

zi = griddata((x, y), z, (xi, yi), method='nearest')
plt.figure(figsize=(8, 6))
plt.imshow(zi, extent=(xmin, xmax, ymin, ymax), origin='lower', cmap='coolwarm')
plt.colorbar(label='Difference de hauteur (mm)')
plt.xlabel('X (mm)')
plt.ylabel('Y (mm)')
plt.title('Difference de hauteur entre plan scanné et plan parfait (z=0)')
plt.axis('equal')
plt.tight_layout()
plt.show()
