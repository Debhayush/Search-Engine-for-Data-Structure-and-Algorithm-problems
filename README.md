# 🔍 Search Engine for DSA Problems

A lightweight Flask-based search engine that allows users to search Data Structure and Algorithm problems using natural language queries. The engine uses **TF-IDF vectorization** and **cosine similarity** to rank problems based on relevance.

🌐 **Live Demo**: [https://web-production-b2fa2.up.railway.app/](https://web-production-b2fa2.up.railway.app/)

---

## ⚙️ Features

- Full-text search over scraped LeetCode problems.
- Ranks results using TF-IDF + Cosine Similarity.
- View detailed problem statements and URLs.
- Clean UI with Flask + Bootstrap.

---

## 🧠 Technologies Used

- Python, Flask
- HTML, CSS, Bootstrap
- TF-IDF, Cosine Similarity
- Selenium (for scraping)
- Railway (for deployment)

---

## 🚀 How to Run Locally

```bash
git clone https://github.com/Debhayush/Search-Engine-for-Data-Structure-and-Algorithm-problems.git
cd Search-Engine-for-Data-Structure-and-Algorithm-problems
pip install -r requirements.txt
python app.py

📁 Folder Structure
├── app.py
├── requirements.txt
├── templates/
├── data/
│   ├── problems/
│   ├── problemdata/
│   ├── problemtitles.txt
│   ├── problemurls.txt
│   ├── keywords.txt
│   ├── TFIDF.txt
│   ├── IDF.txt
│   └── Magnitude.txt
├── scripts/
│   ├── scrape_links.py
│   ├── scrape_problems.py
│   ├── generate_problemdata.py
│   └── generate_tfidf.py
└── README.md
