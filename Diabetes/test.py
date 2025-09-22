import pandas as pd

# Read data
df = pd.read_csv("/Users/dorukakalin/Desktop/Python Internship/Diabetes/diabetes copy.csv")

#Number of Patients
df = df.drop(df[df['Outcome'] == 0].index)
df.to_csv("/Users/dorukakalin/Desktop/Python Internship/Diabetes/diabetes copy.csv")