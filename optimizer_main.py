import PyNomad
import sys
from main_OS1 import to_optimize

# Initial point x0, lower bound (lb) and upper bound(ub)




def bb_pynomad(x):
    """
    "Black-box" function formatted to software PyNomad
    :param x: a vector of 3 component, x=(x1,x2,x3) where x1,x2 are continuous and x3 is an integer.
    :param bb: function to optimize
     NOTE :  x.get_coord(i) retrives the i-th component of the vector x
    :return: for an evaluation, 0 if PyNomad failed, 1 if PyNomad succeed
    """
    try:
        #f = to_optimize(x0=[float(x.get_coord(0))])

        ### 3 vars:
        #f = to_optimize(x0=[float(x.get_coord(0)), float(x.get_coord(1)), float(x.get_coord(2))])

        ### 6 vars:
        #f = to_optimize(x0=[float(x.get_coord(0)), float(x.get_coord(1)), float(x.get_coord(2)), float(x.get_coord(3)), float(x.get_coord(4)), float(x.get_coord(5))])
        ### 15 vars:
        #f = to_optimize(x0=[float(x.get_coord(0)), float(x.get_coord(1)), float(x.get_coord(2))
        #                    , float(x.get_coord(3)), float(x.get_coord(4)), float(x.get_coord(5))
        #                    , float(x.get_coord(6)), float(x.get_coord(7)), float(x.get_coord(8))
        #                    , float(x.get_coord(9)), float(x.get_coord(10)), float(x.get_coord(11))
        #                    , float(x.get_coord(12)), float(x.get_coord(13)), float(x.get_coord(14))])
        ### 10 vars:
        #f = to_optimize(x0=[float(x.get_coord(0)), float(x.get_coord(1)), float(x.get_coord(2))
        #                    , float(x.get_coord(3)), float(x.get_coord(4)), float(x.get_coord(5))
        #                    , float(x.get_coord(6)), float(x.get_coord(7)), float(x.get_coord(8))
        #                    , float(x.get_coord(9))])
        #f = to_optimize(x0=[float(x.get_coord(0)), float(x.get_coord(1)), float(x.get_coord(2))])
        #f = to_optimize(x0=[float(x.get_coord(0)), float(x.get_coord(1)), float(x.get_coord(2))
        #                    , float(x.get_coord(3)), float(x.get_coord(4)), float(x.get_coord(5))
        #                    , float(x.get_coord(6)), float(x.get_coord(7)), float(x.get_coord(8))
        #                    , float(x.get_coord(9)), float(x.get_coord(10)), float(x.get_coord(11))
        #                    , float(x.get_coord(12)), float(x.get_coord(13)), float(x.get_coord(14))
        #                    , float(x.get_coord(15)), float(x.get_coord(16)), float(x.get_coord(17))
        #                    , float(x.get_coord(18)), float(x.get_coord(19)), float(x.get_coord(20))])    #, x.get_coord(1), x.get_coord(2), x.get_coord(3), x.get_coord(4), x.get_coord(5)])
        # 36
        f = to_optimize(x0=[float(x.get_coord(0)), float(x.get_coord(1)), float(x.get_coord(2))
            , float(x.get_coord(3)), float(x.get_coord(4)), float(x.get_coord(5))
            , float(x.get_coord(6)), float(x.get_coord(7)), float(x.get_coord(8))
            , float(x.get_coord(9)), float(x.get_coord(10)), float(x.get_coord(11))
            , float(x.get_coord(12)), float(x.get_coord(13)), float(x.get_coord(14))
            , float(x.get_coord(15)), float(x.get_coord(16)), float(x.get_coord(17))
            , float(x.get_coord(18)), float(x.get_coord(19)), float(x.get_coord(20))
            , float(x.get_coord(21)), float(x.get_coord(22)), float(x.get_coord(23))
            , float(x.get_coord(24)), float(x.get_coord(25)), float(x.get_coord(26))
            , float(x.get_coord(27)), float(x.get_coord(28)), float(x.get_coord(29))
            , float(x.get_coord(30)), float(x.get_coord(31)), float(x.get_coord(32))
            , float(x.get_coord(33)), float(x.get_coord(34)), float(x.get_coord(35))])

        # 28
        #f = to_optimize(x0=[float(x.get_coord(0)), float(x.get_coord(1)), float(x.get_coord(2))
        #    , float(x.get_coord(3)), float(x.get_coord(4)), float(x.get_coord(5))
        #    , float(x.get_coord(6)), float(x.get_coord(7)), float(x.get_coord(8))
        #    , float(x.get_coord(9)), float(x.get_coord(10)), float(x.get_coord(11))
        #    , float(x.get_coord(12)), float(x.get_coord(13)), float(x.get_coord(14))
        #    , float(x.get_coord(15)), float(x.get_coord(16)), float(x.get_coord(17))
        #    , float(x.get_coord(18)), float(x.get_coord(19)), float(x.get_coord(20))
        #    , float(x.get_coord(21)), float(x.get_coord(22)), float(x.get_coord(23))
        #    , float(x.get_coord(24)), float(x.get_coord(25))
        #    , float(x.get_coord(26)), float(x.get_coord(27))])  # , x.get_coord(1), x.get_coord(2), x.get_coord(3), x.get_coord(4), x.get_coord(5)])

        x.setBBO(str(f).encode("UTF-8"))
    except:
        print("Unexpected eval error", sys.exc_info()[0])
        return 0
    return 1  # 1: success 0: failed evaluation

#x0 = [0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995]
#x0 = [0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995]
#lb = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#ub = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

#x0 = [0]
#lb = [0]
#ub = [3]

#x0 = [127.5, 127.5, 127.5, 127.5, 127.5, 127.5]
#lb = [0, 0, 0, 0, 0, 0]
#ub = [255, 255, 255, 255, 255, 255]

# Formatting the parameters for PyNomad
#input_type = "BB_INPUT_TYPE (R R R R R R R R R R R R R R R)"

### 21 vars:

# input_type = "BB_INPUT_TYPE (R R R R R R R R R R R R R R R R R R R R R)"  # R=real (float) and I=integer
# x0 = [0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995]
# lb = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# ub = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# dimension = "DIMENSION 21"

# 15 vars:
#input_type = "BB_INPUT_TYPE (R R R R R R R R R R R R R R R)"
#x0 = [0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995]
#lb = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#ub = [0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995]
#dimension = "DIMENSION 15"

# 10 vars:
#input_type = "BB_INPUT_TYPE (R R R R R R R R R R)"
#x0 = [0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995]
#lb = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#ub = [0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995]
#dimension = "DIMENSION 10"

# 21 vars:
#input_type = "BB_INPUT_TYPE (R R R R R R R R R R R R R R R R R R R R R)"
#x0 = [0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995]
#lb = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#ub = [0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995]
#dimension = "DIMENSION 21"

# 28 vars:
#input_type = "BB_INPUT_TYPE (R R R R R R R R R R R R R R R R R R R R R R R R R R R R)"
#x0 = [0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995]
#lb = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#ub = [0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995]
#dimension = "DIMENSION 28"

# 36 vars:
input_type = "BB_INPUT_TYPE (R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R)"
x0 = [0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995]
lb = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
ub = [0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995, 0.995]
dimension = "DIMENSION 36"

### 6 vars:
#input_type = "BB_INPUT_TYPE (R R R R R R)"
#x0 = [0.995, 0.995, 0.995, 0.995, 0.995, 0.995]
#lb = [0, 0, 0, 0, 0, 0]
#ub = [0.995, 0.995, 0.995, 0.995, 0.995, 0.995]
#dimension = "DIMENSION 6"

### 3 vars:
#input_type = "BB_INPUT_TYPE (R R R)"
#x0 = [0.995, 0.995, 0.995]
#lb = [0, 0, 0]
#ub = [1, 1, 1]
#dimension = "DIMENSION 3"

#dimension = "DIMENSION 1"


max_nb_of_evaluations = "MAX_BB_EVAL 1000"


params = [max_nb_of_evaluations, dimension, input_type,
          "DISPLAY_DEGREE 2", "BB_OUTPUT_TYPE OBJ", "DISPLAY_ALL_EVAL TRUE", "DISPLAY_STATS BBE OBJ (SOL)",
          "NB_THREADS_OPENMP 1", "QUAD_MODEL_SEARCH TRUE", "EVAL_OPPORTUNISTIC FALSE", "INITIAL_MESH_SIZE * 0.25",
          "MIN_MESH_SIZE * 0.01", "SEED 0", "CS_OPTIMIZATION TRUE"]


# Important : PyNomad strictly minimizes the bb function
PyNomad.optimize(bb_pynomad, x0, lb, ub, params)

