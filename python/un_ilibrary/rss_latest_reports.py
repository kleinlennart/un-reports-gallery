from pathlib import Path

import feedparser
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

data_folder = Path("data")

URL = "https://www.un-ilibrary.org/rss/content/all/most_recent_items?fmt=rss"

d = feedparser.parse(URL)

# d["feed"]["title"]
# d["feed"]

entries = d["entries"]

# Convert entries to a pandas DataFrame
df = pd.DataFrame(entries)


df = df[["title", "published", "id", "summary", "link"]]
df


### Get the PDF link / cover


# Function to scrape content, cover image, and PDF link from a given link
def scrape_content(link):
    response = requests.get(link)
    if response.status_code != 200:
        return {
            "cover_image": None,
            "pdf_link": None,
        }
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract cover image
    cover_img = soup.find("img", class_="cover")
    if cover_img and cover_img.get("src"):
        cover_image = cover_img["src"]
        if cover_image.startswith("/"):
            cover_image = "https://www.un-ilibrary.org" + cover_image
    else:
        cover_image = None

    # Extract PDF link
    pdf_form = soup.find("form", class_="ft-download-content__form--pdf")
    if pdf_form and pdf_form.get("action"):
        pdf_link = pdf_form["action"]
        if pdf_link.startswith("/"):
            pdf_link = "https://www.un-ilibrary.org" + pdf_link
    else:
        pdf_link = None

    return {"cover_image": cover_image, "pdf_link": pdf_link}


# Scrape content for each link and add results to separate columns
tqdm.pandas()
results = df["link"].progress_apply(scrape_content)
df["cover_image"] = results.apply(
    lambda x: x["cover_image"] if isinstance(x, dict) else None
)
df["pdf_link"] = results.apply(lambda x: x["pdf_link"] if isinstance(x, dict) else None)


# Export DataFrame to JSON
json_path = data_folder / "output" / "un_ilibrary_latest_reports.json"
df.to_json(json_path, orient="records", force_ascii=False, indent=2)

# Export DataFrame to pickle
pickle_path = data_folder / "output" / "un_ilibrary_latest_reports.pkl"
df.to_pickle(pickle_path)
