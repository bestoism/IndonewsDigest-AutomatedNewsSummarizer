# File: debug_scraper.py (Tugas: Menyimpan HTML mentah)

import requests

URL = "https://www.cnnindonesia.com/indeks"
print(f"Memulai misi investigasi ke: {URL}")

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

try:
    response = requests.get(URL, headers=HEADERS, timeout=10)
    response.raise_for_status()

    # Langkah Kritis: Simpan output mentah ke sebuah file
    # Ini akan menunjukkan apa yang SEBENARNYA dilihat oleh script kita
    with open("debug_output.html", "w", encoding="utf-8") as f:
        f.write(response.text)

    print("\n--- Misi Berhasil! ---")
    print("Sebuah file bernama 'debug_output.html' telah dibuat di folder Anda.")
    print("Langkah selanjutnya: Buka file tersebut dengan text editor (Notepad, VS Code, dll.),")
    print("lalu copy SELURUH isinya dan paste di sini.")

except requests.exceptions.RequestException as e:
    print(f"Terjadi kesalahan saat mengakses URL: {e}")