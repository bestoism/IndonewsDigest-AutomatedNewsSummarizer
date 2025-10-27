# File: app.py (Versi Dinamis)

import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from transformers import pipeline

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="IndoNews Summarizer (Live)",
    page_icon="⚡",
    layout="wide"
)

# --- FUNGSI-FUNGSI INTI (Gabungan dari scraper dan summarizer) ---

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM 

@st.cache_data(ttl=600) # Cache data selama 600 detik (10 menit)
def scrape_and_summarize_data(num_articles=10):
    """
    Fungsi utama yang melakukan scraping dan summarization secara live.
    """
    
    # --- BAGIAN 1: SCRAPING 
    st.info(f"Mengambil {num_articles} berita terbaru dari CNN Indonesia. Harap tunggu...")
    
    URL = "https://www.cnnindonesia.com/indeks"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    
    all_articles_data = []
    
    try:
        response = requests.get(URL, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        main_content = soup.find('div', class_='w-leftcontent')
        if not main_content:
            st.error("Gagal menemukan kontainer konten utama di halaman indeks.")
            return None

        articles = main_content.find_all('article')
        
        for article in articles[:num_articles]:
            link_element = article.find('a')
            if link_element:
                article_url = link_element.get('href')
                title_element = link_element.find('h2')
                if title_element and article_url:
                    article_title = title_element.get_text(strip=True)
                    
                    if "/video/" not in article_url:
                        content_response = requests.get(article_url, headers=headers, timeout=10)
                        content_soup = BeautifulSoup(content_response.text, 'html.parser')
                        content_div = content_soup.find('div', class_='detail-text')
                        if content_div:
                            paragraphs = content_div.find_all('p')
                            full_content = "\n".join([p.get_text(strip=True) for p in paragraphs])
                            all_articles_data.append({
                                "title": article_title,
                                "url": article_url,
                                "content": full_content
                            })
                        time.sleep(0.5)

    except Exception as e:
        st.error(f"Terjadi kesalahan saat scraping: {e}")
        return None
    
    if not all_articles_data:
        st.warning("Tidak ada artikel yang berhasil di-scrape.")
        return None

    df_scraped = pd.DataFrame(all_articles_data)

    # --- BAGIAN 2: SUMMARIZATION (Versi Robust/Manual yang Sudah Diperbaiki) ---
    st.info("Berita berhasil diambil. Memulai proses meringkas dengan AI...")
    
    model_name = "cahya/t5-base-indonesian-summarization-cased"
    
    # METODE MANUAL YANG SUDAH TERBUKTI BERHASIL
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)
    except Exception as e:
        st.error(f"Gagal memuat model AI. Error: {e}")
        return df_scraped # Kembalikan data tanpa ringkasan jika model gagal

    summaries = []
    progress_bar = st.progress(0)
    total_articles = len(df_scraped)

    for i, row in df_scraped.iterrows():
        # Model 'cahya' tidak memerlukan prefix "ringkas: ", jadi kita hapus
        text_to_summarize = row['content'] 
        try:
            summary_result = summarizer(
                text_to_summarize, 
                max_new_tokens=80, # Gunakan max_new_tokens untuk hasil terbaik
                min_length=30, 
                num_beams=4,
                do_sample=False
            )
            summaries.append(summary_result[0]['summary_text'])
        except Exception:
            summaries.append("Gagal diringkas.")
        
        progress_bar.progress((i + 1) / total_articles)

    df_scraped['summary'] = summaries
    st.success("Semua berita berhasil diringkas!")
    progress_bar.empty()
    
    return df_scraped


# --- TAMPILAN UTAMA APLIKASI ---

st.title("⚡ IndoNews Summarizer (Live Version)")
st.markdown("Aplikasi ini mengambil berita terbaru **secara langsung** dari CNN Indonesia dan meringkasnya menggunakan AI.")

# Jalankan fungsi utama untuk mendapatkan data
df = scrape_and_summarize_data(num_articles=10)

# Pastikan DataFrame tidak kosong sebelum melanjutkan
if df is not None and not df.empty:
    st.header("Pilih Berita untuk Dilihat Ringkasannya")

    selected_title = st.selectbox(
        label="Pilih judul artikel:",
        options=df['title']
    )

    selected_article = df[df['title'] == selected_title].iloc[0]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Teks Asli Artikel")
        with st.expander("Klik untuk membaca teks asli selengkapnya"):
            st.write(selected_article['content'])
        st.markdown(f"**Sumber:** [{selected_article['url']}]({selected_article['url']})")

    with col2:
        st.subheader("Ringkasan oleh AI")
        st.success(selected_article['summary'])
else:
    st.error("Gagal memuat data berita. Coba refresh halaman setelah beberapa saat.")