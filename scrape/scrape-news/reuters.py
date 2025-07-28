import requests
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
import re

NAMESPACES = {
    'dc': 'http://purl.org/dc/elements/1.1/',
}

# Feed RSS Reuters
rss_feeds = {
    "reuters": [
        "https://ir.thomsonreuters.com/rss/news-releases.xml?items=15"
    ]
}

def extract_deskripsi(deskripsi):
    return re.sub("<.*?>", "", deskripsi or "").replace("&nbsp;", " ").strip()

def ambil_berita_reuters(max_berita: int = 10):
    berita = []

    for rss in rss_feeds["reuters"]:
        try:
            res = requests.get(rss, timeout=10)
            res.raise_for_status()
            root = ET.fromstring(res.content)
            items = root.findall('.//item')

            for item in items:
                judul = item.findtext('title')
                link = item.findtext('link')
                published = item.findtext('pubDate') or ""
                deskripsi = item.findtext('description') or ""
                penulis = item.findtext('dc:creator', namespaces=NAMESPACES) or "Reuters"

                berita.append({
                    "judul": judul.strip(),
                    "link": link,
                    "sumber": "reuters.com",
                    "published": published,
                    "deskripsi": extract_deskripsi(deskripsi),
                    "penulis": penulis.strip()
                })

        except Exception as e:
            print(f"⚠️ Gagal ambil dari {rss}\nError: {e}\n")

    return berita[:max_berita]

# ✅ Contoh penggunaan
if __name__ == "__main__":
    hasil = ambil_berita_reuters(max_berita=5)
    for b in hasil:
        print(f"[{b['sumber']}] {b['judul']} ({b['published']})")
        print(f"✍️ Penulis: {b['penulis']}")
        print(f"🔗 {b['link']}")
        if b['deskripsi']:
            print(f"📝 Deskripsi: {b['deskripsi'][:200]}...")
        print("=" * 60)
