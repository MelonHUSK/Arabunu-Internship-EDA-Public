import numpy as np

def myAdd(x, y):
    return x+y

myadd = np.frompyfunc(myAdd, 2, 1)

print(myAdd([1, 2, 3, 4], [5, 6, 7, 8]))