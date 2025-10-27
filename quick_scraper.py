# File: quick_scraper.py (Versi 6 - Solusi Definitif)

import requests
from bs4 import BeautifulSoup

URL = "https://www.cnnindonesia.com/indeks"
print(f"Mengambil data dari: {URL}\n")

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

try:
    response = requests.get(URL, headers=HEADERS, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    # Langkah 1: Targetkan kontainer utama tempat semua berita asli berada.
    main_content = soup.find('div', class_='w-leftcontent')

    if not main_content:
        print("Gagal menemukan kontainer konten utama. Struktur website mungkin berubah drastis.")
    else:
        # Langkah 2: Di dalam kontainer utama itu, cari semua artikel.
        # Ini akan mengabaikan artikel "palsu" yang ada di header.
        articles = main_content.find_all('article')
        print(f"Berhasil menemukan {len(articles)} artikel asli. Memproses 5 teratas:\n")

        scraped_data = []

        for article in articles[:5]:
            link_element = article.find('a')
            if link_element:
                article_url = link_element.get('href')
                title_element = link_element.find('h2')
                
                if title_element:
                    article_title = title_element.get_text(strip=True)
                    if article_url and article_title:
                        scraped_data.append({
                            "title": article_title,
                            "url": article_url
                        })
        
        # Cetak hasil yang berhasil kita kumpulkan
        if scraped_data:
            for index, item in enumerate(scraped_data, 1):
                print(f"[{index}] Judul: {item['title']}")
                print(f"    URL  : {item['url']}\n")
        else:
            print("Gagal mengekstrak data di dalam kontainer utama.")

except requests.exceptions.RequestException as e:
    print(f"Terjadi kesalahan saat mengakses URL: {e}")