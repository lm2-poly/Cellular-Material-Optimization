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
    root_path = "C:/Users/olduca/PycharmProjects/2DCellularOptimization"


    # Control points
    # Variable to optimize would be the height of the 36 control points representing the density function.
    #n = len(x0)
    half_panel = 85
    resolution = 600  # was 80
    #ctrlpts = []
    #if (n % 2) == 0:
    #    for subd in n:
    #        ctrlpts.append[[-half_panel, -half_panel, x0[0]]]

    n_vars = 2
    num_arr = 2       # must be how much ? Amount of arrays: 21=6, 15=5, 10=4, 6=3, 3=2, etc.
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

    inc = 85/(num_arr-1)     # -1 since it's odd
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





    #ctrlpts = [
    #    [[-85.0, -85.0, x0[0]], [-85.0, -51.0, x0[1]], [-85.0, -17.0, x0[2]], [-85.0, 17.0, x0[2]], [-85.0, 51.0, x0[1]], [-85.0, 85.0, x0[0]]],
    #    [[-51.0, -85.0, x0[1]], [-51.0, -51.0, x0[3]], [-51.0, -17.0, x0[4]], [-51.0, 17.0, x0[4]], [-51.0, 51.0, x0[3]], [-51.0, 85.0, x0[1]]],
    #    [[-17.0, -85.0, x0[2]], [-17.0, -51.0, x0[4]], [-17.0, -17.0, x0[5]], [-17.0, 17.0, x0[5]], [-17.0, 51.0, x0[4]], [-17.0, 85.0, x0[2]]],
    #    [[17.0, -85.0, x0[2]], [17.0, -51.0, x0[4]], [17.0, -17.0, x0[5]], [17.0, 17.0, x0[5]], [17.0, 51.0, x0[4]], [17.0, 85.0, x0[2]]],
    #    [[51.0, -85.0, x0[1]], [51.0, -51.0, x0[3]], [51.0, -17.0, x0[4]], [51.0, 17.0, x0[4]], [51.0, 51.0, x0[3]], [51.0, 85.0, x0[1]]],
    #    [[85.0, -85.0, x0[0]], [85.0, -51.0, x0[1]], [85.0, -17.0, x0[2]], [85.0, 17.0, x0[2]], [85.0, 51.0, x0[1]], [85.0, 85.0, x0[0]]]
    #]

    # Create a BSpline surface
    surf = BSpline.Surface()

    # Set degrees
    surf.degree_u = 3
    surf.degree_v = 3

    # Set control points
    surf.ctrlpts2d = ctrlpts

    # Set knot vectors
    #surf.knotvector_u = [0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0]
    #surf.knotvector_v = [0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0]
    surf.knotvector_u = utilities.generate_knot_vector(surf.degree_u, surf.ctrlpts_size_u)
    surf.knotvector_v = utilities.generate_knot_vector(surf.degree_v, surf.ctrlpts_size_v)

    # Set evaluation delta
    surf.delta = 0.025

    # Evaluate surface points
    #surf.evaluate()

    # Import and use Matplotlib's colormaps
    from matplotlib import cm

    # Plot the control points grid and the evaluated surface
    #surf.vis = VisMPL.VisSurface()
    #surf.render(colormap=cm.cool)

    #surf.render(colormap=cm.gray)

    # Define a function for cm (colormap)
    x = y = np.linspace(0, 1, resolution + 1)

    # calculate pointrs
    z = np.zeros((resolution + 1)*(resolution + 1))

    x_calcul = np.zeros((resolution + 1)*(resolution + 1))
    y_calcul = np.zeros((resolution + 1)*(resolution + 1))

    s = 0
    for i in x:
        for j in y:
            #coords.append([i, j])
            # White center

            x_calcul[s], y_calcul[s], z[s] = surf.evaluate_single([i, j])     #surf.evaluate_list([[i, j]]) #   # was evaluate_single [2]
            # If in the center, it's already full matter. Eliminate that!
            if (i - 0.5) ** 2 + (j - 0.5) ** 2 < (3 / 170) ** 2:  # radius
                z[s] = 1   # 1 ?
            s += 1

    Z = z.reshape((resolution + 1), (resolution + 1))
    #X = x_calcul.reshape((resolution + 1), (resolution + 1))
    #Y = y_calcul.reshape((resolution + 1), (resolution + 1))


    # Amount of files in dir
    path, dirs, files = next(os.walk(root_path + '/data_OD/DensityFunction'))
    n_files = len(files)


    # Plot the image
    my_dpi = 216.5/4*3 * 1    # 216.5 = 800 pixels. Now is 600 pixels
    #fig_size = int(800/my_dpi)
    #fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(fig_size, fig_size), dpi=my_dpi)
    #plt.figure(figsize=(fig_size, fig_size), dpi=my_dpi)

    #plt.figure(figsize=(fig_size, fig_size), dpi=my_dpi)

    plt.imshow(Z, cmap='gray', interpolation='nearest', filterrad=1)#, block=True)


    #plt.pcolor(X, Y, Z, cmap='gray')
    #plt.pcolormesh(Z, cmap='gray', vmin=0, vmax=255)#, figsize=(1, 1))

    #plt.figure.set_dpi
    #plt.tight_layout()
    plt.axis('off')

    #plt.set_dpi(100)
    #plt.subplots_adjust(left=0.0, right=1.0, bottom=0.0, top=1.0)
    #plt.show()

    # save the figure   #savefig works
    plt.savefig("data_OD/DensityFunction/img_" + str(n_files).zfill(4) + ".png", format='png', bbox_inches='tight', pad_inches=0, dpi=my_dpi)#, figsize=(1.5, 1))
    plt.close()
    # Debugging



#DensityFunction()

