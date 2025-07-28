from playwright.sync_api import sync_playwright
import time
import os
from pathlib import Path

def block_resources(route, request):
    if request.resource_type in ["image", "stylesheet", "font", "media"]:
        route.abort()
    else:
        route.continue_()

def unduh_bi_rate_excel(folder_unduh="downloads"):
    os.makedirs(folder_unduh, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"],
        )
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            accept_downloads=True,
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/115.0.0.0 Safari/537.36"
            )
        )

        page = context.new_page()
        page.route("**/*", block_resources)

        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)

        try:
            url = "https://www.bi.go.id/id/statistik/indikator/data-inflasi.aspx"
            page.goto(url, timeout=90000, wait_until="domcontentloaded")

            with page.expect_download() as download_info:
                page.click('input[id^="ctl00_ctl54_g_"][id$="_ButtonExport"]')
            download = download_info.value

            nama_file = download.suggested_filename
            path_file = Path(folder_unduh) / nama_file
            download.save_as(str(path_file))

            print(f"✅ File berhasil diunduh: {path_file}")

        except Exception as e:
            print(f"❌ Gagal mengunduh file BI Rate: {e}")
        finally:
            context.close()
            browser.close()

if __name__ == "__main__":
    mulai = time.time()
    unduh_bi_rate_excel()
    print(f"⏱️ Durasi: {round(time.time() - mulai, 2)} detik")
