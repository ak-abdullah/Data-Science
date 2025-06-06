import pandas as pd
from googletrans import Translator, LANGUAGES

# Load the data
df = pd.read_csv('Original Dataset/google maps.csv', encoding='latin1')

# Initialize Google Translator
translator = Translator()

# Function to translate text to English with error handling
def translate_to_english(text):
    if isinstance(text, str) and text.strip() != "":
        try:
            translation = translator.translate(text, src='da', dest='en')
            return translation.text  # Translate from Danish to English
        except Exception as e:
            print(f"Error translating text: {text} - {e}")
            return text  # Return original text in case of error
    return text  # Return if text is not a string or is empty

# Translate the columns with error handling
df['name'] = df['name'].apply(translate_to_english)
df['address'] = df['address'].apply(translate_to_english)
df['category'] = df['category'].apply(translate_to_english)

# Replace "No Website"/"No Phone" with empty strings
df['website'] = df['website'].replace({'No Website': ''})
df['phone'] = df['phone'].replace({'No Phone': ''})

# Save the translated dataset
df.to_csv('Datasets/google_maps_cleaned_translated.csv', index=False)

# Preview the cleaned and translated data
print(df.head())
