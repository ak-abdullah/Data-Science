import pandas as pd

business_file = 'yelp_academic_dataset_business.json'

business_df = pd.read_json(business_file,lines=True)


print("Business DataFrame:")
print(business_df.head())