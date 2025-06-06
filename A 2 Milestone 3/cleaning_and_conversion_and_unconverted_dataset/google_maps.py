import pandas as pd

# Load the CSV file
df = pd.read_csv('Datasets/google_maps.csv')  # Make sure this CSV is in the same folder as your script

# Display the first 5 rows
print("First 5 rows of the dataset:")
print(df.head())

# Display general info: column names, data types, and non-null counts
print("\nDataset Information:")
print(df.info())

# Fill missing rating and review_count with median values
df['rating'] = df['rating'].fillna(df['rating'].median())
df['review_count'] = df['review_count'].fillna(df['review_count'].median())


print("Missing values per column:")
print(df.isnull().sum())

# Check percentage of missing values
print("\nPercentage of missing values:")
print((df.isnull().sum() / len(df)) * 100)
# Save the cleaned data to a new CSV file
df.to_csv('Datasets/google_maps.csv', index=False)

print("Cleaned data saved as 'google_maps_cleaned.csv'")

