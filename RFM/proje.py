############################################    
# PROJE: RFM ile Müşteri Segmentasyonu
############################################
# Bir e-ticaret şirketi müşterilerini segmentlere ayırıp bu segmentlere göre pazarlama stratejileri belirlemek istiyor.
# online_retail_II.xlsx veri setinin "Year 2010-2011" isimli sheet'ine RFM analizi uygulayınız.

#############################################
# GÖREV 1: Derste ele alınan uygulamaların benzerlerini yapınız.
############################################

############################################
# GÖREV 2: Müşterileri segmentlere ayırdıktan sonra 3 segment seçerek bu 3 segmenti hem aksiyon
# kararları açısından hem de segmentlerin yapısı açısından (ortalama RFM değerleri açısından)
# yorumlayınız.
############################################

############################################
# GÖREV 3: "Loyal Customers" sınıfına ait customer ID'leri seçerek excel çıktısını alınız.
############################################



#############################################
# GÖREV 1
############################################
import pandas as pd
import datetime as dt

df = pd.read_csv("/Users/dorukakalin/Desktop/Python Internship/CLTV/Year 2010-2011.csv")
df = pd.DataFrame(df)

#Data Prep
df["TotalPrice"] = df["Price"] * df["Quantity"]
df["Date"] = pd.to_datetime(df["Date"])
today_date = dt.datetime(2010, 12, 11)

#Calculate RFM
df = df.groupby('Customer ID').agg({'Date': lambda date: (today_date - date.max()).days, #Recency: Days since last purchase
                                     'Invoice': lambda num: len(num), #Frequency: Number of pruchases
                                     'TotalPrice': lambda TotalPrice: TotalPrice.sum()}) #Monetary: Total money spent per customer
df.columns = ["Recency", "Frequency", "Monetary"]

#Segmenting
df["RecencyScore"] = pd.qcut(df['Recency'], 5, labels=[5, 4, 3, 2, 1]) 
df["FrequencyScore"] = pd.qcut(df['Frequency'], 5, labels=[5, 4, 3, 2, 1])
df["MonetaryScore"] = pd.qcut(df['Monetary'], 5, labels=[5, 4, 3, 2, 1])

df["RFM_SCORE"] = (df['RecencyScore'].astype(str) +
                    df['FrequencyScore'].astype(str) +
                    df['MonetaryScore'].astype(str)) 

rfm_seg_map = {
    r'[1-2][1-2]': 'Hibernating',
    r'[1-2][3-4]': 'At_Risk',
    r'[1-2]5': 'Cant_Lose',
    r'3[1-2]': 'About_to_Sleep',
    r'33': 'Need_Attention',
    r'[3-4][4-5]': 'Loyal_Customers',
    r'41': 'Promising',
    r'51': 'New_Customers',
    r'[4-5][2-3]': 'Potential_Loyalists',
    r'5[4-5]': 'Champions'
}

df['Segment'] = df['RecencyScore'].astype(str) + df['FrequencyScore'].astype(str)
df['Segment'] = df['Segment'].replace(rfm_seg_map, regex=True)
df.drop(columns=["Recency","Frequency","Monetary","RecencyScore","FrequencyScore","MonetaryScore"], inplace=True)
df.to_csv("/Users/dorukakalin/Desktop/Python Internship/RFM/customers.csv")

#############################################
# Görev 2
#############################################

#Data Prep 2
df.reset_index(inplace=True)
df.drop(columns=["Customer ID"], inplace=True)
df.reset_index(inplace=True)
df['RFM_SCORE'] = pd.to_numeric(df['RFM_SCORE'], errors='coerce')
df["RFM_SCORE"].astype(int)

#Main Func
_df = pd.DataFrame()
_df= df.groupby('Segment')['RFM_SCORE'].mean().reset_index()
_df.columns = ["Segment", "RFM_Avg"]
_df.sort_values(by=["RFM_Avg"], ascending=False, inplace=True)
_df.to_csv("/Users/dorukakalin/Desktop/Python Internship/RFM/RFM_analysis.csv")

############################################
# GÖREV 3
############################################

df = pd.read_csv("/Users/dorukakalin/Desktop/Python Internship/RFM/customers.csv")
df.drop(df[df['Segment'] != 'Loyal_Customers'].index, inplace=True)
df.reset_index(inplace=True)
df.drop(columns=["RFM_SCORE", "Segment", "index"], inplace=True)
df.to_csv("/Users/dorukakalin/Desktop/Python Internship/RFM/Loyal_Customers.csv")