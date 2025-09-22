###############################################################
# Customer Segmentation with RFM
###############################################################

# Customer Segmentation with RFM in 6 Steps

# 1. Business Problem
# 2. Data Understanding
# 3. Data Preparation
# 4. Calculating RFM Metrics
# 5. Calculating RFM Scores
# 6. Naming & Analysing RFM Segments


# Bir e-ticaret şirketi müşterilerini segmentlere ayırıp bu segmentlere göre
# pazarlama stratejileri belirlemek istiyor.

# Buna yönelik olarak müşterilerin davranışlarını tanımlayacağız ve
# bu davranışlarda öbeklenmelere göre gruplar oluşturacağız.

# Veri Seti Hikayesi
#
# https://archive.ics.uci.edu/ml/datasets/Online+Retail+II
#
# Online Retail II isimli veri seti İngiltere merkezli online bir satış mağazasının
# 01/12/2009 - 09/12/2011 tarihleri arasındaki satışlarını içeriyor.

# Değişkenler
# InvoiceNo: Fatura numarası. Her işleme yani faturaya ait eşsiz numara.
# Eğer bu kod C ile başlıyorsa işlemin iptal edildiğini ifade eder.
# StockCode: Ürün kodu. Her bir ürün için eşsiz numara.
# Description: Ürün ismi
# Quantity: Ürün adedi. Faturalardaki ürünlerden kaçar tane satıldığını ifade etmektedir.
# InvoiceDate: Fatura tarihi ve zamanı.
# UnitPrice: Ürün fiyatı (Sterlin cinsinden)
# CustomerID: Eşsiz müşteri numarası
# Country: Ülke ismi. Müşterinin yaşadığı ülke.


###############################################################
# Data Understanding
###############################################################

import datetime as dt
import pandas as pd
pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
# pd.set_option('display.float_format', lambda x: '%.5f' % x)

df_ = pd.read_excel("/Users/dorukakalin/Desktop/Python Internship/RFM/online_retail_II.xlsx", #Load Dataset
                    sheet_name="Year 2009-2010") #Name the excel sheet

df = df_.copy()

print(df.head()) #Display first 5 rows of the dataset
print(df.isnull().sum()) #Display number of null elements in the dataset

#Number of unique elements in description (number of products)
df["Description"].nunique()

#Number of each unique description (amount of each product)
df["Description"].value_counts().head()

#Products grouped by quantity ordered
df.groupby("Description").agg({"Quantity": "sum"}).head()


#The Data Frame sorted by var "Quantity" is descending order
df.groupby("Description").agg({"Quantity": "sum"}).sort_values("Quantity", ascending=False).head()

#Number of unique purchases
df["Invoice"].nunique()


# fatura basina ortalama kac para kazanilmistir? ,
# (iki değişkeni çarparak yeni bir değişken oluşturmak gerekmektedir)
# iadeleri çıkararak yeniden df'i oluşturalım

df = df[~df["Invoice"].str.contains("C", na=False)] #Removes rows from df where the Invoice column includes the substring 'C'

df["TotalPrice"] = df["Quantity"] * df["Price"] #Total Price for each purchase is equal to the unit price of product times amount ordered

df.sort_values("Price", ascending=False).head() #Sorts the price of each purchase in descending order

df["Country"].value_counts() #Calculates the number of purchases made from each country

df.groupby("Country").agg({"TotalPrice": "sum"}).sort_values("TotalPrice", ascending=False).head() #Groups df by country and calculates the total price accordingly


###############################################################
# Data Preparation
###############################################################

df.isnull().sum() #Number of null values in df
df.dropna(inplace=True) #Drops rows containing empty values

df.describe([0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99]).T #Describes the data frame in the given intervals and transposes the resul

###############################################################
# Calculating RFM Metrics
###############################################################

# Recency, Frequency, Monetary

# Recency (yenilik): Müşterinin son satın almasından bugüne kadar geçen süre
# Diğer bir ifadesiyle “Müşterinin son temasından bugüne kadar geçen süre” dir.

# Bugünün tarihi - Son satın alma
df["InvoiceDate"].max() #Max value in the invoice date column (latest)

today_date = dt.datetime(2010, 12, 11) #Today's date (Year, month, day)

#RFM Method to analyse customer behaviour
rfm = df.groupby('Customer ID').agg({'InvoiceDate': lambda date: (today_date - date.max()).days, #Recency: Days since last purchase
                                     'Invoice': lambda num: len(num), #Frequency: Number of pruchases
                                     'TotalPrice': lambda TotalPrice: TotalPrice.sum()}) #Monetary: Total money spent per customer


rfm.columns = ['Recency', 'Frequency', 'Monetary'] #Naming the columns of rfm to Recency, Frquency and Monetary

rfm = rfm[(rfm["Monetary"]) > 0 & (rfm["Frequency"] > 0)]

###############################################################
# Calculating RFM Scores
###############################################################


rfm["RecencyScore"] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1]) #Segments the Recency values into five and labels them from 1 to 5

rfm["FrequencyScore"] = pd.qcut(rfm['Frequency'], 5, labels=[1, 2, 3, 4, 5]) #Segments the Frequency values into five and labels them from 1 to 5

rfm["MonetaryScore"] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5]) #Segments the Monetary values into five and labels them from 1 to 5

#Converts the categorial columns of scores into numerical columns and merges them to get a final RFM score
rfm["RFM_SCORE"] = (rfm['RecencyScore'].astype(str) +
                    rfm['FrequencyScore'].astype(str) +
                    rfm['MonetaryScore'].astype(str)) 


rfm[rfm["RFM_SCORE"] == "555"].head() #Outputs the first five customers which have an rfm score of 555 (best possible score)

rfm[rfm["RFM_SCORE"] == "111"] #Outputs the customers who have an rfm score of 111 (worst possible score)

###############################################################
# Naming & Analysing RFM Segments
###############################################################

#Names and categorises customers which fall under a certain range of RFM score
seg_map = {
    r'[1-2][1-2]': 'Hibernating', #Customers who have a Recency AND Frequency score of 1-2 and
    r'[1-2][3-4]': 'At_Risk', #Customers who have a Recency score of 1-2 AND Frequency score of 3-4
    r'[1-2]5': 'Cant_Lose', #Customers who have a Recency score of 1-2 and a Frequency score of 5
    r'3[1-2]': 'About_to_Sleep', #Customers who have a Recency score of 3 AND Frequency score of 1-2
    r'33': 'Need_Attention', #Customers who have a Recency score of 3 AND Frequency score of 3
    r'[3-4][4-5]': 'Loyal_Customers', #Customers who have a Recency score of 3-4 AND Frequency score of 4-5
    r'41': 'Promising', #Customers who have a Recency score of 4 AND Frequency score of 1
    r'51': 'New_Customers', #Customers who have a Recency score of 5 AND Frequency score of 1
    r'[4-5][2-3]': 'Potential_Loyalists', #Customers who have a Recency score of 4-5 AND Frequency score of 2-3
    r'5[4-5]': 'Champions' #Customers who have a Recency score of 5 AND Frequency score of 4-5
}

rfm #Displays rfm

rfm['Segment'] = rfm['RecencyScore'].astype(str) + rfm['FrequencyScore'].astype(str) #Converts RecencyScore and FrequencyScore to numerical columns and combines them to create column "Segment"

rfm['Segment'] = rfm['Segment'].replace(seg_map, regex=True) #Replaces the values in seg_map with the new Segment variable according to the seg_map
df[["Customer ID"]].nunique() #Returns the number of unique customers
rfm[["Segment", "Recency", "Frequency", "Monetary"]].groupby("Segment").agg(["mean", "count"]) #Groups "Segment", "Recency", "Frequency" and "Monetary by Segment and returns the average result and the number

rfm[rfm["Segment"] == "Need_Attention"].head() #Returns the first five customers which fall under the "Need_Attention" segment
rfm[rfm["Segment"] == "Need_Attention"].index #Grabs the indexes of the customers which fall under the "Need_Attention" segment

new_df = pd.DataFrame() #Creates a new Data Frame

new_df["Need_Attention"] = rfm[rfm["Segment"] == "Need_Attention"].index #Creates a new column called "Need_Attention" in ned_df and copies the indexes from rfm which fall under the segment of "Need_Attention"

new_df.to_csv("RFM/Need_Attention.csv") #Writes the result to a csv file


############################################
# PROJE: RFM ile Müşteri Segmentasyonu
############################################
# Bir e-ticaret şirketi müşterilerini segmentlere ayırıp bu segmentlere göre pazarlama stratejileri belirlemek istiyor.
# online_retail_II.xlsx veri setinin "Year 2010-2011" isimli sheet'ine RFM analizi uygulayınız.

# Veri seti nerede? Aşağıdaki adreste yer alan "online_retail_II.xlsx" dosyasını indiriniz.
# https://www.kaggle.com/nathaniel/uci-online-retail-ii-data-set veya
# https://archive.ics.uci.edu/ml/machine-learning-databases/00502/

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

# RFM
# Recency afferim 5 puan gerçekten mantıklı bir 5 puan mı.
# sadakat programı : Need_Attention, At_Risk

# CLTV calculate
# CLTV prediction