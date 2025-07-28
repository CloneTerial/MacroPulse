import requests
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
import re
import dotenv 

dotenv.load_dotenv()
BPS_API_KEY = dotenv.get_key(dotenv.find_dotenv(), "BPS_API_KEY")
rss_feeds = { 
    "crypto": [
        "https://cointelegraph.com/rss",
        "https://www.coindesk.com/arc/outboundfeeds/rss/",
        "https://decrypt.co/feed"
    ]
}

NAMESPACES = {
    'media': 'http://search.yahoo.com/mrss/',
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'dc': 'http://purl.org/dc/elements/1.1/',
}

def ambil_gambar(item, domain):
    media = item.find('media:content', NAMESPACES)
    if media is not None and 'url' in media.attrib:
        return media.attrib['url']
    if domain == "decrypt.co":
        thumb = item.find('media:thumbnail')
        if thumb is not None:
            return thumb.attrib.get('url')
        enc = item.find('enclosure')
        if enc is not None:
            return enc.attrib.get('url')
    if domain == "cointelegraph.com":
        enc = item.find('enclosure')
        if enc is not None:
            return enc.attrib.get('url')
    return None

def ambil_konten_penuh(item):
    tag = item.find('content:encoded', NAMESPACES)
    return tag.text.strip() if tag is not None and tag.text else None

def extract_deskripsi(deskripsi, domain):
    if domain == "cointelegraph.com":
        ps = re.findall(r"<p.*?>(.*?)</p>", deskripsi, re.DOTALL)
        for p in ps:
            if "<img" not in p:
                return re.sub("<.*?>", "", p).strip()
    return re.sub("<.*?>", "", deskripsi or "").strip()

def ambil_berita(kategori: str, max_berita: int = 10, keyword_filter: list = None):
    berita = []

    for rss in rss_feeds.get(kategori, []):
        try:
            res = requests.get(rss, timeout=10)
            res.raise_for_status()
            root = ET.fromstring(res.content)
            domain = urlparse(rss).netloc.replace("www.", "")
            items = root.findall('.//item')

            for item in items:
                judul = item.findtext('title')
                link = item.findtext('link')
                published = item.findtext('pubDate') or ""
                deskripsi = item.findtext('description') or ""

                if keyword_filter and not any(k.lower() in judul.lower() for k in keyword_filter):
                    continue

                image_url = ambil_gambar(item, domain)
                konten_penuh = ambil_konten_penuh(item) if "coindesk.com" in domain else None
                deskripsi_bersih = extract_deskripsi(deskripsi, domain)

                berita.append({
                    "judul": judul.strip(),
                    "link": link,
                    "sumber": domain,
                    "published": published,
                    "image_url": image_url,
                    "deskripsi": deskripsi_bersih,
                    "konten_penuh": konten_penuh
                })

        except Exception as e:
            print(f"⚠️ Gagal ambil dari {rss}\nError: {e}\n")

    berita = sorted(berita, key=lambda x: x['published'], reverse=True)[:max_berita]
    return berita

if __name__ == "__main__":
    hasil = ambil_berita("crypto", max_berita=5)
    for b in hasil:
        print(f"[{b['sumber']}] {b['judul']} ({b['published']})")
        print(f"🔗 {b['link']}")
        if b['image_url']:
            print(f"🖼️ Gambar: {b['image_url']}")
        if b['deskripsi']:
            print(f"📝 Deskripsi: {b['deskripsi'][:150]}...")
        print("=" * 60)
