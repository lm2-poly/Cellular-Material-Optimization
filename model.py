# coding=utf-8
import os
import pyNastran
from pyNastran.bdf.bdf import BDF
from pyNastran.op2.op2 import read_op2
from voronoi import *

# Abaqus - write inp file for FEA
def write_inp(verts, faces_sqr):

    i = 0
    ii = 0
    f = open("inp_file.inp", "w")
    f.write("*Node, NSET=NSET_ALL\n")
    for vertex in verts:
        i += 1
        f.write(str(i) + ", " + str(vertex[0]) + ", " + str(vertex[1]) + ", " + str(vertex[2]) + "\n")

    f.write("*Element, TYPE=S4, ELSET=ELSET_ALL\n")
    for face in faces_sqr:
        ii += 1
        f.write(str(ii) + ", " + str(face[0]+1) + ", " + str(face[1]+1) + ", " + str(face[2]+1) + ", " + str(face[3]+1) + "\n")
    f.close()

# Inspect a BDF. Was used as test
def read_bdf():

    pkg_path = pyNastran.__path__[0]
    test_path = os.path.join(pkg_path, '..', 'models', 'solid_bending')
    bdf_filename = os.path.join(test_path, 'solid_bending.bdf')

    model = pyNastran.bdf.bdf.BDF(debug=False)
    model.read_bdf(bdf_filename, xref=True)
    f = open('junk.out', 'w')

# add one to all values of a list - Python starts at 0, Nastran at 1
def plus_one(input):
    output = list()
    for i in input:
        temp = list()
        for j in i:
            j += 1
            temp.append(j)
        output.append(temp)
    return output


# Function to write faces and verts for Blender import (STL, non-manifold. Blender allows manifold)
def write_faces_and_verts(verts, faces, faces_sqr, file_str):
    with open("./data/STL/stl_" + file_str + ".odstl", 'w', encoding='utf-8') as infile:
        infile.write("verts = " + str(verts) + "\n")
        infile.write("faces = " + str(faces) + "\n")


def write_bdf_V2(filename, n_polygons, n_segments, filename_BDF):
    # This function removes cbar artefacts
    filename2 = delete_cbar(filename)

    # This function differentiate skins from core
    filename3 = correct_properties(filename2)

    model_temp = pyNastran.bdf.bdf.BDF(debug=False)
    model_temp.read_bdf(filename3, xref=False, punch=True)

    # iterate through every GRID (node) and scale its coordinates
    for nid, node in model_temp.nodes.items():
        # .xyz returns the x, y, z coordinates of the node
        scaled_xyz = node.xyz / 1000.0

        # Update the node coordinates
        node.xyz = scaled_xyz

    # modified model
    filename4 = filename3 + "4"
    model_temp.write_bdf(filename4)

    model = pyNastran.bdf.bdf.BDF(debug=False)
    model.read_bdf(filename4, xref=False, punch=True)

    # For contact BC, we have already defined the bdf of a plate
    filename_load = os.getcwd() + "/Plate_Bottom/Plate_Contact2.bdf"

    model2 = pyNastran.bdf.bdf.BDF(debug=False)
    model2.read_bdf(filename_load)

    node_load_id = dict()
    elt_load_id = dict()
    n_node = model.nnodes
    punch_node = list()
    bottom_node = list()
    n_elt = list(model.elements)[-1]

    for node in model2.nodes:
        bottom_node.append(node + n_node)
        node_load_id[node] = model2.nodes[node].xyz
        temp = model2.nodes[node].xyz
        # Ici, on vient ajouter tous les noeuds du punch à notre BDF existant. On le décale en Z pour éviter une collision
        model.add_grid(node + n_node, [temp[0], temp[1], temp[2] - 0.0])

    for elt in model2.elements:
        elt_load_id[node] = model2.elements[elt].nodes
        temp = model2.elements[elt].nodes
        model.add_cquad4(elt + n_elt, 3, [temp[0] + n_node, temp[1] + n_node, temp[2] + n_node, temp[3] + n_node])  # + n nodes....

    model.write_bdf('junk.bdf')

    ss = 0
    elts_to_spc = list()
    elts_surf_top = list()
    elts_to_displacement = list()
    for key in model.nodes:
        xyz = model.nodes[key].xyz
        x = float(xyz[0])
        y = float(xyz[1])
        z = float(xyz[2])

        # Ici, on veut différencier les éléments sur les côtés qui sont fixés (BC)
        #if (abs(x) > 70 or abs(y) > 70) and z == 1:
        if (abs(round(x, 5)) >= 70/1000 or abs(round(y, 5)) >= 70/1000) and round(z, 5) == 1/1000:
            ss += 1
            elts_to_spc.append(key)

        if round(x**2 + y**2, 8) == (3.0/1000)**2:   # was 3.0
            elts_to_displacement.append(key)

    elts_bottom = list()

    # Check nodes of every elements. If at 24, they belong to the top surface.
    for key in model.elements:
        if key > n_elt:
            elts_bottom.append(key)
        nodes_of_elt = model.elements[key].nodes
        pt1 = nodes_of_elt[0]
        pt2 = nodes_of_elt[1]
        pt3 = nodes_of_elt[2]

        # On définit la skin du dessous pour le contact entre surfaces
        if model.nodes[pt1].xyz[2] == 0.001 and model.nodes[pt2].xyz[2] == 0.001 and model.nodes[pt3].xyz[2] == 0.001:
            elts_surf_top.append(key)

    # Magnitude du déplacement forcé par le punch, mm
    mag = float(-0.001) #

    for i, p in enumerate(elts_to_displacement):
        model.add_spcd(200, [p], ["3"], [mag])
    model.add_spc1(5, "123", elts_to_displacement)

    # Définition de la zone de contact du bas
    model.add_bsurf(1, elts_bottom)
    model.add_bcrpara(1, surf="TOP", Type='RIGID', grid_point=elts_bottom[0])   # Grid pts = 0? By default.  511 is center  #maybe  bot

    # Définition de la surface de la peau du bas
    model.add_bsurf(2, elts_surf_top)
    model.add_bcrpara(2, surf="TOP", Type='FLEX')

    # Définition du déplacement forcé sur le punch
    model.add_spc1(11, '123456', bottom_node)
    model.add_spcadd(201, [5, 11])

    # write pshell properties
    mid1 = 1
    pid1 = 1
    t1 = 2.0e-3    # skins
    mid2 = 2
    pid2 = 2
    t2 = 0.48e-3     # core
    mid3 = 3
    pid3 = 3
    t3 = 1.0e-6
    mid4 = 4
    pid4 = 4
    t4 = 2.0    # skin

    model.add_pshell(pid1, mid1=mid1, t=t1, mid2=mid1, mid3=mid1)
    model.add_pshell(pid2, mid1=mid2, t=t2, mid2=mid2, mid3=mid2)
    model.add_pshell(pid3, mid1=mid3, t=t3, mid2=mid3, mid3=mid3)
    model.add_pshell(pid4, mid1=mid4, t=t4, mid2=mid4, mid3=mid4)

    # Material properties
    E1 = 3.08e9
    G1 = None
    nu1 = 0.33
    model.add_mat1(mid1, E1, G1, nu1)
    E2 = 3.08e9
    G2 = None
    nu2 = 0.33
    model.add_mat1(mid2, E2, G2, nu2)
    model.add_mat1(mid4, E2, G2, nu2)
    E3 = 6.9e48
    G3 = None
    nu3 = 0.33
    model.add_mat1(mid3, E3, G3, nu3)
    model.sol = 101
    model.write_bdf('junk2.bdf')

    data = data2 = ""
    # Reading data from file1
    with open('Header.txt') as fp:
        data = fp.read()

    # Reading data from file2
    with open('junk2.bdf') as fp:
        data2 = fp.read()

    # Merging 2 files
    data += data2

    with open('./data/BDF/BDF_file_' + filename_BDF + '.bdf', 'w') as fp:
        fp.write(data)

    #return node_rbe2
    return elts_to_displacement


def delete_cbar(filename):
    filename2 = "OD2.bdf"

    f = open(filename2, 'w')

    with open(filename) as fp:
        Lines = fp.readlines()
        for line in Lines:
            if 'CBAR' not in line:
                f.write(line)
    f.close()
    return filename2

# This function aims to differentiate skins from core, and correct the gmsh units (mm) to NX units (m)
def correct_properties(filename2):
    filename3 = "OD3.bdf"
    f = open(filename3, 'w')

    with open(filename2) as fp:
        Lines = fp.readlines()
        for line in Lines:
            if line[0:6] == "CTRIA6":
                line = line[0:16] + "1        " + line[24:] + "\n"
            if line[0:6] == "CQUAD8":
                line = line[0:16] + "2        " + line[24:] + "\n"
            f.write(line)
    f.close()
    return filename3


def format_nastran_8(field_str):
    field_str = field_str.strip()
    if not field_str:
        return "     0.0"

    # scientific notation check
    if 'E' not in field_str.upper() and 'e' not in field_str.upper():
        for i in range(1, len(field_str)):
            if field_str[i] in ['+', '-']:
                field_str = field_str[:i] + 'E' + field_str[i:]
                break

    val = float(field_str) / 1000.0

    if val == 0.0:
        return "     0.0"

    # Standard float formatting
    for decimals in range(7, -1, -1):
        s = f"{val:.{decimals}f}"

        # Drop the leading zero
        if s.startswith("0."):
            s = s[1:]
        elif s.startswith("-0."):
            s = "-" + s[2:]

        # Clean up trailing zeros
        if "." in s:
            s = s.rstrip("0")

        # Float requires a dot
        if "." not in s:
            s += "."

        # 8 chars
        if len(s) > 8:
            s = s[0:8]

        return f"{s:>8}"

    # If it is too massive or too tiny, scientific notation
    for decimals in range(4, -1, -1):
        s = f"{val:.{decimals}E}"
        if len(s) <= 8:
            return f"{s:>8}"

    return "********"  # Standard Nastran overflow string

def scale_field(field_str):
    # Nastran sometimes leaves zero fields completely blank, so we handle that
    if not field_str.strip():
        return f"{0.0:>8.4f}"

    # Convert to float, divide, and format
    scaled_val = float(field_str) / 1000.0

    # Adjust .4f for a different precision to fit the 8 characters
    return f"{scaled_val:>8.4f}"

def write_batch(n):
    f = open(os.getcwd() + "\\data\\OP2\\batch_run.bat", 'w')
    f.write("\"C:\\Program Files\\Siemens\\Simcenter3D_2020.2\\NXNASTRAN\\bin\\nastranw.exe\" \"" + os.getcwd() + "\\data\\BDF\\BDF_file_" + n + ".bdf\" scr=yes old=no delete=f04,log,xdb")
    f.close()


def op2_reading(n, skin_bottom):
    results = read_op2("data/OP2/bdf_file_" + n + ".op2", load_geometry=True, debug=False)
    f = 0
    subcase_id = 1
    target_nodes = skin_bottom
    spc = results.spc_forces[subcase_id]
    op2_nodes = spc.node_gridtype[:, 0]
    mask = np.isin(op2_nodes, target_nodes)

    # [:, 2] refers to the Z-axis (0=Fx, 1=Fy, 2=Fz, 3=Mx, 4=My, 5=Mz)
    z_forces = spc.data[0, mask, 2]
    f = np.sum(z_forces)

    return f
