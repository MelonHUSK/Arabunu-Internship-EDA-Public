import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

df = pd.read_csv("Spotify (Keyfi)/dataset.csv")
#print(df["track_genre"].unique())

def find_cols(df, cat_lim = 10, car_lim = 20):
    num_cols = [col for col in df.columns if df[col].dtypes != "O"]
    num_but_cat = [col for col in df.columns if df[col].nunique() < cat_lim and
                   df[col].dtypes != "O"]
    cat_cols = [col for col in df.columns if df[col].dtypes == "O"]
    cat_but_car = [col for col in df.columns if df[col].nunique() > car_lim and 
                   df[col].dtypes == "O"]
    final_cat_cols = cat_cols + num_but_cat
    final_cat_cols = [col for col in final_cat_cols if col not in cat_but_car]
    return cat_cols, num_but_cat, cat_but_car, final_cat_cols, num_cols

cat_cols, num_but_cat, cat_but_car, final_cat_cols, num_cols = find_cols(df)

def univarte_analysis_num_col(df):
    for col in num_cols:
        if df[col].nunique() > 10:
            plt.figure(figsize=(8, 6))
            sns.histplot(df[col], kde=True)
            plt.title(f'Histogram of {col}')
            plt.xlabel(col)
            plt.ylabel('Frequency')
            plt.show()
        else:
            plt.figure(figsize=(8, 6))
            ax = sns.countplot(x=col, data=df)
            plt.title(f'Count of {col}')
            plt.xlabel(col)
            plt.ylabel('Count')
            for i in ax.patches:
                ax.annotate(format(i.get_height(), '.0f'), 
                            (i.get_x() + i.get_width() / 2., i.get_height()), 
                            ha = 'center', va = 'center', 
                            xytext = (0, 5), 
                            textcoords = 'offset points')
                plt.show()


univarte_analysis_num_col(df)

df.drop(columns=cat_cols, inplace=True)
ax = sns.heatmap(df.corr(), annot=True)
plt.show()