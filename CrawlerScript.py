import feedparser
import requests
from bs4 import BeautifulSoup
import os

# ---------- Step 1: Fetch the top 3 article links ----------
def get_top_articles_from_rss(rss_url, limit=3):
    feed = feedparser.parse(rss_url)
    articles = []
    for entry in feed.entries[:limit]:
        articles.append({
            "title": entry.title,
            "link": entry.link
        })
    return articles

# ---------- Step 2: Extract the main text of each article ----------
def fetch_article_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')

        # First, get all possible paragraphs that may appear in the article
        paragraphs = soup.find_all('p')

        # Filter out empty paragraphs or obvious ads (optional)
        text = '\n'.join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

        return text
    return ""

# ---------- Main Workflow ----------
rss_url = "https://www.artificialintelligence-news.com/categories/agi/feed/"
top_articles = get_top_articles_from_rss(rss_url)

# Save the raw content of each article
all_contents = []

for i, article in enumerate(top_articles, 1):
    print(f"\n{i}. {article['title']}")
    print(f"   Link: {article['link']}")

    content = fetch_article_content(article['link'])
    print(f"   [Text length]: {len(content)} characters")

    formatted_input = f"Please summarize the following article.\n\ntitle: {article['title']}\ntext: {content}\n\nsummary:"

    all_contents.append({
        "title": article['title'],
        "url": article['link'],
        "text": content,
        "model_input": formatted_input
    })
# (Optional) Print out the results temporarily
print("\nFinished extracting text from all articles. Total:", len(all_contents))


#  Ensure the data directory exists (create if it does not exist)
output_dir = os.path.join(os.getcwd(), "data")
os.makedirs(output_dir, exist_ok=True)

#  Save each article input as a .txt file
for i, article in enumerate(all_contents, 1):
    filename = f"article_{i}.txt"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(article["model_input"])
    
    print(f" Saved: {filepath}")
