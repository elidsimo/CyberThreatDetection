import pandas as pd

url = "https://urlhaus.abuse.ch/downloads/csv_recent/"
df = pd.read_csv(url, comment="#")
df.to_csv("data/urls_brutes.csv", index=False)
print(df.head())
