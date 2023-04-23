import numpy as np
import matplotlib.pyplot as plt
from stl import mesh
import os


filename = input("Please enter the file path of the STL file to be loaded: ")


if not os.path.isfile(filename):
    print("Error: File does not exist.")
    exit()


your_mesh = mesh.Mesh.from_file(filename)


Zmin = np.min(your_mesh.vectors[:,:,2])
Zmax = np.max(your_mesh.vectors[:,:,2])
print(f"Minimum Z value in the mesh is {Zmin}, and maximum Z value is {Zmax}")
while True:
    try:
        z_plane = float(input(f"Please enter a Z plane value between {Zmin} and {Zmax}: "))
        if z_plane < Zmin or z_plane > Zmax:
            print("Error: Z plane value is outside the valid range.")
            continue
        break
    except ValueError:
        print("Error: Invalid input. Please enter a valid Z plane value.")


total_facets = your_mesh.vectors.shape[0]
print(f"Total number of facets in the mesh is {total_facets}.")


i_facets = 0
points = []
for i in range(total_facets):
    facet = your_mesh.vectors[i,:,:]
    z_coords = facet[:,2]
    if np.min(z_coords) <= z_plane and np.max(z_coords) >= z_plane:
        i_facets += 1

        t = (z_plane - facet[0,2])/(facet[2,2]-facet[0,2])
        point = facet[0,:] + t*(facet[2,:]-facet[0,:])
        points.append(point)
print(f"Number of facets intersecting with the Z plane is {i_facets}.")


points = np.array(points)
fig = plt.figure()
ax = fig.add_subplot(111)
points = points.reshape((-1, 2))
ax.scatter(points[:,0], points[:,1], s=10)
ax.set_aspect('equal')
plt.title("2D cross-section of the mesh")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.show()