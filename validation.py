# coding=utf-8
import os

import os
import copy
import numpy as np
import pyNastran
from pyNastran.bdf.bdf import BDF, read_bdf
#from pyNastran.bdf.case_control_deck import CaseControlDeck
from pyNastran.op2.op2 import read_op2, OP2
from pyNastran.utils import object_attributes, object_methods, print_bad_path
from pyNastran.utils.nastran_utils import run_nastran
from pyNastran.bdf.mesh_utils.mass_properties import mass_properties

path_main = "C:/Users/olduca/PycharmProjects/2DCellularOptimization/data_OD - 5G0 - Sensitivity/"
path_op2 = path_main + "OP2/"

file_results_validation = open(path_main + "result_validation_Center.txt", "w")

for n, file in enumerate(os.listdir(path_op2)):
    if file.endswith(".op2"):
        results = read_op2(file, load_geometry=True, debug=False)

        #elts_bottom = list()

        f = 0
        for pts in results.nodes:
            x = results.nodes[pts].xyz[0]
            y = results.nodes[pts].xyz[1]
            z = results.nodes[pts].xyz[2]
            if z == 0.0:                              #round(x**2 + y**2, 0) == 3.0**2:   # 0.0 = z pour rigid. 1.0 = z pour flex. Exclusion du centre pour les borders.
                #elts_bottom.append(pts)
                f += results.spc_forces[1].data.__array__()[0].__array__()[pts-1][2] / 1000000

        file_results_validation.write(str(n))
        file_results_validation.write("\t")
        file_results_validation.write(str(f))
        file_results_validation.write("\n")