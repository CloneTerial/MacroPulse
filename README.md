# MacroPulse

Proyek ini berisi kumpulan script Python untuk melakukan scraping data dari berbagai sumber berita dan data ekonomi, khususnya terkait dengan Bloomberg, Bank Indonesia (BI), IDX, Reuters, Federal Reserve, dan Crypto.

## Fitur Utama

- **Scraping Data Ekonomi BI**: Otomatisasi unduh data inflasi bulanan, suku bunga, dan indikator ekonomi lain dari website Bank Indonesia.
- **Scraping data Federal Reserve**: Mengambil data penting berupa treasury yield, inflasi AS, suku bunga / federal funds rate
- **Scraping Berita Bloomberg, Reuters, IDX, Crypto**: Mengambil berita terbaru dan data pasar dari berbagai sumber finansial.
- **Pengolahan Data Saham**: Mendukung pencarian kode saham, pengelolaan daftar saham, dan pengunduhan data saham IDX.
- **Optimasi Performa**: Blokir resource tidak penting (gambar, font, dsb) saat scraping untuk mempercepat proses.
- **Bypass Deteksi Bot**: Menggunakan Playwright dengan modifikasi user-agent dan properti browser agar tidak terdeteksi sebagai bot.
- **Struktur Folder Modular**: Memisahkan script, data hasil unduhan, dan profil browser untuk kemudahan pengelolaan.

## Struktur Folder

- `scrape/scrape-news/` : Berisi script scraping berita dan data ekonomi.
  - `BI-bulanan.py` : Mengunduh data inflasi bulanan dari website Bank Indonesia secara otomatis menggunakan Playwright.
  - `BI-inflasi.py`, `BI.py` : Script terkait data BI lainnya.
  - `bloomberg-news.py`, `reuters.py`, `crypto.py`, `idx.py`, `fred.py` : Scraper untuk berbagai sumber berita dan data.
  - `downloads/` : Folder hasil unduhan data (misal: Data Inflasi.xlsx).
  - `profile_BI/` : Profil browser untuk scraping BI (cache, cookies, dsb).
- `scrape/scrape-saham/` : Berisi script dan data terkait saham.
  - `bi.py`, `daftar_saham.py`, `data_saham.py`, `search_kode.py` : Script pengolahan data saham.
  - `downloads_idx/` : Folder hasil unduhan data saham.

## Penjelasan Script

- **BI-bulanan.py**: Mengunduh file Excel data inflasi bulanan dari BI secara otomatis. Mendukung blokir resource tidak penting dan bypass deteksi bot.
- **BI-inflasi.py, BI.py**: Scraping data statistik dan indikator ekonomi lain dari BI.
- **bloomberg-news.py**: Mengambil berita terbaru dari Bloomberg.
- **reuters.py**: Scraping berita ekonomi dari Reuters.
- **crypto.py**: Mengambil data dan berita terkait cryptocurrency.
- **idx.py**: Scraping data saham dari IDX.
- **fred.py**: scraping data berupa treasury yield, inflasi as, suku bunga / federal funds rate
- **daftar_saham.py, data_saham.py, search_kode.py**: Pengolahan, pencarian, dan manajemen data saham.

## Cara Menjalankan

1. **Install dependencies**

   Pastikan Python 3.8+ sudah terinstall. Install Playwright dan dependencies lain:

   ```bash
   pip install playwright pandas dotenv
   playwright install
   ```

2. **Jalankan script**

   dapatkan api key [fred](https://fred.stlouisfed.org/docs/api/api_key.html) lalu tempelkan di `.env`

   Contoh menjalankan script untuk mengunduh data inflasi BI:

   ```bash
   python scrape/scrape-news/BI.py
   ```

   File hasil unduhan akan tersimpan di folder `downloads/`.

   Untuk script lain, jalankan dengan cara serupa, misal:

   ```bash
   python scrape/scrape-news/bloomberg-news.py
   python scrape/scrape-saham/data_saham.py
   ```

## 📌 Catatan

- 📎 Contoh file hasil scraping tersedia di folder `downloads/` dan `downloads_idx/` sebagai referensi:

  - `sample_inflasi.xlsx` — contoh hasil scraping data inflasi BI
  - `sample_saham.xlsx` — contoh hasil scraping data saham dari IDX

- Jalankan `BI-bulanan.py` dan `idx.py` secara berkala untuk memperbarui data dengan versi terbaru.
- Script menggunakan Playwright (headless browser) untuk menghindari deteksi bot.
- Beberapa script membutuhkan koneksi internet yang stabil.
- Struktur folder dapat disesuaikan sesuai kebutuhan.
- Untuk mengubah folder hasil unduhan, edit parameter `folder_unduh` di masing-masing fungsi.
- Untuk scraping BI, profil browser disimpan di `profile_BI/` agar sesi login/cookies dapat dipertahankan.

## ✅ To-Do List

- [x] Data BI rate, inflasi bulanan indonesia, cadangan devisa
- [x] Daftar saham IDX
- [x] News crypto RSS
- [x] data fred treasury yield, inflasi AS, suku bunga / federal funds rate
- [x] Struktur folder dan dokumentasi awal
- [ ] Web UI sederhana
- [ ] Logging dan error handling yang lebih baik
