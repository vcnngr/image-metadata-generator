
# 🧠 Image Metadata Generator (con GPT-4o + WordPress Integration)

Questo progetto ti consente di generare automaticamente **Title**, **Alt Text**, **Caption** e **Description** per le immagini presenti in pagine web, sfruttando le API di **OpenAI GPT-4o**.

Puoi anche **inserire i metadati nel database di WordPress** oppure **generare lo script SQL** per farlo manualmente.

---

## 🚀 Funzionalità principali

✅ Interfaccia web per:
- Inserire gli URL delle pagine da analizzare
- Inserire un prompt personalizzato per la generazione
- Inserire le credenziali del database (facoltative)

✅ Estrazione di immagini e testo HTML dai siti forniti

✅ Generazione di metadati SEO con GPT-4o

✅ Aggiornamento automatico del database WordPress (se configurato)

✅ Esportazione dei dati in:
- `image_context.json`
- `image_metadata.json`
- `insert_metadata.sql` (se DB non configurato)

---

## 🧩 Requisiti

- Python 3.9+
- OpenAI API Key
- Connessione internet
- Accesso al database WordPress (opzionale)

### 📦 requirements.txt

```txt
openai>=1.3.0
python-dotenv
requests
beautifulsoup4
mysql-connector-python
```

---

## 🧪 Come si usa

### 1. Clona o scarica il progetto

```bash
git clone https://github.com/vcnngr/image-metadata-generator.git
cd image-metadata-generator
```

### 2. Installa le dipendenze

```bash
pip install -r requirements.txt
```

### 3. Avvia l’interfaccia web

```bash
python app.py
```

Vai su `http://localhost:5000` e compila i tre moduli:
- URL da analizzare
- Prompt personalizzato
- (Opzionale) Connessione al database

### 4. Esegui gli script in ordine

```bash
python extract_images_from_urls.py
python generate_image_metadata.py
python update_wordpress_metadata.py  # solo se DB configurato
```

Se non configuri il DB, puoi scaricare `insert_metadata.sql` dalla pagina di successo.

---

## 🗃️ File generati

| File                     | Descrizione                                        |
|--------------------------|----------------------------------------------------|
| `image_context.json`     | Immagini trovate con testo di contesto             |
| `image_metadata.json`    | Metadati generati da GPT                           |
| `insert_metadata.sql`    | Script SQL per aggiornare WordPress manualmente    |

---

## 🐳 Esecuzione con Docker

```bash
docker build -t image-metadata-generator .
docker run -p 5000:5000 image-metadata-generator
```

---

## 🧩 Struttura del progetto

- `app.py` — UI web per inserimento input
- `extract_images_from_urls.py` — Estrazione immagini + testo
- `generate_image_metadata.py` — Generazione metadati da OpenAI
- `update_wordpress_metadata.py` — Aggiornamento metadati nel DB WordPress
- `Dockerfile` — Ambiente containerizzato
- `requirements.txt` — Dipendenze
- `.env` — Dati sensibili (non incluso in Git)
- `prompt.txt` / `urls.txt` — File generati dalla UI

---

## ℹ️ Note finali

- Il progetto è completamente generico e riutilizzabile su qualsiasi sito.
- Per WordPress, assicurati che il campo `guid` nel DB corrisponda esattamente all’URL dell’immagine.
- Il campo `TABLE_PREFIX` può essere configurato nel `.env` (es: `wp_`).

---

## 🧠 Licenza

MIT — puoi usare, modificare e distribuire liberamente il progetto.
