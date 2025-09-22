arr = [0, 1, 0, 1, 0, 0, 1, 1, 1, 0]
newArr = ([i for i in arr if i == 0] + [j for j in arr if j == 1])
print(newArr)