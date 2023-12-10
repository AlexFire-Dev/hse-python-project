import pandas as pd

df = pd.read_csv("init.csv")
print(df.shape)
df = df.sample(frac=0.02, replace=False, random_state=1)
df.to_csv("dataframe.csv")
print(df.shape)
