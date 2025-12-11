import csv
import os
import sys

csv.field_size_limit(2**31 - 1)

# List your CSV file names here
csv_files = [
    # 'C:/Data/BNMIT/Semester 7/Final Year Project/scraper/new_datasets/arxiv.csv',
    # 'C:/Data/BNMIT/Semester 7/Final Year Project/scraper/new_datasets/clean_science_daily.csv',
    'C:/Data/BNMIT/Semester 7/Final Year Project/scraper/new_datasets/science_daily.csv',
]

total_rows = 0

for filename in csv_files:
    if not os.path.isfile(filename):
        print(f"❌ File not found: {filename}")
        continue

    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        row_count = sum(1 for row in reader) - 1  # subtract header
        print(f"📄 {filename}: {row_count} rows")
        total_rows += row_count

print(f"\n🧮 Total rows across all CSV files: {total_rows}")
