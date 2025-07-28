from playwright.sync_api import sync_playwright
from daftar_saham import kode_saham

def block_resources(route, request):
    if request.resource_type in ["image", "stylesheet", "font"]:
        route.abort()
    else:
        route.continue_()

def ambil_data_saham(kode):
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir="./profile_saham", headless=True
        )
        page = browser.new_page()
        page.route("**/*", block_resources)

        try:
            page.goto(f"https://finance.yahoo.com/quote/{kode}.JK", timeout=90000)
            page.wait_for_selector(
                '[data-testid="qsp-price"], [data-testid="qsp-price-change"], [data-testid="qsp-price-change-percent"]',
                state='attached',
                timeout=90000
            )

            harga_el = page.query_selector('[data-testid="qsp-price"]')
            change_el = page.query_selector('[data-testid="qsp-price-change"]')
            change_percent_el = page.query_selector('[data-testid="qsp-price-change-percent"]')

            print(f"\n📈 Data Saham {kode}:")
            if harga_el: print(f"  Harga: {harga_el.inner_text()}")
            if change_el: print(f"  Perubahan: {change_el.inner_text()}")
            if change_percent_el: print(f"  Persentase Perubahan: {change_percent_el.inner_text()}")
        except Exception as e:
            print(f"Gagal mengambil data {kode}: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    kode_saham = kode_saham(jumlah=5)
    for kode in kode_saham:
        ambil_data_saham(kode)
