import pandas as pd
import re

def extract_rating_reviews(value):
    match = re.match(r'([\d\.]+)\s*\((\d+)\)', str(value))  # Match "4.1 (587)"
    if match:
        return float(match.group(1)), int(match.group(2))  # Extract rating and review count
    try:
        return float(value), None  # If only rating is present
    except ValueError:
        return None, None  # If invalid data
    
def clean_text(text):
    if pd.isna(text):  # Check if it's NaN
        return text
    text = re.sub(r'\s+', ' ', text).strip()  # Rem
    return re.sub(r'[^\x00-\x7F]+', '', str(text))  # Remove non-ASCII characters

# Read the first CSV file
df1 = pd.read_csv('danish.csv')

# Read the second CSV file
df2 = pd.read_csv('english.csv')

# Display the first few rows of each DataFrame
merged_df = pd.concat([df1, df2], ignore_index=True)

# Save to a new CSV file
merged_df = merged_df.drop(columns=['reviews'])
duplicate_count = merged_df.duplicated(subset=['phone', 'plus_code', 'name', 'address', 'website', 'category']).sum()
merged_df = merged_df.drop_duplicates(subset=['phone', 'plus_code', 'name', 'address', 'website', 'category'], keep='first')
print(f"Duplicates : {duplicate_count}")
merged_df[['rating', 'review_count']] = merged_df['rating'].apply(lambda x: pd.Series(extract_rating_reviews(x)))
columns_to_clean = ['phone', 'plus_code']  # Add more columns if needed
for col in columns_to_clean:
    merged_df[col] = merged_df[col].apply(clean_text)
merged_df.to_csv('merged.csv', index=False)



