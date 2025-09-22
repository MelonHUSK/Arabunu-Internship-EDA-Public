import numpy as np
import pandas as pd
import seaborn as sns 
from matplotlib import pyplot as plt

#Load & Clean Data
df = pd.read_csv("/Users/dorukakalin/Desktop/Python Internship/AB Testing/cookie_cats.csv")
df_cleaned = df[df["sum_gamerounds"] <= 493]
df_cleaned["version"] = df_cleaned["version"].replace("gate_40", 1) 
df_cleaned["version"] = df_cleaned["version"].replace("gate_30", 0) 
df_cleaned["retention_1"] = df_cleaned["retention_1"].replace(True, 1) 
df_cleaned["retention_1"] = df_cleaned["retention_1"].replace(False, 0) 
df_cleaned["retention_7"] = df_cleaned["retention_7"].replace(True, 1) 
df_cleaned["retention_7"] = df_cleaned["retention_7"].replace(False, 0) 

#Datasets
df_40 = df_cleaned.loc[df_cleaned["version"] == 1]
df_30 = df_cleaned.loc[df_cleaned["version"] == 0]

#Avg Gamerounds per Versiob
gt_40_avg = df_40["sum_gamerounds"].mean()
gt_30_avg = df_30["sum_gamerounds"].mean()

#EDA - Corrolation
ax = sns.heatmap(df_cleaned.corr(), annot=True)
plt.show()

#Retention Rate (1 Day)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

df = df_cleaned[df_cleaned["version"] == 1]
retained_count = df[df["retention_1"] == 1].shape[0]
left_count = df[df["retention_1"] == 0].shape[0]
labels = 'Retained', 'Left'
sizes = [retained_count, left_count]
colors = ['skyblue', 'lightcoral']
ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=150)
ax1.axis('equal')  
ax1.set_title('Retention of Players - Gate at 40 - 1 Day')


df = df_cleaned[df_cleaned["version"] == 0]
retained_count = df[df["retention_1"] == 1].shape[0]
left_count = df[df["retention_1"] == 0].shape[0]
labels = 'Retained', 'Left'
sizes = [retained_count, left_count]
colors = ['skyblue', 'lightcoral']
ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=150)
ax2.axis('equal')  
ax2.set_title('Retention of Players - Gate at 30 - 1 Day')

plt.tight_layout()
plt.show()

#Retention Rate (7 Days)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

df = df_cleaned[df_cleaned["version"] == 1]
retained_count = df[df["retention_7"] == 1].shape[0]
left_count = df[df["retention_7"] == 0].shape[0]
labels = 'Retained', 'Left'
sizes = [retained_count, left_count]
colors = ['skyblue', 'lightcoral']
ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=150)
ax1.axis('equal')  
ax1.set_title('Retention of Players - Gate at 40 - 1 Week')


df = df_cleaned[df_cleaned["version"] == 0]
retained_count = df[df["retention_7"] == 1].shape[0]
left_count = df[df["retention_7"] == 0].shape[0]
labels = 'Retained', 'Left'
sizes = [retained_count, left_count]
colors = ['skyblue', 'lightcoral']
ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=150)
ax2.axis('equal')  
ax2.set_title('Retention of Players - Gate at 30 - 1 Week')

plt.tight_layout()
plt.show()

#Number of Games Played
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

sns.histplot(df_40["sum_gamerounds"], kde=True, ax=ax1)
ax1.set_title(f'Histogram of Sum of Games Played - Gate 40')
ax1.set_xlabel("Sum of Games Played")
ax1.set_ylabel('Frequency')

sns.histplot(df_30["sum_gamerounds"], kde=True, ax=ax2)
ax2.set_title(f'Histogram of Sum of Games Played - Gate 30')
ax2.set_xlabel("Sum of Games Played")
ax2.set_ylabel('Frequency')

plt.tight_layout()
plt.show()

# Statistical Test: Permutation Test with Median
df_median = df_cleaned.copy()
np.random.seed(34)
median_null = []

observed_diff = df_cleaned.groupby('version')['sum_gamerounds'].median().diff().iloc[-1]

num_permutations = 5000

# Perform permutations and calculate median differences
for i in range(num_permutations):
    df_permuted = df_cleaned.copy()
    df_permuted['sum_gamerounds'] = np.random.permutation(df_permuted['sum_gamerounds'])
    diff_median = df_permuted.groupby('version')['sum_gamerounds'].median().diff().iloc[-1]
    median_null.append(diff_median)

# Calculate p-value (proportion of differences less than observed_diff)
p_value = np.mean(np.abs(np.array(median_null)) < 0.05 * np.median(df_cleaned["sum_gamerounds"]))

# Plotting histogram of median differences under null hypothesis
plt.figure(figsize=(8, 6))
sns.histplot(median_null, kde=True)
plt.axvline(0.05 * np.median(df_cleaned["sum_gamerounds"]), color='red', linestyle='--', label=f'5% of Median\n(p-value={p_value:.3f})')
plt.title('Distribution of Median Differences under Null Hypothesis')
plt.xlabel('Difference in Median Gamerounds')
plt.ylabel('Frequency')
plt.legend()
plt.show()

#Statistical Test: Permutation Test with Mean
df_mean = df_cleaned.copy()
np.random.seed(34)
mean_null = []

observed_diff = df_cleaned.groupby('version')['sum_gamerounds'].mean().diff().iloc[-1]

num_permutations = 5000

# Perform permutations and calculate median differences
for i in range(num_permutations):
    df_permuted = df_cleaned.copy()
    df_permuted['sum_gamerounds'] = np.random.permutation(df_permuted['sum_gamerounds'])
    diff_mean = df_permuted.groupby('version')['sum_gamerounds'].mean().diff().iloc[-1]
    mean_null.append(diff_mean)

# Calculate p-value (proportion of differences less than observed_diff)
p_value = np.mean(np.abs(np.array(mean_null)) < 0.05 * np.mean(df_cleaned["sum_gamerounds"]))

# Plotting histogram of median differences under null hypothesis
plt.figure(figsize=(8, 6))
sns.histplot(mean_null, kde=True)
plt.axvline(0.05 * np.mean(df_cleaned["sum_gamerounds"]), color='red', linestyle='--', label=f'5% of Median\n(p-value={p_value:.3f})')
plt.title('Distribution of Mean Differences under Null Hypothesis')
plt.xlabel('Difference in Mean Gamerounds')
plt.ylabel('Frequency')
plt.legend()
plt.show()