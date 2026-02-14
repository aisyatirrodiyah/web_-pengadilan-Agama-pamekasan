import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_news():
    url = "https://pa-pamekasan.go.id/kategori/berita/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        news_items = []
        # Standard WordPress/PA Pamekasan structure identifiers
        articles = soup.find_all('article')
        
        for article in articles[:6]:  # Limit to 6 news items
            title_tag = article.find('h2', class_='entry-title') or article.find('h3', class_='entry-title')
            if not title_tag:
                continue
            
            title = title_tag.get_text(strip=True)
            link = title_tag.find('a')['href'] if title_tag.find('a') else ""
            
            desc_tag = article.find('div', class_='entry-summary') or article.find('div', class_='entry-content')
            description = desc_tag.get_text(strip=True)[:150] + "..." if desc_tag else ""
            
            img_tag = article.find('img')
            image_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else "assets/news-placeholder.jpg"

            news_items.append({
                "title": title,
                "link": link,
                "description": description,
                "image": image_url
            })

        # Save to JSON
        with open('news_data.json', 'w', encoding='utf-8') as f:
            json.dump(news_items, f, ensure_ascii=False, indent=4)
        
        print(f"Successfully scraped {len(news_items)} news items.")
        return news_items

    except Exception as e:
        print(f"Error during scraping: {e}")
        # Create a fallback/empty file to avoid JS errors
        if not os.path.exists('news_data.json'):
            with open('news_data.json', 'w') as f:
                json.dump([], f)
        return []

if __name__ == "__main__":
    scrape_news()
