import requests
from bs4 import BeautifulSoup
import time
import pandas as pd 

# Fungsi get_article_content 
def get_article_content(url):
    print(f"  -> Mengunjungi artikel: {url}")
    try:
        if "/video/" in url:
            print("     -> Halaman video terdeteksi. Konten teks tidak relevan. Melewati...")
            return None

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        content_div = soup.find('div', class_='detail-text')

        if not content_div:
            print("     Gagal menemukan div konten utama (kemungkinan bukan artikel teks standar).")
            return None

        paragraphs = content_div.find_all('p')
        full_content = "\n".join([p.get_text(strip=True) for p in paragraphs])
        return full_content
    except requests.exceptions.RequestException as e:
        print(f"     Error saat mengakses artikel: {e}")
        return None
    except Exception as e:
        print(f"     Terjadi error tak terduga: {e}")
        return None

def scrape_index_page():
    URL = "https://www.cnnindonesia.com/indeks"
    print(f"Memulai scraping dari halaman utama: {URL}\n")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(URL, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        main_content = soup.find('div', class_='w-leftcontent')
        if not main_content:
            print("Gagal menemukan kontainer konten utama.")
            return

        articles = main_content.find_all('article')
        print(f"Berhasil menemukan {len(articles)} tautan artikel. Memproses 5 teratas:\n")
        all_articles_data = []
        skipped_articles = 0
        for index, article in enumerate(articles[:5], 1):
            link_element = article.find('a')
            if link_element:
                article_url = link_element.get('href')
                title_element = link_element.find('h2')
                if title_element and article_url:
                    article_title = title_element.get_text(strip=True)
                    print(f"[{index}] Memproses: {article_title}")
                    content = get_article_content(article_url)
                    if content:
                        all_articles_data.append({
                            "title": article_title,
                            "url": article_url,
                            "content": content
                        })
                        print("     -> Sukses. Konten berhasil diekstrak.\n")
                    else:
                        skipped_articles += 1
                        print("     -> Gagal atau dilewati. Artikel tidak diproses.\n")
                    time.sleep(1)

        print("--- Scraping Selesai ---")
        print(f"Total artikel berhasil diproses: {len(all_articles_data)}")
        print(f"Total artikel dilewati (video/format lain): {skipped_articles}\n")
        
        # <<<--- 2. LOGIKA BARU UNTUK MENYIMPAN DATA --->>>
        if all_articles_data:
            print("Menyimpan data ke file CSV...")
            # Ubah list of dictionaries menjadi DataFrame Pandas
            df = pd.DataFrame(all_articles_data)
            
            # Simpan DataFrame ke file CSV
            # index=False agar tidak ada kolom nomor baris tambahan di file
            df.to_csv('scraped_articles.csv', index=False, encoding='utf-8')
            
            print("Berhasil! Data telah disimpan di file 'scraped_articles.csv'")
        else:
            print("Tidak ada data untuk disimpan.")

    except requests.exceptions.RequestException as e:
        print(f"Terjadi kesalahan saat mengakses URL Indeks: {e}")

if __name__ == "__main__":
    scrape_index_page()