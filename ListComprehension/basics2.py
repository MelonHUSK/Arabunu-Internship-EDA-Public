list = ["Black", "Blue", "Green", "Yellow", "White", "Red", "Indigo"]
listUpdated = [x if x == "Yellow" else "Omitted" for x in list]
print(listUpdated)