numbersList = [i for i in range(20)]
numbersComposition = ["Zero" if i == 0 else "Even Number" if i % 2 == 0 else "Odd number" for i in numbersList]
print(numbersList)
print(numbersComposition)