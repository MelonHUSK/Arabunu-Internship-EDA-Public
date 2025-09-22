from numpy import random as rd

x = rd.rand(3, 5)
print(x)

y = rd.choice([3,5,7,9], size=(3,5))
print(y)