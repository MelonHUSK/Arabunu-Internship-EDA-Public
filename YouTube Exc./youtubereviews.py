import pandas as pd
import math
from spicy import stats as st 
from sklearn.preprocessing import MinMaxScaler as mms

#Read Dataset
df = pd.read_csv("YouTube Exc./USvideos.csv")

#Clean Dataset
drop_columns = ["trending_date", "publish_time", "thumbnail_link","comments_disabled","ratings_disabled","video_error_or_removed","description", "tags"]
df.drop(columns=drop_columns, inplace=True)

#Rating Paramaters
df["likes_dislikes_diff"] = df["likes"] - df["dislikes"]

def likes_ratio(likes_num, dislikes_num):
    if likes_num + dislikes_num == 0:
        return 0
    else:
        return (likes_num / (likes_num + dislikes_num)) * 100
    
df["likes_percentage"] = df.apply(lambda x: likes_ratio(x["likes"], x["dislikes"]), axis=1)

def wilson_lower_bound(likes_num, dislikes_num, confidence=0.95):
    n = likes_num + dislikes_num
    if n == 0:
        return 0
    z = st.norm.ppf(1-(1-confidence)/2)
    phat = 1.0 * likes_num / n
    return (phat+z*z/(2*n) - z*math.sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n)

df["wlb_likes"] = df.apply(lambda x: wilson_lower_bound(x["likes"], x["dislikes"]), axis=1)
df.drop_duplicates(subset="video_id", keep="first", inplace=True)

df.sort_values(by="wlb_likes", ascending=False, inplace=True)
df.to_csv("YouTube Exc./temp.csv")