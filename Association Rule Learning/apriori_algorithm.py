import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

#Data Reading and Cleaning
df = pd.read_csv("/Users/dorukakalin/Desktop/Python Internship/Association Rule Learning/GroceryStoreDataSet.csv", names = ['products'], sep = ',')
data = list(df["products"].apply(lambda x:x.split(",")))

#TSE
a = TransactionEncoder()
a_data = a.fit(data).transform(data)
df_ap = pd.DataFrame(a_data,columns=a.columns_)
df_ap = df_ap.replace(False,0)
df_ap = df_ap.replace(True, 1)
print(df_ap)

#Apriori Data Structure
df = apriori(df_ap, min_support = 0.2, use_colnames = True, verbose = 1)
print(df)

#Rules for the dataset
df_ar = association_rules(df, metric = "confidence", min_threshold = 0.6)
print(df_ar)

#Reccomendation Algorithm
rules_sorted = df_ar.sort_values("lift", ascending=False)

def recommended_products(product_id, rec_count=5):
    recommended_products = []

    for i, product in rules_sorted["antecedents"].items():
        if product_id in product:
            recommended_products.extend(list(rules_sorted.iloc[i]["consequents"]))

    recommended_products = list(set(recommended_products)) 
    return recommended_products[:rec_count]

print(recommended_products(input()))