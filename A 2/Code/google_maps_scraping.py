from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import time
from selenium.common.exceptions import StaleElementReferenceException

import pandas as pd

# 1️⃣ Setup WebDriver
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Queries to search


queries = [
    "Cykelmarkedspladser og reparationsværksteder i København",
    "Cykelbutikker i København",
    "Cykeludlejningsbutikker i København",
    "Butikker med cykeltilbehør i København",
    "Elcykelbutikker i København",
    "Cykelbutikker, værksteder, udlejning og tilbehør i København"
]


collected_data = []

for query in queries:
    print(f"🔍 Searching for: {query}")
    driver.get("https://www.google.com/maps")
    wait = WebDriverWait(driver, 10)
    
    search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='searchboxinput']")))
    search_box.clear()
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)  # Allow results to load

    # Function to Extract Business Data
    def scrape_detailed_info():
        """Extracts details from the expanded business panel."""
        time.sleep(2)  # Ensure details are loaded

        try:
            name = driver.find_element(By.CLASS_NAME, "DUwDvf").text.strip()
        except:
            name = "No Name"

        try:
            rating = driver.find_element(By.CLASS_NAME, "F7nice").text.strip()
        except:
            rating = "No Rating"

        try:
            reviews = driver.find_element(By.CLASS_NAME, "UY7F9").text.strip()
        except:
            reviews = "No Reviews"

        try:
            category = driver.find_element(By.CLASS_NAME, "DkEaL").text.strip()
        except:
            category = "No Category"

        try:
            address = driver.find_element(By.CLASS_NAME, "Io6YTe").text.strip()
        except:
            address = "No Address"

        try:
            phone = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Phone')]//div").text.strip()
        except:
            phone = "No Phone"

        
        try:
            website = driver.find_element(By.XPATH, "//a[contains(@aria-label, 'Website')]").get_attribute("href")
        except:
            website = "No Website"
        
        try:
            plus_code = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Plus code')]//div").text.strip()
        except:
            plus_code = "No Plus Code"
        
        try:
            latitude, longitude = driver.current_url.split("@")[1].split("z")[0].split(",")[:2]
        except:
            latitude, longitude = "No Latitude", "No Longitude"
        
        return {
            "name": name, "rating": rating, "reviews": reviews, "category": category,
            "address": address, "phone": phone, "website": website, "plus_code": plus_code,
            "latitude": latitude, "longitude": longitude
        }

    # Scroll & Extract Data Properly
    previous_count = -1
    scroll_attempts = 0
    seen_businesses = set()

    scroll_panel = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "m6QErb")))
    
    while True:
        results = driver.find_elements(By.CLASS_NAME, "Nv2PK")
        
        

        for index in range(len(results)):
            attempts = 0
            while attempts < 3:  # Retry up to 3 times
                try:
                    results = driver.find_elements(By.CLASS_NAME, "Nv2PK")  # Refresh element list
                    result = results[index]

                    business_name = result.text.split("\n")[0]
                    if business_name in seen_businesses:
                        break

                    seen_businesses.add(business_name)
                    driver.execute_script("arguments[0].scrollIntoView();", result)
                    time.sleep(1)

                    result.click()
                    time.sleep(3)

                    business_data = scrape_detailed_info()
                    if business_data["name"] == "No Name":
                        result.click()
                        time.sleep(3)
                        business_data = scrape_detailed_info()

                    if business_data not in collected_data:
                        collected_data.append(business_data)
                        print(f"📌 Scraped {len(collected_data)}: {business_data}")
                    break  # Exit retry loop if successful

                except StaleElementReferenceException:
                    print(f"🔄 Stale element detected at index {index}. Retrying...")
                    attempts += 1  # Retry fetching the element

                except Exception as e:
                    print(f"⚠️ Error at index {index}: {e}")
                    break  # Exit loop if another error occurs

        for _ in range(3):  
            driver.execute_script("arguments[0].scrollBy(0, 300);", scroll_panel)
            time.sleep(2)

        try:
            more_places = driver.find_element(By.XPATH, "//button[contains(text(),'More places')]")
            driver.execute_script("arguments[0].click();", more_places)
            print("🟢 Clicking 'More Places' to load additional results.")
            time.sleep(5)
        except:
            pass

        if len(collected_data) == previous_count:
            scroll_attempts += 1
            if scroll_attempts > 5:
                print("🚫 No more new data available. Stopping scroll.")
                break
        else:
            previous_count = len(collected_data)
            scroll_attempts = 0
        

# 5️⃣ Save Data to CSV
df = pd.DataFrame(collected_data)
df.to_csv("copenhagen_bicycle_shops_extended.csv", index=False, encoding="utf-8")

print(f"✅ Scraping completed. {len(collected_data)} records saved in 'copenhagen_bicycle_shops_extended.csv'")
driver.quit()
