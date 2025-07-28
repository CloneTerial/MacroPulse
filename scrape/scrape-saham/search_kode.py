from daftar_saham import semua_saham
from data_saham import ambil_data_saham


kode_input = input("Masukkan kode saham: ").strip()
kode = kode_input.upper()
semua = semua_saham()
    
if kode in semua:
    print(f"✅ Kode saham '{kode}' ditemukan di daftar.")
else:
     print(f"❌ Kode saham '{kode}' TIDAK ditemukan di daftar.")
     
ambil_data_saham(kode)

     
