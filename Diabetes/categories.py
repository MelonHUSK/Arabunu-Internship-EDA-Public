import pandas as pd

# Read data
df = pd.read_csv("/Users/dorukakalin/Desktop/Python Internship/Diabetes/diabetes.csv")
df = pd.DataFrame(df)

# Create categorical columns
df["Pregnancies_cat"] = pd.cut(df['Pregnancies'],
                               bins=[0, 3, 6, 12, 18],
                               labels=["Pregnancy_0_3", "Pregnancy_4_6", "Pregnancy_7_12", "Pregnancy_13_18"])

df["Glucose_cat"] = pd.cut(df['Glucose'],
                           bins=[0, 50, 100, 150, 200],
                           labels=["Glucose_0_50", "Glucose_51_100", "Glucose_101_150", "Glucose_151_200"])

df["BloodPressure_cat"] = pd.cut(df['BloodPressure'],
                                 bins=[0, 30, 60, 90, 120],
                                 labels=["BloodPressure_0_30", "BloodPressure_31_60", "BloodPressure_61_90", "BloodPressure_91_120"])

df["SkinThickness_cat"] = pd.cut(df['SkinThickness'],
                                 bins=[0, 10, 20, 30, 50],
                                 labels=["SkinThickness_0_10", "SkinThickness_11_20", "SkinThickness_21_30", "SkinThickness_31_50"])

df["Insulin_cat"] = pd.cut(df['Insulin'],
                           bins=[0, 100, 200, 300, 900],
                           labels=["Insulin_0_100", "Insulin_101_200", "Insulin_201_300", "Insulin_301_900"])

df["BMI_cat"] = pd.cut(df['BMI'],
                       bins=[0, 15, 30, 45, 60],
                       labels=["BMI_0_15", "BMI_16_30", "BMI_31_45", "BMI_45_60"])

df["DiabetesPedigreeFunction_cat"] = pd.cut(df['DiabetesPedigreeFunction'],
                                            bins=[0, 2],
                                            labels=["DiabetesPedigreeFunction_0_2"])

df["Age_cat"] = pd.cut(df['Age'],
                       bins=[0, 20, 40, 60, 90],
                       labels=["Age_0_20", "Age_21_40", "Age_41_60", "Age_61_90"])

#Counting
df = df.groupby(["Pregnancies_cat","Glucose_cat","BloodPressure_cat","SkinThickness_cat","Insulin_cat","BMI_cat","DiabetesPedigreeFunction_cat","Age_cat"]).agg({"Outcome" : "sum"})
df.sort_values(by=["Outcome"], ascending=False, inplace=True)
df.reset_index(inplace=True)
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)
df.to_csv("Diabetes/categories.csv")


# Convert categorical columns to string before concatenation
df["Pregnancies_cat"] = df["Pregnancies_cat"].astype(str)
df["Glucose_cat"] = df["Glucose_cat"].astype(str)
df["BloodPressure_cat"] = df["BloodPressure_cat"].astype(str)
df["SkinThickness_cat"] = df["SkinThickness_cat"].astype(str)
df["Insulin_cat"] = df["Insulin_cat"].astype(str)
df["BMI_cat"] = df["BMI_cat"].astype(str)
df["DiabetesPedigreeFunction_cat"] = df["DiabetesPedigreeFunction_cat"].astype(str)
df["Age_cat"] = df["Age_cat"].astype(str)

# Concatenate categorical columns
df["patient_level_based"] = df["Pregnancies_cat"] + "_" + df["Glucose_cat"] + "_" + df["BloodPressure_cat"] + "_" + df["SkinThickness_cat"] + "_" + df["Insulin_cat"] + "_" + df["BMI_cat"] + "_" + df["DiabetesPedigreeFunction_cat"] + "_" + df["Age_cat"]
df.drop(columns=["Pregnancies_cat","Glucose_cat","BloodPressure_cat","SkinThickness_cat","Insulin_cat","BMI_cat","DiabetesPedigreeFunction_cat","Age_cat"], inplace=True)
df = df.drop(df[df['Outcome'] == 0].index)

# Save to CSV
df.to_csv("/Users/dorukakalin/Desktop/Python Internship/Diabetes/categories.csv")
print(df.agg({"Outcome" : "sum"}))