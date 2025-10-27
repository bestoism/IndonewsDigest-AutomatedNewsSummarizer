<img width="1920" height="1857" alt="image" src="https://github.com/user-attachments/assets/2e10baee-a4eb-49e1-8a64-043ec483abee" /># IndoNews Digest: Live Automated News Summarizer

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://bestoism-indonews-summarizer.streamlit.app/)

## 🚀 Live Application

You can access and interact with the live version of the application here:
**[https://bestoism-indonews-summarizer.streamlit.app](https://bestoism-indonews-summarizer.streamlit.app)**


## 📖 Project Overview

IndoNews Digest is a full-stack, real-time data application that automatically scrapes the latest news from a major Indonesian media outlet (CNN Indonesia), processes the text content, and provides concise, AI-generated summaries. This project demonstrates an end-to-end data lifecycle, from live data acquisition and NLP processing to a final, interactive presentation in a web dashboard.

## ✨ Key Features

-   **Real-Time Data Pipeline:** Scrapes the 10 most recent articles directly from the source upon loading, ensuring the data is always up-to-date.
-   **State-of-the-Art NLP Summarization:** Leverages a T5-based Transformer model fine-tuned for Bahasa Indonesia to generate high-quality, abstractive summaries.
-   **Interactive Web Interface:** Built with Streamlit, the UI allows users to easily select an article and view a clean, side-by-side comparison of the original text and its AI-generated summary.
-   **Efficient Performance:** Implements Streamlit's caching (`@st.cache_data`) to store scraped results for 10 minutes, preventing redundant scraping and providing a fast experience for all users within that window.
-   **Robust & Resilient:** Intelligently identifies and skips non-article content (like video pages) to prevent errors and ensure a smooth data processing flow.

## 🛠️ Tech Stack

-   **Data Collection:** Python (`requests`, `BeautifulSoup4`)
-   **NLP / Machine Learning:** Hugging Face `Transformers`, `PyTorch`
-   **Data Manipulation:** `pandas`
-   **Web Framework & Deployment:** `Streamlit`, Streamlit Community Cloud
-   **Environment:** Python 3, `venv`

## 🏗️ System Architecture

The final application operates as a single, cohesive system that executes the following steps in real-time when a user visits the app:

1.  **Trigger:** A user session initiates the main function within the Streamlit application.
2.  **Live Scraping:** The app sends an HTTP request to the news index page, parses the HTML to find the latest article links, and then visits each link to extract the full text content.
3.  **Data Caching:** The results of the scraping and summarization process are cached in memory for 10 minutes. If another user visits within this period, the cached data is served instantly, avoiding repeated requests to the source website.
4.  **AI Summarization:** The extracted text from each article is passed to a pre-trained T5 Transformer model, which generates a concise summary.
5.  **UI Population:** The scraped titles are used to populate a dropdown menu. When a user selects a title, the corresponding original text and its AI-generated summary are displayed in a clean, two-column layout.

## 🌱 Project Evolution: From Scripts to a System

This project was built iteratively, evolving from simple, single-purpose scripts into a fully integrated application. Understanding this journey showcases the development and debugging process.

### 1. Exploration & Experimentation Files

These files were used in the initial stages for discovery, debugging, and proof-of-concept. They are not part of the final application but were critical to its development.

-   **`quick_scraper.py`**: The very first script. Its purpose was purely to test the feasibility of scraping the target website, overcoming initial challenges like `403 Forbidden` errors and finding the correct HTML selectors.
-   **`debug_scraper.py`**: An essential diagnostic tool created when the scraper failed to find content that was visible in a browser. It saved the raw HTML received by the `requests` library, revealing that the initial content was a placeholder, leading to the solution of targeting the main content `div`.
-   **`nlp_summarizer.ipynb`**: The NLP laboratory. This Jupyter Notebook was used to experiment with different summarization models from Hugging Face in an isolated environment. It allowed for rapid testing of models (like BART vs. T5) and fine-tuning of parameters (`num_beams`, `max_length`, etc.) using a static CSV file as input, separating NLP development from data collection.

### 2. Legacy / Bridge Files

These files represent a more mature, but now obsolete, stage of the project.

-   **`main_scraper.py`**: The first production-ready scraper. It evolved from `quick_scraper.py` to fetch full article content and save the structured data into a CSV file.
-   **`scraped_articles.csv`**: A static data file that acted as a bridge between the scraping and NLP stages. It was created by `main_scraper.py` and consumed by `nlp_summarizer.ipynb`. This file is no longer needed in the final dynamic application.

### 3. Final Application Files

These are the only files required to run the live, deployed application.

-   **`app.py`**: The heart and brain of the project. This single file integrates all the successful logic from the experimental scripts. It handles the live scraping, calls the NLP model for summarization, and builds the entire interactive user interface with Streamlit.
-   **`requirements.txt`**: The dependency list. This critical file tells the Streamlit Community Cloud server exactly which Python libraries to install for the application to run correctly.

## ⚙️ How to Run Locally

To run this application on your own machine, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/bestoism/IndonewsDigest-AutomatedNewsSummarizer.git
    cd IndonewsDigest-AutomatedNewsSummarizer
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```
    Your browser should automatically open a new tab with the running application.

## 📸 Application Demo

![Application Screenshot](<img width="1920" height="1857" alt="image" src="https://github.com/user-attachments/assets/f2b2a492-8c4c-4b87-ad49-16797b690918" />
)
