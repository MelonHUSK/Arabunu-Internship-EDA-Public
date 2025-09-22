import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns 

df = pd.read_csv("/Users/dorukakalin/Desktop/Python Internship/Spotify (Keyfi)/dataset.csv")
df.sort_values(by="popularity", ascending=False, inplace=True)
df.drop_duplicates(subset="track_name", keep="first", inplace=True)
df.reset_index(inplace=True)
df = df.groupby("artists").agg({"popularity" : "sum"})
df.sort_values(by=["popularity"], ascending=False, inplace=True)
print(df.head())
df.to_csv("/Users/dorukakalin/Desktop/Python Internship/Spotify (Keyfi)/deeperAnalysis/normie artists.csv")

