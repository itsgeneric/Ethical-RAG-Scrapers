# Ethical Web Scrapers & RAG Datasets

This repository contains a collection of Python-based web scrapers designed to ethically harvest textual data for building and training Retrieval-Augmented Generation (RAG) systems. 

Alongside the scraping scripts, this repository provides pre-compiled `.csv` datasets spanning various domains (news, finance, legal, research, and history) ready for immediate use in vector databases or NLP pipelines.

## ⚖️ Ethical Scraping & Compliance
All scrapers in this repository are built with **strict `robots.txt` compliance**. The crawler logic actively parses and respects the target website's rules, crawl delays, and disallowed paths to ensure responsible data collection without overwhelming host servers.

## 📂 Included Datasets
If you just need the data without running the scrapers, the `Datasets/` directory contains the following pre-scraped collections:
* `ap_news_articles.csv`
* `finance.csv`
* `legal_gov.csv`
* `research_papers.csv` (includes arXiv)
* `sciencedaily.csv`
* `tech_docs.csv`
* `tngo_articles.csv`
* `tribunal_docs.csv`
* `wanderingearl.csv`
* `wikipedia_articles_1.csv` & `wikipedia_articles_2.csv`
* `worldhistory.csv`

## 🚀 How to Use

### Using the Datasets
The datasets are provided in standard CSV format. You can load them directly into Pandas or your preferred data processing pipeline:
```python
import pandas as pd
df = pd.read_csv('Datasets/research_papers.csv')
```

### Scrapers
The repository also provides for scrapers using the `BeautifulSoup` Python Library that can be accessed inside the `Scrapers` folder.
Feel free to modify the scrapers to fit any other website or another set of URLs from the same `robots.txt`.


