import requests
import xml.etree.ElementTree as ET
from dotenv import load_dotenv, get_key, find_dotenv
import os

env_path = find_dotenv()
load_dotenv(env_path)
API_KEY = get_key(env_path, "FRED_API_KEY")

def ambil_data_fred(series_id: str, api_key: str, max_data: int = 15):
    data = []
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}"
    print(f"Mengambil data dari: {url}")

    try:
        res = requests.get(url, timeout=15)
        res.raise_for_status()

        root = ET.fromstring(res.content)
        items = root.findall('.//observation')

        for item in items:
            tanggal = item.get('date')
            start = item.get('realtime_start')
            end = item.get('realtime_end')
            nilai = item.get('value')
            nilai_float = None if nilai == "." else float(nilai)

            data.append({
                "tanggal": tanggal,
                "nilai": nilai_float,
                "start": start,
                "end": end
            })

    except requests.exceptions.HTTPError as e:
        print(f"Error HTTP: {e}\nCek kembali series_id dan api_key Anda.")
    except requests.exceptions.RequestException as e:
        print(f"Gagal mengambil data dari FRED API untuk series '{series_id}'.\nError: {e}")
    except ET.ParseError as e:
        print(f"Gagal mem-parsing XML. Respons dari server mungkin bukan XML yang valid.\nError: {e}")
    except Exception as e:
        print(f"Terjadi error yang tidak terduga: {e}")

    return data[:max_data]


if __name__ == "__main__":
    if not API_KEY:
        print("API Key tidak ditemukan. Pastikan file .env berisi FRED_API_KEY=<api_kamu>")
    else:
        daftar_series = {
            "DFF": 15,
            "DGS10": 15,
            "CPIAUCSL": 15
        }

        semua_data = {}

        for series_id, jumlah in daftar_series.items():
            print(f"\nMengambil {jumlah} data untuk series: {series_id}")
            hasil = ambil_data_fred(series_id=series_id, api_key=API_KEY, max_data=jumlah)
            semua_data[series_id] = hasil

        for series_id, data_series in semua_data.items():
            print("-" * 60)
            print(f"{series_id} - Jumlah data: {len(data_series)}")
            for observasi in data_series:
                print(f"Tanggal: {observasi['tanggal']}, Nilai: {observasi['nilai']}, Start: {observasi['start']}, End: {observasi['end']}")
