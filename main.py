import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from scraper import fetch_and_clean_articles
from uploader import sync_to_openai

load_dotenv()

MANIFEST_FILE = "manifest.json"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
VS_ID = os.getenv("VECTOR_STORE_ID")

def load_manifest():
    if os.path.exists(MANIFEST_FILE):
        try:
            with open(MANIFEST_FILE, 'r') as f:
                content = f.read().strip()
                if not content:
                    return {}
                return json.loads(content)
        except (json.JSONDecodeError, Exception) as e:
            print(f"Warning: Manifest file corrupted or empty. Starting fresh. Error: {e}")
            return {}
    return {}

def save_manifest(manifest):
    with open(MANIFEST_FILE, 'w') as f:
        json.dump(manifest, f, indent=4)

def chunk_text(text, chunk_size=1000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def main():
    print("--- Starting OptiBot Sync Job ---")
    old_manifest = load_manifest()
    new_articles = fetch_and_clean_articles(30)
    
    files_to_sync = []
    new_manifest = {}
    
    added = 0
    updated = 0
    skipped = 0
    all_chunks_count = 0

    for art in new_articles:
        chunks = chunk_text(art['content'])
        all_chunks_count += len(chunks)
        art_id = art['id']
        current_hash = art['hash']
        file_path = f"data/{art['slug']}.md"
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(art['content'])

        if art_id not in old_manifest:
            files_to_sync.append(file_path)
            added += 1
        elif old_manifest[art_id] != current_hash:
            files_to_sync.append(file_path)
            updated += 1
        else:
            skipped += 1
            # if os.path.exists(file_path): os.remove(file_path)
            
        new_manifest[art_id] = current_hash

    print(f"Total files: {len(new_articles)}")
    print(f"Total chunks embedded: {all_chunks_count}")

    synced_count = sync_to_openai(client, VS_ID, files_to_sync)
    
    save_manifest(new_manifest)
    
    print(f"--- Job Completed ---")
    print(f"Added: {added} | Updated: {updated} | Skipped: {skipped}")
    print(f"Total files embedded in this run: {synced_count}")

if __name__ == "__main__":
    main()