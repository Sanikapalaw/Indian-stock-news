Got it! Here's a **professional, polished README** suitable for GitHub or presentation to stakeholders:

---

# 📈 Indian Stock News Dashboard

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-green)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-Non--Commercial-red)](LICENSE)


---

## 🔹 Project Overview

The **Indian Stock News Dashboard** is an interactive **Streamlit application** that provides curated, real-time news for **Indian stocks**. It fetches the latest articles from **Google News RSS feeds**, filtering out routine earnings/results updates, and delivers actionable insights for investors and analysts.

This tool streamlines financial news monitoring, helping users stay updated with market-moving events.

---

## 🔹 Features

* **Searchable Stock Selection:** Quickly search for any Indian stock by name or ticker.
* **Curated News Feed:** Displays the **top 10 latest articles** while excluding earnings/results news.
* **Interactive Dashboard:** View headlines, summaries, publication dates, and full article links.
* **CSV Export:** Download curated news for offline analysis and record-keeping.
* **Automatic Caching:** Reduces repeated requests with a **10-minute cache**.

---

## 🔹 Technologies Used

* **Python 3.11** – Core programming language
* **Streamlit** – Interactive dashboard and UI
* **Requests & BeautifulSoup** – Web scraping Google News RSS feeds
* **Pandas** – Data handling and CSV export

---

## 🔹 Installation & Setup

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/indian-stock-news-dashboard.git
cd indian-stock-news-dashboard
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Run the Streamlit app:**

```bash
streamlit run app.py
```

---

## 🔹 Usage

1. Open the sidebar and **search for a stock** by name or ticker.
2. Select the stock from the dropdown list.
3. Click **Fetch News** to display the latest curated articles.
4. Scroll through headlines, summaries, publication dates, and links.
5. Optionally, click **📥 Download News CSV** to save the news for offline analysis.

---

## 🔹 Example Workflow

1. Search for `Reliance` in the sidebar.
2. Select `RELIANCE.NS` from the dropdown.
3. Click **Fetch News** to display the latest 10 articles.
4. Review summaries and publication dates.
5. Download CSV for further analysis.

---

## 🔹 Future Enhancements

* **Multi-stock comparison:** View news for multiple stocks simultaneously.
* **Real-time stock price integration:** Combine news with live price charts.
* **Sentiment analysis:** Automatically classify articles as positive, negative, or neutral.
* **Notification system:** Alert users for critical news events.

---

## 🔹 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

✅ **Professional Notes:**

* No screenshots included—keeps README lightweight and professional.
* Clear sections and structured flow for investors, analysts, or developers.
* Ready to host on GitHub, internal dashboards, or portfolio presentations.

Dashboard link: https://indian-stock-news.streamlit.app/
