import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urlparse
import os
import time
import re

# Configuration
# Folder containing your .txt files with arXiv URLs
ARXIV_TXT_DIR = "arxiv_txt"
HEADERS = {"User-Agent": "Mozilla/5.0 (Research Project; mailto:your_email@example.com)"}


# Step 1: Read URLs from local text file
def extract_urls_from_txt(path, limit=None):
    with open(path, "r", encoding="utf-8") as file:
        # Filter out empty lines and ensure valid URLs
        urls = [line.strip() for line in file if line.strip().startswith("http")]
        return urls[:limit] if limit else urls


# Get all .txt files from the directory
if not os.path.exists(ARXIV_TXT_DIR):
    os.makedirs(ARXIV_TXT_DIR)
    print(f"⚠️ Created folder '{ARXIV_TXT_DIR}'. Please put your URL text files inside it.")
    exit()

txt_files = [f for f in os.listdir(ARXIV_TXT_DIR) if f.endswith('.txt')]
txt_files.sort()


# Step 2: Scraper logic specific to arXiv.org
def extract_data_from_url(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)

        # specific handling for 404/500 errors
        if r.status_code != 200:
            print(f"⚠️ Status {r.status_code} for {url}")
            return None

        soup = BeautifulSoup(r.content, "html.parser")

        # 1. Title (Strip the "Title:" prefix)
        title_tag = soup.find("h1", class_="title")
        if title_tag:
            # Remove the <span class="descriptor">Title:</span> part
            if title_tag.find("span", class_="descriptor"):
                title_tag.find("span", class_="descriptor").decompose()
            title = title_tag.get_text(strip=True)
        else:
            title = None

        # 2. Abstract/Content (Strip the "Abstract:" prefix)
        abstract_tag = soup.find("blockquote", class_="abstract")
        if abstract_tag:
            if abstract_tag.find("span", class_="descriptor"):
                abstract_tag.find("span", class_="descriptor").decompose()
            content = abstract_tag.get_text(strip=True)
        else:
            content = None

        # 3. Authors (Strip "Authors:" prefix)
        authors_tag = soup.find("div", class_="authors")
        if authors_tag:
            if authors_tag.find("span", class_="descriptor"):
                authors_tag.find("span", class_="descriptor").decompose()
            author = authors_tag.get_text(strip=True)
        else:
            author = None

        # 4. Date (Found in the dateline div)
        # Format usually: "(Submitted on 1 Jan 2024)"
        date_div = soup.find("div", class_="dateline")
        date = date_div.get_text(strip=True) if date_div else None

        # Optional: Clean up date string
        if date:
            date = date.replace("(Submitted on", "").replace(")", "").strip()

        # 5. Categories/Subjects
        # Found in: <td class="tablecell subjects">
        subjects_tag = soup.find("td", class_="tablecell subjects")
        categories = subjects_tag.get_text(strip=True) if subjects_tag else "General"

        domain = urlparse(url).netloc

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
            "categories": "Unknown",
        }


# Step 3: Process all .txt files
print(f"🚀 Found {len(txt_files)} .txt files to process")

for file_idx, txt_file in enumerate(txt_files, 1):
    print(f"\n📁 Processing file {file_idx}/{len(txt_files)}: {txt_file}")

    txt_file_path = os.path.join(ARXIV_TXT_DIR, txt_file)

    # Extract URLs
    urls = extract_urls_from_txt(txt_file_path)
    print(f"   Found {len(urls)} URLs in {txt_file}")

    data = []

    # Process URLs
    for url_idx, url in enumerate(urls, start=1):
        print(f"   🔄 Scraping URL {url_idx}/{len(urls)}: {url}")

        result = extract_data_from_url(url)

        if result:
            data.append(result)

        # CRITICAL: arXiv requires delays. Do not remove this sleep.
        # Sleeping 3 seconds is safe.
        time.sleep(3)

    # Step 4: Save to CSV
    # Create output filename based on input txt name
    csv_filename = txt_file.replace(".txt", ".csv")

    # Ensure we don't overwrite if it exists, or maybe we want to?
    # Current logic overwrites.

    try:
        with open(csv_filename, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["title", "content", "date", "author", "url", "domain", "categories"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        print(f"   ✅ Data saved to {csv_filename} ({len(data)} papers)")

    except Exception as e:
        print(f"   ❌ Error saving CSV: {e}")

print("\n🎉 All files processed successfully!")