from playwright.sync_api import sync_playwright
from pathlib import Path

def unduh_idx_daftar_saham(url, folder="downloads_idx"):
    Path(folder).mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_selector("button.btn-download", timeout=90000)
        with page.expect_download() as dl:
            page.click("button.btn-download")
        download = dl.value
        path = Path(folder)/download.suggested_filename
        download.save_as(str(path))
        print("✅ Tersimpan di:", path)
        print(path)
        context.close()
        browser.close()

if __name__=="__main__":
    unduh_idx_daftar_saham("https://www.idx.co.id/id/data-pasar/data-saham/daftar-saham")
