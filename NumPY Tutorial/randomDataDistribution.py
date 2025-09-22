from numpy import random

x = random.choice([3, 5, 7, 9], p=[0.1, 0.3, 0.59, 0.01], size=(100, 3))

print(x)