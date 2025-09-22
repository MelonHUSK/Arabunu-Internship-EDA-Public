#List is a collection which is ordered and changeable. Allows duplicate members.
#Tuple is a collection which is ordered and unchangeable. Allows duplicate members.
#Set is a collection which is unordered, unchangeable*, and unindexed. No duplicate members.
#Dictionary is a collection which is ordered** and changeable. No duplicate members.

myList = ["BMTH", "Pierce The Veil", "Dethtech", "Neet", "Deep Purple", "Green Day"]
newList = [x.split(" ") for x in myList if "e" in x]
print(newList)