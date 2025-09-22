import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns


cat_lim = 10

df = pd.read_csv("/Users/dorukakalin/Desktop/Python Internship/Diabetes/diabetes.csv")

#Number of Diabetes Patients
print(df.agg({"Outcome" : "sum"}))

#Determining Columns
def data_frame_information(df):
    cat_cols, num_but_cat, cat_but_car, final_cat_cols, num_cols = find_cols(df)
    target_var = find_target(df)
    df_length = len(df.axes[0])
    id_var = find_id(df, df_length)
    return cat_cols, num_but_cat, cat_but_car, final_cat_cols, num_cols, target_var, id_var

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
 
def find_target(df, target_lim = 2):
    target_var = [col for col in df.columns if df[col].nunique() == target_lim
                  and df[col].dtypes != "O"]
    return target_var

def find_id(df, df_length):
    id_var = [col for col in df.columns if df[col].nunique() == df_length]
    return id_var

#Outputting result
cat_cols, num_but_cat, cat_but_car, final_cat_cols, num_cols, target_var, id_var = data_frame_information(df)
print(["Cat cols:"] + [cat_cols])
print(["Num but cat:"] + [num_but_cat])
print(["Cat but car:"] + [cat_but_car])
print(["Num cols:"] + [num_cols])
print(["Finals Cat Cols:"] + [final_cat_cols])
print(["Target var:"] + [target_var])
print(["ID var:"] + [id_var])
print(["Data frame shape:"] + [df.shape]) 

#Start and end of data frame
print(df.head())
print(df.tail())

#Output of the corrolation between variables
print(df.corr(numeric_only=True))


#Plotting numerical and categorical columns
def univarte_analysis_num_col(df):
    for col in num_cols:
        if df[col].nunique() > cat_lim:
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

#Locating Outliers by Using Boxplot
def boxplot_analysis(df):
    for col in num_cols:
        if df[col].nunique() > cat_lim:
            plt.figure(figsize=(8, 6))
            sns.boxplot(data=df,x=col)
            plt.title(f'Boxplot of {col}')
            plt.xlabel(col)
            plt.show()

boxplot_analysis(df)

#Plotting corrolations
ax = sns.heatmap(df.corr(), annot=True)
plt.show()

#Corrolation Between Age / Outcome
plt.figure(figsize=(10, 6))
sns.boxplot(x='Outcome', y='Age', data=df)
plt.title('Box Plot of Age by Outcome')
plt.xlabel('Outcome')
plt.ylabel('Age')
plt.show()

#Corrolation Between BMI / Outcome
plt.figure(figsize=(10, 6))
sns.boxplot(x='Outcome', y='BMI', data=df)
plt.title('Box Plot of BMI by Outcome')
plt.xlabel('Outcome')
plt.ylabel('Age')
plt.show()

#Corrolation Between Insulin / Outcome
plt.figure(figsize=(10, 6))
sns.boxplot(x='Outcome', y='Glucose', data=df)
plt.title('Box Plot of Glucose by Outcome')
plt.xlabel('Outcome')
plt.ylabel('Age')
plt.show()

#Glucose Cat
df["Glucose_cat"] = pd.cut(x=df['Glucose'],
                                   bins=[0, 50, 100, 150, 200],
                                   labels=["Glucose_0_50", "Glucose_51_100", "Glucose_101_150", "Glucose_151_200"])
df.drop(df.columns[[1]], axis=1, inplace=True)

#BMI Cat
df["BMI_cat"] = pd.cut(x=df['BMI'],
                                   bins=[0, 15, 30, 45, 60],
                                   labels=["BMI_0_15", "BMI_16_30", "BMI_31_45", "BMI_45_60"])
df.drop(df.columns[[5]], axis=1, inplace=True)


class_data = df[df["Outcome"] == 1]

BMI_0_15 = class_data[class_data["BMI_cat"] == "BMI_0_15"].shape[0]
BMI_16_30 = class_data[class_data["BMI_cat"] == "BMI_16_30"].shape[0]
BMI_31_45 = class_data[class_data["BMI_cat"] == "BMI_31_45"].shape[0]
BMI_46_60 = class_data[class_data["BMI_cat"] == "BMI_46_60"].shape[0]

labels = "0-15", "16-30", "31-45", "45-69"
sizes = [BMI_0_15, BMI_16_30, BMI_31_45, BMI_46_60]
colors = ['skyblue', 'lightcoral']

plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=150)
plt.axis('equal')  
plt.title('Distribution of Diabetes by the BMI Index')
plt.show()

class_data = df[df["Outcome"] == 1]

Glucose_0_50 = class_data[class_data["Glucose_cat"] == "Glucose_0_50"].shape[0]
Glucose_51_100 = class_data[class_data["Glucose_cat"] == "Glucose_51_100"].shape[0]
Glucose_101_150 = class_data[class_data["Glucose_cat"] == "Glucose_101_150"].shape[0]
Glucose_151_200 = class_data[class_data["Glucose_cat"] == "Glucose_151_200"].shape[0]

labels = "0-50", "51-100", "101-150", "151-200"
sizes = [Glucose_0_50, Glucose_51_100, Glucose_101_150, Glucose_151_200]
colors = ['skyblue', 'lightcoral', 'slateblue', 'seagreen']

plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=150)
plt.axis('equal')  
plt.title('Distribution of Diabetes by Glucose')
plt.show()

#Categorising 
df["patient_level_based"] = df["Pregnancies_cat"] + "_" + df["Glucose_cat"] + "_" + df["BloodPressure_cat"] + "_" + df["SkinThickness_cat"] + "_" + df["Insulin_cat"] + "_" + df["BMI_cat"] + "_" + df["DiabetesPedigreeFunction_cat"] + "_" + df["Age_cat"]
df.to_csv("/Users/dorukakalin/Desktop/Python Internship/Diabetes/categories.csv")
print(df)