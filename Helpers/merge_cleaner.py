import pandas as pd

# Load CSV
df = pd.read_csv("../Merged Datasets/Fifth_5k.csv")

# Clean up summary and keywords columns for comparison
df['summary_clean'] = df['summary'].fillna('').str.strip().str.lower()
df['keywords_clean'] = df['keywords'].fillna('').str.strip().str.lower()

# Create mask for rows to delete
rows_to_delete = (df['summary_clean'] == "summary not generated.") | (df['keywords_clean'] == "n/a")

# Apply mask to remove those rows
filtered_df = df[~rows_to_delete].copy()

# Drop the helper columns
filtered_df.drop(columns=['summary_clean', 'keywords_clean'], inplace=True)

# Save the cleaned data
filtered_df.to_csv("cleaned_file.csv", index=False)

# Report
print(f"Original rows: {len(df)}")
print(f"Rows after cleaning: {len(filtered_df)}")
print(f"Rows removed: {len(df) - len(filtered_df)}")
