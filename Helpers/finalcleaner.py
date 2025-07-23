import pandas as pd
import re

def clean_and_standardize_for_mongo(csv_file_path, output_file_path=None):
    """
    Convert various date formats to 'YYYY-MM-DD' (Mongo-compatible).
    Fix corrupted rows with known date. Ensure 'title' is string.
    
    Args:
        csv_file_path (str): Input CSV path
        output_file_path (str): Output CSV path (optional)
    """
    df = pd.read_csv(csv_file_path)

    def normalize_date(date_str):
        """Convert to YYYY-MM-DD string"""
        try:
            date_str = str(date_str).strip()

            if not date_str or date_str.lower() == 'nan':
                return None

            # Handle "9 August 2024, at 03:04(UTC)." → extract just the date
            if ', at ' in date_str and '(UTC)' in date_str:
                date_part = date_str.split(', at')[0]
                return pd.to_datetime(date_part).strftime('%Y-%m-%d')

            # Format: "January 29, 2024"
            if re.match(r'^[A-Za-z]+ \d{1,2}, \d{4}$', date_str):
                return pd.to_datetime(date_str).strftime('%Y-%m-%d')

            # Format: "2024-07-19"
            if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
                return date_str

            # Weird edge case - not a date at all
            if "seconds" in date_str.lower():
                return None

            # Try fallback parsing
            return pd.to_datetime(date_str).strftime('%Y-%m-%d')

        except Exception as e:
            print(f"Warning: Failed to convert date '{date_str}': {e}")
            return None


    def to_str(val):
        """Ensure string type"""
        try:
            return str(val) if pd.notna(val) else ""
        except:
            return ""

    # Clean date column
    if 'date' in df.columns:
        df.loc[25723:26066, 'date'] = '2025-07-18'
        df['date'] = df['date'].apply(normalize_date)

        # Fix corrupt rows: 25724 to 26065 → "2025-07-18"

    # Clean title column
    if 'title' in df.columns:
        df['title'] = df['title'].apply(to_str)

    # Output file
    output_path = output_file_path if output_file_path else csv_file_path
    df.to_csv(output_path, index=False)

    print(f"Cleaned CSV saved to: {output_path}")
    return df

# Run this block to execute
if __name__ == "__main__":
    input_csv = "../RAG/Embeddings/final_embeddings_merged.csv"
    output_csv = "../Merged Datasets/final_embeddings.csv"
    clean_and_standardize_for_mongo(input_csv, output_csv)
