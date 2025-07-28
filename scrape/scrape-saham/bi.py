import pandas as pd
from pathlib import Path

path_excel = Path("1.xlsx")

df = pd.read_excel(path_excel, skiprows=4, usecols="A:C", names=["No", "Periode", "Data Inflasi"])
df.dropna(how="all", inplace=True)
df = df[pd.to_numeric(df["No"], errors="coerce").notna()]
df["No"] = df["No"].astype(int)

print("Data Inflasi Terbaru:")
print(df.head(10).to_string(index=False))
