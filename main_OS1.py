#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: Olivier Duchesne
Date: May 20, 2026
Version: 2.0

This script is designed to perform a 2D cellular optimization.

Purpose:
The main goal of this script is to optimize a cellular structure for a specific
mechanical objective (i.e. maximize stiffness or minimize peak stress)
by iteratively generating a Voronoi tessellation for a sandwich panel,
running a Nastran analysis,
and evaluating the performance.

The key steps involved are:
1.  **Density Function Generation**: Creates a density image based on input variables (`x0`).
        The density function is a direct function of the blackbox optimization variables.
2.  **Stippling**: Converts the density image into a set of optimized points.
3.  **Voronoi Tessellation**: Generates a Voronoi diagram from the points.
4.  **NASTRAN numerical model creation**: Creates a BDF file and runs a Nastran simulation.
5.  **Result Evaluation**: Reads the OP2 output file to extract and evaluate the objective function (`f`).

"""

from RoundG0_36Vars import DensityFunction # Change according to amount of variables
from voronoi2 import *
from seeds import *
from model import *
from config import *
from points import hexagon_centers, read_points_from_file
import os
import sys
import time
import subprocess
from os.path import exists


def to_optimize(x0):

    tic = time.time()
    cmd = sys.executable
    root_path = "C:/Users/olduca/PycharmProjects/2DCellularOptimization"

    dim_x = 170
    dim_y = 170

    # Amount of files in dir
    path, dirs, files = next(os.walk(root_path + '/data/DensityFunction'))
    n_files = len(files)

    path_dots = "./data/Voronois/img_" + str(n_files).zfill(4) + "-stipple.npy"
    path_img = "./data/WVS/img_" + str(n_files).zfill(4) + "-stipple.png"

    perimeter = [[-85, -85], [85, -85], [85, 85], [-85, 85]]
    x, y = zip(*perimeter)


    # 1. **Density Function Generation**
    DensityFunction(x0)

    # 2. **Stippling**
    # Weighted Voronoi Stippling
    os.system(cmd + " " + "./stippler.py ./data/DensityFunction/img_" + str(n_files).zfill(4) + ".png --save \
    --n_point 320 --n_iter 100 --pointsize 25 25 --figsize 6 \
    --threshold 255 --force") # --interactive is off --force


    pts = read_points_from_file(path_dots, path_img, dim_x, dim_y)

    # 3.  **Voronoi Tessellation**
    vor = Voronoi(pts)

    regions, vertices = voronoi_finite_polygons_2d(vor) # Gets the regions and vertices from the points (2D)
    polygons_core = get_polygons(regions, vertices, vor, perimeter) # List of polygons of the voronoi
    polygons, carre = boundary_conditions(polygons_core)
    verts, faces, faces_sqr = get_faces_and_verts(polygons, choice='TestCarreCisaillement') # Get verts and faces out of these polygons

    # To create cores in Blender
    verts_stlOD, faces_stlOD, bad_data = get_faces_and_verts(polygons_core, choice='TestCarreCisaillement')
    Vertex_2D_ID, Vertex_2D_val, Segment_2D_ID, Segment_2D_val, Polygon_2D_ID, Polygon_2D_val = dict_vertex_2D(polygons)
    Segment_not_in_core = find_segment_not_in_core(Vertex_2D_ID, Vertex_2D_val, Segment_2D_ID, Segment_2D_val)

    n_segments = len(Segment_2D_ID)
    n_polygons = len(Polygon_2D_ID)

    Vertex_3D_ID, Vertex_3D_val, Segment_3D_ID, Segment_3D_val, Polygon_3D_ID, Polygon_3D_val = dict_vertex_3D(Vertex_2D_ID, Vertex_2D_val, Segment_2D_ID, Segment_2D_val, Polygon_2D_ID, Polygon_2D_val, Segment_not_in_core)

    file_name = seeding_V3(Vertex_3D_ID, Vertex_3D_val, Segment_3D_ID, Segment_3D_val, Polygon_3D_ID, Polygon_3D_val, seed_size, n_polygons, n_segments)

    # 4. **NASTRAN numerical model creation**
    elts_sigma_f = write_bdf_V2(file_name, n_polygons, n_segments, str(n_files).zfill(4))

    # Print faces and verts in a file = Blender allows non-manifold to manifold
    write_faces_and_verts(verts_stlOD, faces_stlOD, faces_sqr, str(n_files).zfill(4))

    # Launch Nastran
    write_batch(str(n_files).zfill(4))
    time.sleep(1)
    batch_file = "C:\\Users\\olduca\\PycharmProjects\\2DCellularOptimization\\data\\OP2\\batch_run.bat"
    target_dir = "C:\\Users\\olduca\\PycharmProjects\\2DCellularOptimization\\data\\OP2"

    status = subprocess.call(batch_file, cwd=target_dir)

    # Fct to wait until op2 is completed
    Ready_to_continue = False
    while not Ready_to_continue:
        time.sleep(5)
        if exists(target_dir + "\\" +"bdf_file_" + str(n_files).zfill(4) + ".op2") and not exists(target_dir + "\\" + "bdf_file_" + str(n_files).zfill(4) + ".pch"):
            Ready_to_continue = True

    # 5.  **Result Evaluation**
    f = op2_reading(str(n_files).zfill(4), elts_sigma_f)

    ## Quick infos for modelling

    nozzle = 0.48 # diameter
    perimeter_len = get_overall_perimeter(verts, faces)
    area = area_of_polygon(perimeter)
    print("Perimeter length : " + str(perimeter_len))
    density = nozzle*(perimeter_len-4*170)/area
    volume = nozzle*perimeter_len*21+170*170*4

    #print("Density : " + str(density))
    #print("Volume : " + str(volume))

    plot_verts(verts, faces, x, y, n_files)
    write_params(str(f), perimeter_len, n_files)

    #x.setBBO(str(f).encode("UTF-8"))

    toc = time.time()

    print("Calculation time : " + str(round(toc-tic)))
    print("f is : " + str(f))
    return (f)


# To Test without the whole optimizer, uncomment the 4 following lines.
x0 = [0.945, 0, 0.995, 0.995, 0.995, 0.995, 0.995, 0.04, 0.995, 0.9325, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995,
0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995,
0.995, 0.995, 0.995]
f = to_optimize(x0)
