import pandas as pd
import re

# Load datasets
population_df = pd.read_excel('Datasets/Copenhagen_Population.xlsx')  # Replace with your actual filename
business_df = pd.read_csv('Datasets/google_maps.csv')      # Replace with your actual filename

# --- STEP 1: Extract postal codes ---

# Function to extract the first 4-digit postal code from a string
def extract_postal_code(text):
    match = re.search(r'\b\d{4}\b', str(text))
    return int(match.group()) if match else None

# Extract from population dataset
population_df['postal_code'] = population_df['Location'].apply(extract_postal_code)

# Extract from business dataset
business_df['postal_code'] = business_df['address'].apply(extract_postal_code)

# --- STEP 2: Drop rows with missing postal codes (optional) ---
population_df.dropna(subset=['postal_code'], inplace=True)
business_df.dropna(subset=['postal_code'], inplace=True)

# --- STEP 3: Convert to integer (for consistent merging) ---
population_df['postal_code'] = population_df['postal_code'].astype(int)
business_df['postal_code'] = business_df['postal_code'].astype(int)

# --- STEP 4: Merge on postal_code ---
merged_df = pd.merge(business_df, population_df, on='postal_code', how='left')

# --- STEP 5: Save merged output ---
merged_df.to_csv('merged_business_population_data.csv', index=False)

print("✅ Merge complete. Output saved as 'merged_business_population_data.csv'")
