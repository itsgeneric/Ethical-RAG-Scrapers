import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urlparse
import os

# Step 1: Read URLs from local sitemap file
# Updated to read URLs from a plain text file (one URL per line)
def extract_urls_from_txt(path, limit=10000):
    with open(path, "r", encoding="utf-8") as file:
        urls = [line.strip() for line in file if line.strip()]
        return urls[:limit]

# Get all .txt files from the sciencedaily_txt directory
sciencedaily_txt_dir = r"C:\Data\BNMIT\Semester 7\Final Year Project\scraper\Scrapers\sciencedaily_txt"
txt_files = [f for f in os.listdir(sciencedaily_txt_dir) if f.endswith('.txt')]
txt_files.sort()  # Sort files to process them in order

# Step 2: Scraper logic
HEADERS = {"User-Agent": "Mozilla/5.0"}

def extract_data_from_url(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, "html.parser")

        # Title
        title = soup.find("h1").get_text(strip=True) if soup.find("h1") else None

        # Content
        content_div = soup.find("div", {"id": "text"})
        paragraphs = content_div.find_all("p") if content_div else []
        content = "\n".join(p.get_text(strip=True) for p in paragraphs)

        # Date and Author from <dl>
        date, author = None, None
        dl = soup.find("dl", class_="dl-horizontal dl-custom")
        if dl:
            dt_tags = dl.find_all("dt")
            for dt in dt_tags:
                label = dt.get_text(strip=True)
                dd = dt.find_next_sibling("dd")
                if label == "Date:":
                    date = dd.get_text(strip=True) if dd else None
                elif label == "Source:":
                    author = dd.get_text(strip=True) if dd else None

        domain = urlparse(url).netloc
        categories = "Science"

        return {
            "title": title,
            "content": content,
            "date": date,
            "author": author,
            "url": url,
            "domain": domain,
            "categories": categories,
        }

    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
        return {
            "title": None,
            "content": None,
            "date": None,
            "author": None,
            "url": url,
            "domain": urlparse(url).netloc,
            "categories": "Science",
        }

# Step 3: Process all .txt files
print(f"Found {len(txt_files)} .txt files to process")

for file_idx, txt_file in enumerate(txt_files, 1):
    print(f"\n📁 Processing file {file_idx}/{len(txt_files)}: {txt_file}")

    # Full path to the current txt file
    txt_file_path = os.path.join(sciencedaily_txt_dir, txt_file)

    # Extract URLs from current file
    urls = extract_urls_from_txt(txt_file_path)
    print(f"   Found {len(urls)} URLs in {txt_file}")

    # Extract data from URLs
    data = []
    for url_idx, url in enumerate(urls, start=1):
        print(f"   🔄 Scraping URL {url_idx}/{len(urls)}: {url}")
        result = extract_data_from_url(url)
        data.append(result)

    # Step 4: Save to CSV (separate file for each year)
    year = txt_file.replace("sitemap-releases-", "").replace(".txt", "")
    csv_filename = f"sciencedaily_{year}.csv"

    with open(csv_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "content", "date", "author", "url", "domain", "categories"])
        writer.writeheader()
        writer.writerows(data)

    print(f"   ✅ Data saved to {csv_filename} ({len(data)} articles)")

print("\n🎉 All files processed successfully!")
