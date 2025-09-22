arr = [1, 14, 5, 20, 4, 2, 54, 20, 87, 98, 3, 1, 32]  
lowVal = 14 
highVal = 20
solution = [1, 5, 4, 2, 3, 1, 14, 20, 20, 54, 87, 98, 32]

newArr = ([i for i in arr if i < lowVal] + [j for j in arr if j >= lowVal and j <= highVal] + [x for x in arr if x > highVal])
print(newArr)
print(newArr == solution)