
import json
import os
import re
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with open("prompt.txt", "r", encoding="utf-8") as f:
    base_prompt = f.read()

with open("image_context.json", "r", encoding="utf-8") as f:
    data = json.load(f)

output_clean = []

def extract_json(text):
    try:
        json_text = re.search(r"{.*}", text, re.DOTALL).group(0)
        return json.loads(json_text)
    except:
        raise ValueError("Formato JSON non valido nella risposta")

for entry in data:
    if "image" in entry and "page_text_excerpt" in entry:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": base_prompt + "\n\nTESTO DELLA PAGINA:\n" + entry["page_text_excerpt"]},
                            {"type": "image_url", "image_url": {"url": entry["image"]}}
                        ]
                    }
                ],
                max_tokens=700
            )
            content = response.choices[0].message.content
            try:
                metadata = extract_json(content)
                output_clean.append({
                    "image": entry["image"],
                    "title": metadata.get("Title", ""),
                    "alt_text": metadata.get("Alt Text", ""),
                    "caption": metadata.get("Caption", ""),
                    "description": metadata.get("Description", "")
                })
            except:
                output_clean.append({
                    "image": entry["image"],
                    "error": "Errore nel parsing JSON",
                    "raw_response": content
                })
        except Exception as e:
            output_clean.append({
                "image": entry["image"],
                "error": str(e)
            })

with open("image_metadata.json", "w", encoding="utf-8") as f:
    json.dump(output_clean, f, indent=2, ensure_ascii=False)

print("✅ Metadati generati e salvati in image_metadata.json")
