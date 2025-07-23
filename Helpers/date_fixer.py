import pandas as pd
import re

def convert_date_format(csv_file_path, output_file_path=None):
    """
    Convert date format from YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS+TZ:TZ to Month DD, YYYY format
    Skip dates already in Month DD, YYYY format
    Clean dates with extra time/UTC information
    Using pandas only

    Args:
        csv_file_path (str): Path to input CSV file
        output_file_path (str): Path to output CSV file (optional, defaults to input file)
    """

    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    def format_date(date_str):
        """Convert various date formats to Month DD, YYYY"""
        try:
            # Convert to string and strip whitespace
            date_str = str(date_str).strip()

            # Skip if empty or NaN
            if not date_str or date_str.lower() == 'nan':
                return date_str

            # Handle dates with extra time info like "2 November 2024, at 08:20(UTC)"
            if ', at ' in date_str or '(UTC)' in date_str:
                # Extract just the date part before ", at"
                date_part = date_str.split(', at')[0]
                # Parse and reformat to standard Month DD, YYYY
                date_obj = pd.to_datetime(date_part)
                return date_obj.strftime('%B %d, %Y')

            # Skip if already in Month DD, YYYY format (without extra info)
            if re.match(r'^[A-Za-z]+ \d{1,2}, \d{4}$', date_str):
                return date_str

            # Handle ISO format with timezone (2024-08-20T12:38:45+05:30)
            if 'T' in date_str and ('+' in date_str or date_str.count('-') > 2):
                # Extract just the date part (before 'T')
                date_part = date_str.split('T')[0]
                date_obj = pd.to_datetime(date_part)
                return date_obj.strftime('%B %d, %Y')

            # Handle simple date format (2025-07-19) or ISO without timezone
            else:
                # Use pandas to_datetime which handles multiple formats
                date_obj = pd.to_datetime(date_str)
                return date_obj.strftime('%B %d, %Y')

        except (ValueError, TypeError, pd.errors.ParserError) as e:
            # Return original value if conversion fails
            print(f"Warning: Could not convert date '{date_str}': {e}")
            return date_str

    # Apply the conversion to the date column
    df['date'] = df['date'].apply(format_date)

    # Save to output file (or overwrite input file if no output specified)
    output_path = output_file_path if output_file_path else csv_file_path
    df.to_csv(output_path, index=False)

    print(f"Date conversion completed. File saved as: {output_path}")
    return df

# This script converts date formats in a CSV file from various formats to "Month DD, YYYY"
if __name__ == "__main__":
    csv_file = '../Merged Datasets/improper_clean_merged_15k-20k.csv'

    # Method 1: Apply-based approach (easier to understand)
    convert_date_format(csv_file, '../RAG/Embeddings/clean_merged_15k-20k.csv')
