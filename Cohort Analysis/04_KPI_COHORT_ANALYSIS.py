############################################
# KPI & COHORT ANALIZI: RETENTION RATE
############################################

# 3 ADIMDA RETENTION RATE KPI'NIN COHORT ANALIZINE SOKULMASI

# 1. Veri ön işleme
# 2. Retention matrisinin oluşturulması
#    1. Her bir müşteri için eşsiz sipariş sayısının hesaplanması
#    2. Tüm veri setinde bir kereden fazla sipariş veren müşteri oranı.
#    3. Sipariş aylarının yakalanması.
#    4. Cohort değişkeninin oluşturulması.
#    5. Aylık müşteri sayılarını çıkarılması.
#    6. Periyod numarasının çıkarılması
#    7. Cohort_pivot'un oluşturulması
#    8. Retention_matrix'in oluşturulması
# 3. Retention matrisinin ısı haritası ile görselleştirilmesi


####################################
# 1. Veri ön işleme
####################################


import numpy as np
import pandas as pd
pd.set_option('display.max_rows', 10)
import matplotlib.pyplot as plt
import warnings
import seaborn as sns
from operator import attrgetter
import matplotlib.colors as mcolors

df_ = pd.read_excel('Cohort Analysis/online_retail.xlsx', #Load dataset
                   dtype={'CustomerID': str,
                          'InvoiceID': str}, #Set var types to string (obj)
                   parse_dates=['InvoiceDate']) #Convert the data in the dataset to dates usable by pandas
df = df_.copy()
print(df.head() )#Display first 10 rows of df 
print(df.shape ) #Display the shape of df
print(df.info()) #Display info about the columns of df

df.dropna(subset=['CustomerID'], inplace=True) #Drop rows in which the 'customer_id' column is empty
df = df[['CustomerID', 'InvoiceNo', 'InvoiceDate']].drop_duplicates() #Drop rows in which there are duplicates of 'CustomerID', 'InvoiceNo' or 'InvoiceDate'

print(df.shape) #Display new shape

####################################
# 2. Retention matrisinin oluşturulması
####################################

# SONUC
# n_orders = df.groupby(['CustomerID'])['InvoiceNo'].nunique()
# orders_perc = np.sum(n_orders > 1) / df['CustomerID'].nunique()
# df['order_month'] = df['InvoiceDate'].dt.to_period('M')
# df['cohort'] = df.groupby('CustomerID')['InvoiceDate'] \
#     .transform('min') \
#     .dt.to_period('M')
# df_cohort = df.groupby(['cohort', 'order_month']) \
#     .agg(n_customers=('CustomerID', 'nunique')) \
#     .reset_index(drop=False)
# df_cohort['period_number'] = (df_cohort.order_month - df_cohort.cohort).apply(attrgetter('n'))
# cohort_pivot = df_cohort.pivot_table(index='cohort',
#                                      columns='period_number',
#                                      values='n_customers')
#
# cohort_size = cohort_pivot.iloc[:, 0]
# retention_matrix = cohort_pivot.divide(cohort_size, axis=0)


n_orders = df.groupby(['CustomerID'])['InvoiceNo'].nunique() #Calculates the amount of purchases per customer 

orders_perc = np.sum(n_orders > 1) / df['CustomerID'].nunique()
100*orders_perc #Percentage value of customers who places and order more than once compared to unique customers

df['order_month'] = df['InvoiceDate'].dt.to_period('M') #The month in which the orders were placed are calculated

#Groups customer ids by their invoice date and selects the earliest (min) month in which a purchase was made
df['cohort'] = df.groupby('CustomerID')['InvoiceDate'] \
    .transform('min') \
    .dt.to_period('M')

#Group df by cohort and order_month, then aggregate to count unique customers in CustomerID
df_cohort = df.groupby(['cohort', 'order_month']) \
    .agg(n_customers=('CustomerID', 'nunique')) \
    .reset_index(drop=False) #Resets index and grouped columns are added back to the DF


(df_cohort.order_month - df_cohort.cohort).head() #Calculates the difference of time in months between a purchase and the user's cohort month

#Calculates the period difference between order_month and cohort_month in months
df_cohort['period_number'] = (df_cohort.order_month - df_cohort.cohort).apply(attrgetter('n'))

#Creates a pivot table with the index (grouped by) cohort. The column name is period_number and the values are n_customers
cohort_pivot = df_cohort.pivot_table(index='cohort',
                                     columns='period_number',
                                     values='n_customers')
#In essance, this pivot table shows the amount of customers in each cohort month

cohort_size = cohort_pivot.iloc[:, 0] #Selects all rows in cohort_pivot except for the first column

retention_matrix = cohort_pivot.divide(cohort_size, axis=0) #Divides cohort_pivot by its size along the 0 axis (horizontally)
retention_matrix #Displays the retention maxis



def create_retention_matrix(dataframe): #Defines a new function to create a retention matrix for a data frame
    n_orders = dataframe.groupby(['CustomerID'])['InvoiceNo'].nunique() #n_orders is the amount of unique purchases made by customers
    dataframe['order_month'] = dataframe['InvoiceDate'].dt.to_period('M') #order_month extracts the month out of the purchase date of a given purchase
    #Calculates the cohort month of purchase by extracting the month out of all purchases made by a user and selecting the min value (earliest)
    dataframe['cohort'] = dataframe.groupby('CustomerID')['InvoiceDate'] \
        .transform('min') \
        .dt.to_period('M')
    #Group dataframe by cohort and order_month, then aggregate to count unique customers in CustomerID
    df_cohort = dataframe.groupby(['cohort', 'order_month']) \
        .agg(n_customers=('CustomerID', 'nunique')) \
        .reset_index(drop=False) #Resets index without dropping the previous columns
    df_cohort['period_number'] = (df_cohort.order_month - df_cohort.cohort).apply(attrgetter('n'))
    #Creates a pivot table with the index (grouped by) cohort. The column name is period_number and the values are n_customers
    cohort_pivot = df_cohort.pivot_table(index='cohort',
                                         columns='period_number',
                                         values='n_customers')
    #In essance, this pivot table shows the amount of customers in each cohort month
    cohort_size = cohort_pivot.iloc[:, 0] #Selects all rows in cohort_pivot except for the first column to get the size of the array along the 0 axis
    retention_matrix = cohort_pivot.divide(cohort_size, axis=0) #Divides cohort_pivot by its size along the 0 axis (horizontally)
    return retention_matrix #Returns the retention matrix


create_retention_matrix(df)
#Calls the function for the dataframe df

####################################
# 3. Retention matrisinin ısı haritası ile görselleştirilmesi
####################################


sns.axes_style("white") #Sets the global style for seaborn plots to "white"
fig, ax = plt.subplots(1, 2, #Specifies that 1 row and 2 columns are subplots
                       figsize=(12, 8), #Sets the resolution for the plot
                       sharey=True,  #Shares the y-axis between the subplots which ensures that they have the same scale
                       gridspec_kw={'width_ratios': [1, 11]} #Adjusts the width reatios of the subplots to 1 by 11
                       # to create the grid the subplots are placed on
                       )

#Creation or retention matrix as a heatmap
sns.heatmap(retention_matrix, #Creates a hetmap for the retention matrix
            annot=True, #Anotates the values shown on the heatmap
            fmt='.0%',  #Shows the percentage values shown on the graph
            cmap='RdYlGn',  #Colourscheme of the heatmap
            ax=ax[1])  #Selects the ax variable defined previously as the heatmaps axis (2nd column)

#Labeling the heatmap
ax[1].set_title('Monthly Cohorts: User Retention', fontsize=16) 
ax[1].set(xlabel='# of periods', ylabel='')


#Cohort Size
cohort_size_df = pd.DataFrame(cohort_size).rename(columns={0: 'cohort_size'}) #Rename the column with index 0 to 'cohort_size' in the cohort_size df which will be equal to a new df called cohort_size_df
white_cmap = mcolors.ListedColormap(['white']) #var white_cmap is equal to the colourscheme "white"
sns.heatmap(cohort_size_df, #Creates a seaborn heatmap for the cohort_size_df dataframe
            annot=True,  #Anotates the values of the graph
            cbar=False,  #Tells the script to not draw a colour bar while displaying the graph
            fmt='g',     #Uset green colour for formatting text
            cmap=white_cmap, #Uses the previously defined white_cmap variable as the colour scheme for the graph
            ax=ax[0])  #Selects the ax variable defined previously as the heatmaps axis (1st column)
fig.tight_layout() #Defines the layout of the graph
plt.show() #Displays the graph



# RECAP
# Virtual env.
# Dependency man.
# Python (functions, if-else, loops, list comp.)
# EDA

# PROJE'den elde edilmesi gereken çıktılar nelerdi?
# - Herhangi ds, ml tekniği bilmeyen kişi nasıl segmentasyon yapar bunu görmek.
# - Dinamik label ve bin oluşturmak
# - Elimizde herhangi verisi olmadığı halde olası müşteri potansiyelini belirlemek (sınıflandırmak)

#Solution for the previous excercise (users purchases)
import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
users = pd.read_csv('/Users/dorukakalin/Desktop/Python Internship/Cohort Analysis/users.csv') #Read data
purchases = pd.read_csv('/Users/dorukakalin/Desktop/Python Internship/Cohort Analysis/purchases.csv') #Read data
df = purchases.merge(users, how='inner', on='uid') #Merge both datasets by innermerde on the var 'uid'

agg_df = df.groupby(by=["country", 'device', "gender", "age"]).agg({"price": "sum"}).sort_values("price", ascending=False) #Group the datagrame by country, device, gender and age to find the sum of the price variable in these groups
agg_df = agg_df.reset_index() #Reset indexes
bins = [0, 19, 24, 31, 41, agg_df["age"].max()] #Create bins for the age var
mylabels = ['0_18', '19_23', '24_30', '31_40', '41_' + str(agg_df["age"].max())] #Create labels for these bins
agg_df["age_cat"] = pd.cut(agg_df["age"], bins, labels=mylabels) #Create a new variable called "age_cat" and categorise users according to their age using the bins and labels


agg_df["customers_level_based"] = [row[0] + "_" + row[1].upper() + "_" + row[2] + "_" + row[5] for row in agg_df.values] #Merge multiple columns into one big column
agg_df = agg_df[["customers_level_based", "price"]] #Only include the new "customers_level_based" and "price" columns in the dataframe
agg_df = agg_df.groupby("customers_level_based").agg({"price": "mean"}) #Group customer_level_based in agg_df and find the mean value of these groups
agg_df = agg_df.reset_index() #Reset index

agg_df["segment"] = pd.qcut(agg_df["price"], 4, labels=["D", "C", "B", "A"]) #Create 4 segments for the price variable and label them D, C, B and A

new_user = "TUR_IOS_F_41_75"
new_user = "USA_AND_F_31_40"
agg_df[agg_df["customers_level_based"] == new_user] #Returns the row containing new_user

