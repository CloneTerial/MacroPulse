from playwright.sync_api import sync_playwright
import time

browser_context = None

def block_resources(route, request):
    if request.resource_type in ["image", "stylesheet", "font", "media"]:
        route.abort()
    else:
        route.continue_()

def ambil_data_indikator_bi():
    global browser_context

    if browser_context is None:
        playwright = sync_playwright().start()
        browser_context = playwright.chromium.launch_persistent_context(
            user_data_dir="./profile_BI",
            headless=True,
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1280, "height": 720},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/115.0.0.0 Safari/537.36"
            )
        )
    
    page = browser_context.new_page()
    page.route("**/*", block_resources)

    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """)

    try:
        url = "https://www.bi.go.id/id/statistik/indikator/default.aspx"
        page.goto(url, timeout=30000, wait_until="domcontentloaded")

        container = page.wait_for_selector(".landing-page-indikator", timeout=10000)
        cards = page.query_selector_all(".landing-page-indikator .box-list")

        print("📊 Data Indikator Ekonomi BI:\n")

        for card in cards:
            try:
                title = card.query_selector("p").inner_text().strip()
                value = card.query_selector("h2").inner_text().strip()
                date = card.query_selector_all("p")[1].inner_text().strip()
                print(f"📌 {title}: {value} (📅 {date})")
            except:
                continue

    except Exception as e:
        print(f"❌ Gagal mengambil data indikator BI: {e}")
    finally:
        page.close()

def shutdown_browser():
    global browser_context
    if browser_context:
        browser_context.close()
        browser_context = None

if __name__ == "__main__":
    mulai = time.time()
    ambil_data_indikator_bi()
    shutdown_browser()
    print(f"\n⏱️ Durasi: {round(time.time() - mulai, 2)} detik")
