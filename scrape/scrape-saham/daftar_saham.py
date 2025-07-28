from playwright.sync_api import sync_playwright
from pathlib import Path
import pandas as pd
import re

FOLDER = "downloads_idx"

def unduh_idx_daftar_saham(url="https://www.idx.co.id/id/data-pasar/data-saham/daftar-saham", folder=FOLDER):
    Path(folder).mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_selector("button.btn-download", timeout=60000)
        with page.expect_download() as dl:
            page.click("button.btn-download")
        download = dl.value
        path = Path(folder) / download.suggested_filename
        download.save_as(str(path))
        print("✅ File terbaru tersimpan:", path)
        context.close()
        browser.close()
        return path

def _baca_file_excel_terbaru(folder=FOLDER):
    files = sorted(Path(folder).glob("*.xlsx"), key=lambda f: f.stat().st_mtime, reverse=True)
    if not files:
        raise FileNotFoundError("❌ Tidak ada file Excel ditemukan di folder unduhan.")
    return files[0]

def kode_saham(jumlah=5):
    path_excel = _baca_file_excel_terbaru()
    df = pd.read_excel(path_excel)
    df = df[["Kode", "Nama Perusahaan"]].dropna()
    return df["Kode"].head(jumlah).tolist()

def semua_saham():
    path_excel = _baca_file_excel_terbaru()
    df = pd.read_excel(path_excel)
    df = df[["Kode", "Nama Perusahaan"]].dropna()
    return set(df["Kode"])
