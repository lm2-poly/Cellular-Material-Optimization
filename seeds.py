# coding=utf-8
from numpy import ceil
import gmsh


def get_lines(faces):
    line_1 = [faces[0], faces[1]]
    line_2 = [faces[1], faces[2]]
    line_3 = [faces[2], faces[3]]
    line_4 = [faces[3], faces[0]]
    return line_1, line_2, line_3, line_4


def seeding(verts, faces_sqr, max_seed_size):
    GRID = dict()
    QUAD4 = list()
    s = 0

    for ss, face in enumerate(faces_sqr):
        p1, p2, p3, p4 = face
        v1 = verts[p1]
        v2 = verts[p2]
        v3 = verts[p3]
        v4 = verts[p4]

        # Assume QUAD
        dz = dist3(v1, v2)
        dxy = dist3(v2, v3)
        nz, nxy = amount_seeds(max_seed_size, dz, dxy)
        GRID_temp, QUAD4_temp = parsing(nz, nxy, v1, v2, v3, v4)

        for pt in GRID_temp:
            if pt not in GRID.values():
                s += 1
                GRID[s] = pt

        for sss, Quads in enumerate(QUAD4_temp):
            new_corners = list()
            for vx in Quads:
                for key, value in GRID.items():
                    if value == GRID_temp[vx]:
                        new_corners.append(key)
            QUAD4.append(new_corners)

    return GRID, QUAD4


def seeding_V3(Vertex_3D_ID, Vertex_3D_val, Segment_3D_ID, Segment_3D_val, Polygon_3D_ID, Polygon_3D_val, max_seed_size, n_polygons, n_segments):

    tm = max_seed_size

    gmsh.initialize()
    gmsh.option.setNumber("General.Terminal", 1)

    gmsh.model.add("modele_test")

    geom = gmsh.model.geo

    for keys in Vertex_3D_ID:
        gmsh.model.geo.addPoint(Vertex_3D_ID[keys][0], Vertex_3D_ID[keys][1], Vertex_3D_ID[keys][2], tm, keys)

    # BC
    """
    central = keys + 1
    left = keys + 2
    right = keys + 3
    gmsh.model.geo.addPoint(0, 0, 0, tm/3, central)  # Punto central del círculo
    gmsh.model.geo.addPoint(-12.7, 0, 0, tm/3, left)
    gmsh.model.geo.addPoint(12.7, 0, 0, tm/3, right)
"""
    for keys in Segment_3D_ID:
        gmsh.model.geo.addLine(Segment_3D_ID[keys][0], Segment_3D_ID[keys][1], keys)
    """
    circle_top = keys + 1
    circle_bottom = keys + 2
    gmsh.model.geo.addCircleArc(left, central, right, circle_top)  # Arco superior
    gmsh.model.geo.addCircleArc(right, central, left, circle_bottom)  # Arco inferior
"""
    for keys in Polygon_3D_ID:
        gmsh.model.geo.addCurveLoop(Polygon_3D_ID[keys], keys)
    """
    gmsh.model.geo.addCurveLoop([circle_top, circle_bottom], keys + 1)
    """

    plane = list()
    for i, keys in enumerate(Polygon_3D_ID):
        gmsh.model.geo.addPlaneSurface([keys], keys)

    # THIS IS FOR THE STRUCTURED GRID TO APPEAR
    for i, keys in enumerate(Segment_3D_ID):
        if keys > 2 * n_segments:
            #gmsh.model.geo.mesh.setTransfiniteCurve(keys, 7)
            gmsh.model.geo.mesh.setTransfiniteCurve(keys, round(30 / max_seed_size) + 2)
    for i, keys in enumerate(Polygon_3D_ID):
        if keys > 2 * n_polygons:
            gmsh.model.geo.mesh.setTransfiniteSurface(keys)
            gmsh.model.geo.mesh.setRecombine(2, keys)

    gmsh.model.geo.synchronize()

    gmsh.option.setNumber('Mesh.SurfaceFaces', 1)  # Ver las "caras" de los elementos finitos 2D
    gmsh.option.setNumber('Mesh.Points', 1)  # Ver los nodos de la malla

    gmsh.option.setNumber('Mesh.MeshSizeMax', max_seed_size)
    gmsh.option.setNumber('Mesh.ElementOrder', 2)
    gmsh.option.setNumber("Mesh.SecondOrderIncomplete", 1)

    # Silence please
    gmsh.option.setNumber("General.Verbosity", 0)

    gmsh.model.mesh.generate(3)

    gmsh.option.setNumber("Mesh.Format", 31)        # was 31

    # Y finalmente guardar la malla
    filename = 'OD.bdf'
    gmsh.write(filename)

    # Podemos visualizar el resultado en la interfaz gráfica de GMSH
    #gmsh.fltk.run()

    # %% Tras finalizar el proceso se recomienda usar este comando
    gmsh.finalize()

    return filename

def dist2(p1, p2):
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5

def dist3(p1, p2):
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)**0.5


def amount_seeds(max_seed_size, dz, dxy):

    nz = int(ceil(dz/max_seed_size) + 1)
    nxy = int(ceil(dxy/max_seed_size) + 1)
    return nz, nxy

def parsing(nz, nxy, p1, p2, p3, p4):
    QUAD4_temp = list()
    GRID_temp = list()
    for i in range(nz):
        ip = i / (nz - 1)   # get percentage for each pt
        for j in range(nxy):
            pt = list()
            jp = j / (nxy - 1)
            x = round(p1[0] * (1 - jp) + p4[0] * jp, 3)
            y = round(p1[1] * (1 - jp) + p4[1] * jp, 3)
            z = round(p1[2] * (1 - ip) + p2[2] * ip, 3)
            GRID_temp.append([x, y, z])

    for i in range(nz-1):
        for j in range(nxy - 1):
            QUAD4_temp.append([i*(nxy - 1) + j + 1, i*(nxy - 1) + j + 2, i*nxy + j + 1, i*nxy + j + 2])


    return GRID_temp, QUAD4_temp


