import pandas as pd

#Init Dataframe
df = pd.read_csv("/Users/dorukakalin/Desktop/Python Internship/CLTV/Year 2010-2011.csv", encoding="unicode_escape")
df = pd.DataFrame(df)

#Cleaning Data
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)

#Data Prep
df["Date"] = pd.to_datetime(df["Date"])
df = df.groupby("Customer ID").agg({"Price" : ["sum", "mean",], "Date" : ["min", "max", "count"]})

df.columns = ['total_spent', 'average_spent', 'first_purchase', 'last_purchase', 'purchase_count']

df['customer_lifetime'] = (df['last_purchase'] - df['first_purchase']).dt.days
df['customer_lifetime'] = df['customer_lifetime'].replace(0, 1)
df['purchase_frequency'] = df['purchase_count'] / df['customer_lifetime']
df['avg_order_value'] = df['total_spent'] / df['purchase_count']

df["cltv"] = df['avg_order_value'] * df['purchase_frequency'] * df['customer_lifetime']
df.sort_values(by=["cltv"], ascending=False, inplace=True)
df.to_csv("/Users/dorukakalin/Desktop/Python Internship/CLTV/CleanedData.csv")