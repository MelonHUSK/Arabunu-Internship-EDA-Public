import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

df = pd.DataFrame()
df = pd.read_csv("/Users/dorukakalin/Desktop/Python Internship/Spotify (Keyfi)/cleaned.csv")
df.sort_values(by="popularity", ascending=False, inplace=True)
df.drop_duplicates(subset="track_name", keep="first", inplace=True)

df = df.groupby("artists").agg({"popularity" : "sum"})
df.sort_values(by=["popularity"], ascending=False, inplace=True)
print(df.head())
df.to_csv("/Users/dorukakalin/Desktop/Python Internship/Spotify (Keyfi)/deeperAnalysis/popular artists.csv")

_df = pd.read_csv("/Users/dorukakalin/Desktop/Python Internship/Spotify (Keyfi)/cleaned.csv")
columns_to_remove = ["track_id", "index", "Unnamed: 0", "danceability","energy","key","loudness","mode","speechiness","acousticness","instrumentalness","liveness","valence","tempo","time_signature"]
_df.drop(columns=columns_to_remove, inplace=True)
artists = ["Bring Me The Horizon", "My Chemical Romance", "Green Day", "Nirvana", "Three Days Grace", "Paramore", "A Day To Remember", "blink-182", "Sleeping With Sirens", "The Offspring", "Papa Roach", "Emmure"]
df_new = pd.DataFrame()

for artists in artists:
    df_temp = _df[_df["artists"] == artists]
    df_temp.sort_values(by=["popularity"], ascending=False, inplace=True)
    df_new = pd.concat([df_new, df_temp], axis=0)
    
df_new.to_csv("/Users/dorukakalin/Desktop/Python Internship/Spotify (Keyfi)/deeperAnalysis/popularsongs.csv")

print(_df.head())

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

cat_cols, num_but_cat, cat_but_car, final_cat_cols, num_cols = find_cols(_df)

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
                
univarte_analysis_num_col(_df)

