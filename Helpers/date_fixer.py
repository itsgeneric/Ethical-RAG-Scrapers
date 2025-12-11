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

    # Function to convert date format
    def format_date(date_str):
        """Convert various date formats to Month DD, YYYY"""
        try:
            # Convert to string and strip whitespace
            date_str = str(date_str).strip()

            # Skip if empty or NaN
            if not date_str or date_str.lower() == 'nan':
                return date_str

            # 🔹 Handle patterns like "[Submitted on 15 Feb 2005]"
            # or any text that just contains a "15 Feb 2005" style date
            m = re.search(r'\b\d{1,2}\s+[A-Za-z]{3,}\s+\d{4}\b', date_str)
            if m:
                date_obj = pd.to_datetime(m.group(0))
                return date_obj.strftime('%B %d, %Y')

            # Handle dates with extra time info like "2 November 2024, at 08:20(UTC)"
            if ', at ' in date_str or '(UTC)' in date_str:
                # Extract just the date part before ", at"
                date_part = date_str.split(', at')[0]
                date_obj = pd.to_datetime(date_part)
                return date_obj.strftime('%B %d, %Y')

            # Skip if already in Month DD, YYYY format (without extra info)
            if re.match(r'^[A-Za-z]+ \d{1,2}, \d{4}$', date_str):
                return date_str

            # Handle ISO format with timezone (2024-08-20T12:38:45+05:30)
            if 'T' in date_str and ('+' in date_str or date_str.count('-') > 2):
                date_part = date_str.split('T')[0]
                date_obj = pd.to_datetime(date_part)
                return date_obj.strftime('%B %d, %Y')

            # Fallback: let pandas parse it
            date_obj = pd.to_datetime(date_str)
            return date_obj.strftime('%B %d, %Y')

        except (ValueError, TypeError, pd.errors.ParserError) as e:
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
    csv_file = '../new_datasets/Backup/science_daily.csv'

    # Method 1: Apply-based approach (easier to understand)
    convert_date_format(csv_file, '../NEW Merged Datasets/science_daily.csv')
