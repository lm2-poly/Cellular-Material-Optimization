#from geomdl.visualization import VisMPL
import numpy as np
import matplotlib.pyplot as plt
import os, os.path
from geomdl import BSpline
from geomdl import utilities
import time
import math


# 6 variables to optimize so far
def DensityFunction(x0):
    # Root path
    root_path = os.getcwd()


    # Control points
    # Variable to optimize would be the height of the 36 control points representing the density function.
    #n = len(x0)
    half_panel = 85
    resolution = 600  # was 80 then 600
    #ctrlpts = []
    #if (n % 2) == 0:
    #    for subd in n:
    #        ctrlpts.append[[-half_panel, -half_panel, x0[0]]]

    n_vars = 8
    num_arr = 8       # must be how much ? Amount of arrays fct of variables: 21=6, 15=5, 10=4, etc.
    ctrlpts = list()
    x_min_bound = -85
    x_max_bound = 85
    y_min_bound = -85
    y_max_bound = 85

    sym = dict()
    # Ici, on vient créer les positions d'un cadran du problème
    s = 0
    for i in range(num_arr):
        for j in range(num_arr):
            if i >= j:
                sym[str(i) + " " + str(j)] = x0[s]
                s += 1

    inc = (85 - 0.01)/(num_arr-1)     # -1 since it's odd (-0.01 for rounding errors)
    for i in range(-num_arr + 1, num_arr):     #(-math.floor((n_vars-1)/2), math.floor(n_vars/2) + 1):
        temp = list()
        for j in range(-num_arr + 1, num_arr):     #-math.floor((n_vars-1)/2), math.floor(n_vars/2) + 1):
            if abs(j) <= abs(i):
                key = str(abs(i)) + " " + str(abs(j))
                coords_dict = sym[key]
            else:
                key = str(abs(j)) + " " + str(abs(i))
                coords_dict = sym[key]  # abs because of symmetry

            temp.append([inc*i, inc*j, coords_dict])
        ctrlpts.append(temp)

    # Create a BSpline surface
    surf = BSpline.Surface()

    # Set degrees
    surf.degree_u = 2
    surf.degree_v = 2

    # Set control points
    surf.ctrlpts2d = ctrlpts

    surf.knotvector_u = utilities.generate_knot_vector(surf.degree_u, surf.ctrlpts_size_u)
    surf.knotvector_v = utilities.generate_knot_vector(surf.degree_v, surf.ctrlpts_size_v)

    # Set evaluation delta
    surf.delta = 0.025

    # Define a function for cm (colormap)
    x = y = np.linspace(0, 1, resolution + 1)

    # calculate pointrs
    z = np.zeros((resolution + 1)*(resolution + 1))

    x_calcul = np.zeros((resolution + 1)*(resolution + 1))
    y_calcul = np.zeros((resolution + 1)*(resolution + 1))

    s = 0
    for i in x:
        for j in y:
            x_calcul[s], y_calcul[s], z[s] = surf.evaluate_single([i, j])     #surf.evaluate_list([[i, j]]) #   # was evaluate_single [2]
            # If in the center, it's already full matter. Eliminate that!
            if (i - 0.5) ** 2 + (j - 0.5) ** 2 < (3 / 170) ** 2:  # radius
                z[s] = 1   # 1 ?
            s += 1

    Z = z.reshape((resolution + 1), (resolution + 1))

    # Amount of files in dir
    path, dirs, files = next(os.walk(root_path + '/data/DensityFunction'))
    n_files = len(files)

    # Plot the image
    my_dpi = 216.5/4*3 * 1    # 216.5 = 800 pixels. Now is 600 pixels

    plt.imshow(Z, cmap='gray', interpolation='nearest', filterrad=1)#, block=True)

    plt.axis('off')

    plt.savefig("data/DensityFunction/img_" + str(n_files).zfill(4) + ".png", format='png', bbox_inches='tight', pad_inches=0, dpi=my_dpi)#, figsize=(1.5, 1))
    plt.close()


