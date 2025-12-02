from flask import Flask, render_template, request, redirect, url_for, jsonify, session, send_from_directory
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "gamevault.db")

app = Flask(__name__)
app.secret_key = "gamevault_key_2025"

# ===========================================
#   BASE DE DATOS
# ===========================================
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def ensure_tables():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        email TEXT UNIQUE,
        contrasena TEXT,
        avatar TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS juegos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        publisher TEXT,
        description TEXT,
        image TEXT,
        file TEXT
    );
    """)

    conn.commit()
    conn.close()

ensure_tables()

# ===========================================
#   Inicializar juegos existentes
# ===========================================
def inicializar_juegos_existentes():
    conn = get_db()
    cur = conn.cursor()

    # Lista de juegos existentes (ejemplo con placeholder)
    juegos_existentes = [
        {"name": "Hollow Knight", "description": "Metroidvania épico", "image": "hollow_knight.jpg"},
        {"name": "Counter Strike", "description": "Shooter táctico FPS", "image": "cs.jpg"},
        {"name": "God of War: Ragnarok", "description": "Hack & Slash de acción", "image": "gow_ragnarok.jpg"},
        {"name": "Resident Evil 7", "description": "Survival horror", "image": "re7.jpg"},
        # ... agrega aquí los demás 296 juegos con la misma estructura
    ]

    for juego in juegos_existentes:
        # Evitar duplicados
        cur.execute("SELECT id FROM juegos WHERE name=? AND publisher='existente'", (juego["name"],))
        if cur.fetchone():
            continue
        cur.execute("""
            INSERT INTO juegos (name, publisher, description, image, file)
            VALUES (?, ?, ?, ?, ?)
        """, (juego["name"], "existente", juego.get("description", ""), juego.get("image", ""), ""))

    conn.commit()
    conn.close()

inicializar_juegos_existentes()

# ===========================================
#   RUTAS PRINCIPALES
# ===========================================
@app.route("/")
def inicio():
    if "usuario_id" in session:
        return render_template("index.html", nombre=session["nombre"])
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        contrasena = request.form["contrasena"]

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE email=? AND contrasena=?", (email, contrasena))
        user = cur.fetchone()
        conn.close()

        if user:
            session["usuario_id"] = user["id"]
            session["nombre"] = user["nombre"]
            return redirect(url_for("inicio"))

        return render_template("login.html", error=True)

    return render_template("login.html")

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        contrasena = request.form["contrasena"]

        conn = get_db()
        cur = conn.cursor()

        try:
            cur.execute("INSERT INTO usuarios (nombre, email, contrasena) VALUES (?, ?, ?)",
                        (nombre, email, contrasena))
            conn.commit()
            user_id = cur.lastrowid
        except sqlite3.IntegrityError:
            conn.close()
            return render_template("registro.html", error="Correo ya registrado.")

        conn.close()
        session["usuario_id"] = user_id
        session["nombre"] = nombre
        return redirect(url_for("inicio"))

    return render_template("registro.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ===========================================
#   API: JUEGOS
# ===========================================
@app.route("/api/juegos")
def api_juegos():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM juegos ORDER BY id DESC")
    rows = [dict(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(rows)

@app.route("/api/subir_juego", methods=["POST"])
def subir_juego():
    if "usuario_id" not in session:
        return jsonify({"ok": False, "error": "No autenticado"}), 403

    titulo = request.form.get("titulo")
    descripcion = request.form.get("descripcion")

    if not titulo or not descripcion:
        return jsonify({"ok": False, "error": "Faltan datos"}), 400

    img_file = request.files.get("imagen")
    file_file = request.files.get("archivo")

    carpeta_imgs = os.path.join(BASE_DIR, "static", "uploads", "images")
    carpeta_archivos = os.path.join(BASE_DIR, "static", "uploads", "files")
    os.makedirs(carpeta_imgs, exist_ok=True)
    os.makedirs(carpeta_archivos, exist_ok=True)

    img_name = None
    file_name = None

    if img_file and img_file.filename:
        img_name = img_file.filename
        img_path = os.path.join(carpeta_imgs, img_name)
        img_file.save(img_path)

    if file_file and file_file.filename:
        file_name = file_file.filename
        file_path = os.path.join(carpeta_archivos, file_name)
        file_file.save(file_path)

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO juegos (name, publisher, description, image, file)
        VALUES (?, ?, ?, ?, ?)
    """, (titulo, session["nombre"], descripcion, img_name, file_name))
    conn.commit()
    conn.close()

    return jsonify({"ok": True})

# ===========================================
#   PERFIL API
# ===========================================
@app.route("/api/perfil")
def api_perfil():
    if "usuario_id" not in session:
        return jsonify({"ok": False}), 403

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT nombre, email, avatar FROM usuarios WHERE id=?", (session["usuario_id"],))
    user = cur.fetchone()
    conn.close()

    return jsonify({
        "ok": True,
        "nombre": user["nombre"],
        "email": user["email"],
        "avatar": user["avatar"]
    })

# ===========================================
#   SUBIR AVATAR
# ===========================================
@app.route("/api/subir_avatar", methods=["POST"])
def subir_avatar():
    if "usuario_id" not in session:
        return jsonify({"ok": False}), 403

    if "avatar" not in request.files:
        return jsonify({"ok": False, "error": "No file"}), 400

    archivo = request.files["avatar"]
    if archivo.filename == "":
        return jsonify({"ok": False}), 400

    carpeta = os.path.join(BASE_DIR, "static", "avatars")
    os.makedirs(carpeta, exist_ok=True)

    archivo.save(os.path.join(carpeta, archivo.filename))

    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE usuarios SET avatar=? WHERE id=?", (archivo.filename, session["usuario_id"]))
    conn.commit()
    conn.close()

    return jsonify({"ok": True, "avatar": archivo.filename})

if __name__ == "__main__":
    app.run(debug=True)
