import requests
import os
import hashlib
from markdownify import markdownify as md

def get_content_hash(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def fetch_and_clean_articles(limit=30):
    url = f"https://support.optisigns.com/api/v2/help_center/en-us/articles.json?page_size={limit}"
    articles_data = []
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get('articles', [])
        
        if not os.path.exists('data'):
            os.makedirs('data')

        for art in articles:
            article_id = str(art.get('id', ''))
            slug = art.get('slug', article_id) 
            html_content = art.get('body') or ""
            html_url = art.get('html_url', "")

            if not article_id: continue 

            footer = f"\n\nArticle URL: {html_url}"
            markdown_text = md(html_content + footer, heading_style="ATX")
            
            articles_data.append({
                "id": article_id,
                "slug": slug,
                "content": markdown_text,
                "hash": get_content_hash(markdown_text),
                "url": html_url
            })
            
        return articles_data
    except Exception as e:
        print(f"Error scraping: {e}")
        return []