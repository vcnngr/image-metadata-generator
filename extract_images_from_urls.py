
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

with open("urls.txt", "r") as f:
    urls = [line.strip() for line in f if line.strip()]

def extract_images_and_text(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string.strip() if soup.title else "Untitled"
        page_text = ' '.join([p.get_text(strip=True) for p in soup.find_all('p')])
        page_text_excerpt = page_text[:300] + "..." if len(page_text) > 300 else page_text

        images = []
        for img in soup.find_all("img"):
            src = img.get("src")
            if src and (src.endswith(".png") or src.endswith(".jpg") or src.endswith(".jpeg")):
                image_url = urljoin(url, src)
                images.append({
                    "image": image_url,
                    "page_url": url,
                    "page_title": title,
                    "page_text_excerpt": page_text_excerpt
                })
        return images
    except Exception as e:
        return [{"error": str(e), "page_url": url}]

all_data = []
for url in urls:
    all_data.extend(extract_images_and_text(url))

with open("image_context.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, indent=2, ensure_ascii=False)

print("✅ Estrazione completata. File salvato come image_context.json")
