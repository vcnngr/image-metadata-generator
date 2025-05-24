
from flask import Flask, request, render_template_string, redirect, send_file
import os
import json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        urls = request.form["urls"]
        prompt = request.form["prompt"]
        db_host = request.form["db_host"]
        db_user = request.form["db_user"]
        db_pass = request.form["db_pass"]
        db_name = request.form["db_name"]

        with open("urls.txt", "w") as f:
            f.write(urls)
        with open("prompt.txt", "w") as f:
            f.write(prompt)
        with open(".env", "w") as f:
            f.write(f"DB_HOST={db_host}\nDB_USER={db_user}\nDB_PASS={db_pass}\nDB_NAME={db_name}")

        return redirect("/success")

    return render_template_string("""
        <h2>Configurazione</h2>
        <form method="post">
            <label>Inserisci gli URL (uno per riga):</label><br>
            <textarea name="urls" rows="5" cols="60"></textarea><br><br>

            <label>Inserisci il prompt da usare per la generazione dei testi:</label><br>
            <textarea name="prompt" rows="10" cols="60"></textarea><br><br>

            <label>DB Host:</label><input type="text" name="db_host"><br>
            <label>DB User:</label><input type="text" name="db_user"><br>
            <label>DB Password:</label><input type="password" name="db_pass"><br>
            <label>DB Name:</label><input type="text" name="db_name"><br><br>

            <input type="submit" value="Salva e Continua">
        </form>
    """)

@app.route("/success")
def success():
    return render_template_string("""
        <h3>Configurazione salvata con successo.</h3>
        <ul>
            <li><a href='/download/image_context'>Scarica image_context.json</a></li>
            <li><a href='/download/image_metadata'>Scarica image_metadata.json</a></li>
            <li><a href='/download/sql_script'>Scarica script SQL</a></li>
        </ul>
    """)

@app.route("/download/image_context")
def download_image_context():
    return send_file("image_context.json", as_attachment=True)

@app.route("/download/image_metadata")
def download_image_metadata():
    return send_file("image_metadata.json", as_attachment=True)

@app.route("/download/sql_script")
def download_sql_script():
    sql_path = "insert_metadata.sql"
    if not os.path.exists(sql_path):
        if os.path.exists("image_metadata.json"):
            with open("image_metadata.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            with open(sql_path, "w", encoding="utf-8") as f_sql:
                for row in data:
                    f_sql.write(f"INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES ({{post_id}}, '_wp_attachment_image_alt', '{row.get("alt_text", "").replace("'", "''")}');\n")
                    f_sql.write(f"INSERT INTO wp_posts (ID, post_excerpt) VALUES ({{post_id}}, '{row.get("caption", "").replace("'", "''")}') ON DUPLICATE KEY UPDATE post_excerpt = VALUES(post_excerpt);\n")
                    f_sql.write(f"-- image: {row.get("image")}\n\n")
    return send_file(sql_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
