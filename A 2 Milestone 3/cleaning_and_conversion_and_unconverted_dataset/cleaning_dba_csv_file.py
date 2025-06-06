import pandas as pd

# Load the CSV
df = pd.read_csv('output.csv')

# Drop multiple columns
df.drop(columns=['Product URL', 'Another Column'], inplace=True)

# Save the updated CSV
df.to_csv('output_cleaned.csv', index=False)
