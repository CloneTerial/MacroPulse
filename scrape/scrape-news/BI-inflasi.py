import pandas as pd
from pathlib import Path

path_excel = 'downloads/*.xlsx'
files = sorted(Path().glob(path_excel), key=lambda f: f.stat().st_mtime, reverse=True)
if not files:
    raise FileNotFoundError("❌ Tidak ada file Excel ditemukan di folder unduhan.")

df = pd.read_excel(files[0], skiprows=4, usecols="A:C", names=["No", "Periode", "Data Inflasi"])
df.dropna(how="all", inplace=True)
df = df[pd.to_numeric(df["No"], errors="coerce").notna()]
df["No"] = df["No"].astype(int)

print("Data Inflasi Terbaru:")
print(df.head(10).to_string(index=False))
