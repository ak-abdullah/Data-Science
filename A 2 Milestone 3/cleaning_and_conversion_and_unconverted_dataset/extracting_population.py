import pandas as pd

# Load the Excel file
df = pd.read_excel('Datasets/population.xlsx')

# Filter rows that contain 'København' in the 'Location' column
filtered_df = df[df['Location'].str.contains("København", na=False)]

# Save the filtered data to an Excel file
filtered_df.to_excel('Datasets/Copenhagen_Population.xlsx', index=False)

# Preview the filtered data
print(filtered_df)
