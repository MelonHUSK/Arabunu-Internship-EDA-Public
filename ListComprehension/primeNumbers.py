import pandas as pd
import matplotlib.pyplot as plt

def checkIfPrime(n):
    if n < 2:
        return "Not Prime"
    i = 2
    while i*i <= n:
        if n % i == 0:
            return "Not Prime"
        i += 1
    return "Is Prime"
    
numbers = [i for i in range(2001)]
primeChecker = [checkIfPrime(i) for i in range(20001)]
combined = [(i, j) for i, j in zip(numbers, primeChecker)]
df = pd.DataFrame(combined)
df = df.dropna()
print(df.to_string())
df.to_csv("/Users/dorukakalin/Desktop/Python Internship/Pandas Tutorial/data.csv")
df.plot()
plt.show()