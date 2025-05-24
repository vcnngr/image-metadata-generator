
import json
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

# Connessione al DB MySQL (WordPress)
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME"),
    charset=os.getenv("DB_CHARSET", "utf8mb4"),
    collation='utf8mb4_general_ci'  # Compatibilità con MySQL 5.7
)

cursor = conn.cursor(dictionary=True)

# Tabelle con prefisso configurabile
prefix = os.getenv("TABLE_PREFIX", "wp_")
posts_table = f"{prefix}posts"
meta_table = f"{prefix}postmeta"

DRY_RUN = False  # True = solo stampa, False = esegue query

# Caricamento dati metadati
with open("image_metadata.json", "r", encoding="utf-8") as f:
    images = json.load(f)

for entry in images:
    image_url = entry["image"]
    title = entry.get("title", "")
    alt_text = entry.get("alt_text", "")
    caption = entry.get("caption", "")
    description = entry.get("description", "")

    # Trova attachment corrispondente
    cursor.execute(f"""
        SELECT ID, post_title, post_excerpt, post_content FROM {posts_table}
        WHERE guid = %s
        AND post_type = 'attachment'
        AND post_mime_type IN ('image/jpeg', 'image/png')
    """, (image_url,))
    post = cursor.fetchone()

    if post:
        post_id = post["ID"]
        print(f"✔️ Trovato attachment ID {post_id} per {image_url}")

        if not DRY_RUN:
            # Aggiorna alt text
            cursor.execute(f"""
                INSERT INTO {meta_table} (post_id, meta_key, meta_value)
                VALUES (%s, '_wp_attachment_image_alt', %s)
                ON DUPLICATE KEY UPDATE meta_value = VALUES(meta_value)
            """, (post_id, alt_text))

            # Aggiorna excerpt e opzionalmente title/content
            cursor.execute(f"""
                UPDATE {posts_table}
                SET post_excerpt = %s
                WHERE ID = %s
            """, (caption, post_id))

            if not post["post_excerpt"] and not post["post_content"]:
                cursor.execute(f"""
                    UPDATE {posts_table}
                    SET post_title = %s, post_content = %s
                    WHERE ID = %s
                """, (title, description, post_id))

            conn.commit()
    else:
        print(f"❌ Nessun attachment trovato per {image_url}")

cursor.close()
conn.close()
print("✅ Aggiornamento completato.")
