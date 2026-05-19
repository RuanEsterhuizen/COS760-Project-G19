#Remember to add citation info

import pandas as pd
import requests
from bs4 import BeautifulSoup

csvRepo = "https://github.com/dsfsi/za-isizulu-siswati-news-2022/raw/refs/heads/main/data/isizulu-titles-all-categories.csv"
#csvRepo = "https://github.com/dsfsi/za-isizulu-siswati-news-2022/raw/refs/heads/main/data/isizulu-titles-reduced-categories.csv"

def urlAvailable(url):
    try:
        print(url)
        response = requests.head(url, allow_redirects=True, timeout=5)
        isAvailable = response.status_code < 400
        return isAvailable
    except requests.RequestException:
        print(f"Error accessing URL: {url} for availability check.")
        return False

def getUrlText(url):
    try:
        #print(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        divs = soup.find_all("div", class_="text_text__oJhZK")
        text = [div.get_text(strip=True) for div in divs]
        #print(text[0])
        return text[0]
    except requests.RequestException:
        print(f"Error fetching URL: {url} for text extraction.")
        return ""

"""def getAvailableUrlText(row):
    url = row['url']"""

#urlText = getUrlText("https://www.isolezwe.co.za/izindaba/kusamile-ukufunda-kwelicija-ngamakhono-14489242")

df = pd.read_csv(csvRepo)
df = df.drop("label", axis=1)
df = df.rename(columns={"title": "source"})

#Replace url with text from source.

#print("Checking URL availability...")
#df = df[df['url'].apply(urlAvailable)]
#print("Extracting text from URLs...")
#df["text"] = df["url"].apply(getUrlText)

#Combine both functions to avoid multiple iterations over the dataframe
print("Checking URL availability and extracting text...")
df["text"] = df.apply(lambda row: getUrlText(row['url']) if urlAvailable(row['url']) else "", axis=1)
df = df[df["text"] != ""] 

df = df.drop("url", axis=1)
df["MGT"] = 0
df.to_csv('isiZuluDataset.csv', index=False)

print(df)

