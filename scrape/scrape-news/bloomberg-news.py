import requests
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
import re

NAMESPACES = {
    'media': 'http://search.yahoo.com/mrss/',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'content': 'http://purl.org/rss/1.0/modules/content/',
}

rss_feeds = {
    "bloombergs": [
        "https://feeds.bloomberg.com/economics/news.rss"
    ]
}

def ambil_gambar(item):
    media = item.find('media:content', NAMESPACES)
    if media is not None and 'url' in media.attrib:
        return media.attrib['url']
    return None

def extract_deskripsi(deskripsi):
    return re.sub("<.*?>", "", deskripsi or "").strip()

def ambil_berita_bloomberg(max_berita: int = 10):
    berita = []

    for rss in rss_feeds["bloombergs"]:
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
                image_url = ambil_gambar(item)
                deskripsi_bersih = extract_deskripsi(deskripsi)

                berita.append({
                    "judul": judul.strip(),
                    "link": link,
                    "sumber": "bloomberg.com",
                    "published": published,
                    "image_url": image_url,
                    "deskripsi": deskripsi_bersih,
                })

        except Exception as e:
            print(f"⚠️ Gagal ambil dari {rss}\nError: {e}\n")

    return berita[:max_berita]

if __name__ == "__main__":
    hasil = ambil_berita_bloomberg(max_berita=5)
    for b in hasil:
        print(f"[{b['sumber']}] {b['judul']} ({b['published']})")
        print(f"🔗 {b['link']}")
        if b['image_url']:
            print(f"🖼️ Gambar: {b['image_url']}")
        if b['deskripsi']:
            print(f"📝 Deskripsi: {b['deskripsi'][:150]}...")
        print("=" * 60)
