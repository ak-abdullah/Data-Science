import pandas as pd


business_file = 'yelp_academic_dataset_business.json'

df = pd.read_json(business_file,lines=True)


relevant_columns = ['business_id', 'name', 'address', 'stars', 'review_count', 'categories', 'latitude', 'longitude']
df = df[relevant_columns]


# Check for missing values in the DataFrame
missing_values = df.isnull().sum()

# Print missing values per column
print("Missing values in dataset:\n", missing_values)
# Count duplicate business IDs
duplicate_count = df.duplicated(subset=['business_id']).sum()

print(f"Number of duplicate business entries: {duplicate_count}")
# Check the data types of each column

# print(df['categories'])

df['categories'] = df['categories'].apply(lambda x: list(set(x.split(', '))) if pd.notnull(x) else [])
# Get unique categories from the dataset
unique_categories = set([cat for sublist in df['categories'] for cat in sublist])


import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="yelp123",  # Replace with your actual password
    database="YelpDB"
)

cursor = conn.cursor()
print("Connected to MySQL successfully!")

# # SQL Insert Query with parameterized values
# insert_query = """
# INSERT INTO Businesses (business_id, name, address, stars, review_count, latitude, longitude)
# VALUES (%s, %s, %s, %s, %s, %s, %s)
# """

# # Insert data securely using parameterized query
# for _, row in df.iterrows():
#     cursor.execute(insert_query, (
#         row['business_id'], row['name'], row['address'], row['stars'],
#         row['review_count'], row['latitude'], row['longitude']
#     ))

# # Commit the transaction
# conn.commit()
# print("✅ Business data inserted successfully using parameterized queries!")





# Insert unique categories using parameterized queries
# insert_category_query = "INSERT INTO Categories (category_name) VALUES (%s) ON DUPLICATE KEY UPDATE category_name=category_name"

# for category in unique_categories:
#     cursor.execute(insert_category_query, (category,))

# conn.commit()
# print("Categories inserted successfully!")





# Fetch the category mappings from the Categories table
cursor.execute("SELECT category_id, category_name FROM Categories")
category_db_mapping = {category_name: category_id for category_id, category_name in cursor.fetchall()}

# Prepare the business-category insert query
business_category_insert_query = "INSERT INTO BusinessCategory (business_id, category_id) VALUES (%s, %s)"

# Prepare a list to store the data for batch insertion
insert_values = []

# Iterate through the dataframe and prepare the data for insertion
for _, row in df.iterrows():
    business_id = row['business_id']
    for category in row['categories']:
        category_id = category_db_mapping.get(category)  # Get the category ID from the mapping
        if category_id:
            insert_values.append((business_id, category_id))  # Append the values to the list

# Insert the data in batches using executemany
if insert_values:
    cursor.executemany(business_category_insert_query, insert_values)
    conn.commit()  # Commit the transaction once all inserts are completed

print(f"Inserted {len(insert_values)} rows into the BusinessCategory table.")
