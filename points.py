# coding=utf-8
import numpy as np
import PIL
import math


def read_points_from_file(path_dots, path_img, dim_x, dim_y):
    filtered_pts = np.load(path_dots)
    image = PIL.Image.open(path_img)
    width, height = image.size          # for scaling
    pts = list()
    for point in filtered_pts:
        x_r = (point[0] * (dim_x) / width) - (dim_x)/2   # 85 for la carre cisaillement instead of 250 or 350
        y_r = (point[1] * (dim_y) / height) - (dim_y)/2    # Ici on recentre et recardre
        point_r = [x_r, y_r]
        pts.append(point_r)
    return pts

def hex_centers(width, height, size):
    """Returns a list of the centers of all hexagonal cells in a rectangular grid.
    width, height: Width and height of the grid in number of cells.
    size: Length of the hexagon's sides.
    """
    centers = []
    for y in range(height):
        offset = size if y % 2 == 0 else size / 2
        for x in range(width):
            center_x = x * size * math.sqrt(3) + offset
            center_y = y * 1.5 * size
            centers.append((center_x, center_y))
    return centers

def hexagon_centers(grid_size, hex_size):
    centers = []
    offset_x = 171.9 + 0.9214 + 4.367
    offset_y = 183 + 4.3035 + 4.09
    for i in range(grid_size):
        for j in range(grid_size):
            x = i * hex_size * math.sqrt(3) + (j % 2) * hex_size * math.sqrt(3) / 2 - offset_x
            y = j * hex_size * 3 / 2 - offset_y
            centers.append((x, y))
    return centers
