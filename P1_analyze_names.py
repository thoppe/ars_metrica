import pandas as pd

f_csv = "data/scored_names/yob2017.csv"

df = pd.read_csv(f_csv, dtype={'IPA_stress':str})
df['is_female'] = df.gender == "F"


g = df.groupby(["gender", "IPA_stress"])
print(g["counts"].sum().sort_values(ascending=False))

#print(df.groupby("IPA_stress").gender.mean())
print(df[df.IPA_stress=="0"])


