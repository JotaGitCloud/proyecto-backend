from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import sqlite3
import os
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "gamevault.db")

app = Flask(__name__)
app.secret_key = "gamevault_key_2025"

def obtener_juegos_steam():
    try:
        url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
        data = requests.get(url, timeout=5).json()

        # Lista completa de apps de Steam
        apps = data["applist"]["apps"]
        
        juegos = []

        for app in apps[:40]:
            appid = app["appid"]

            # Consultar detalles para obtener imagen, nombre y precio
            detalles_url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=us&l=es"
            resp = requests.get(detalles_url, timeout=5).json()

            if not resp[str(appid)]["success"]:
                continue

            info = resp[str(appid)]["data"]

            if "name" not in info or "header_image" not in info:
                continue

            juegos.append({
                "name": info["name"],
                "header_image": info.get("header_image", ""),
                "price_overview": info.get("price_overview")
            })

            if len(juegos) >= 20:
                break

        return juegos

    except Exception as e:
        print("Error al obtener juegos de Steam:", e)
        return []

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
        nombre TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        contrasena TEXT NOT NULL,
        avatar TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS juegos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        publisher TEXT,
        short_description TEXT,
        price TEXT
    );
    """)

    conn.commit()
    conn.close()

ensure_tables()

# ------------------ API´s ------------------

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
            cur.execute(
                "INSERT INTO usuarios (nombre, email, contrasena) VALUES (?, ?, ?)",
                (nombre, email, contrasena)
            )
            conn.commit()
            user_id = cur.lastrowid
        except sqlite3.IntegrityError:
            conn.close()
            return render_template("registro.html", error="El correo ya está registrado.")

        conn.close()

        session["usuario_id"] = user_id
        session["nombre"] = nombre

        return redirect(url_for("inicio"))

    return render_template("registro.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/api/juegos")
def api_juegos():
    try:
        import requests
        r = requests.get("https://steam-api-dot-steam-api-355303.uc.r.appspot.com/games?", timeout=4)
        if r.ok:
            return jsonify(r.json())
    except:
        pass

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

    data = request.json
    titulo = data.get("titulo")
    descripcion = data.get("descripcion")
    creador = session["nombre"]

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO juegos (name, publisher, short_description, price)
        VALUES (?, ?, ?, ?)
    """, (titulo, creador, descripcion, "Gratis"))
    conn.commit()
    conn.close()

    return jsonify({"ok": True})


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

@app.route("/explorar")
def explorar():
    juegos_steam = obtener_juegos_steam() 
    print(juegos_steam)

    conn = sqlite3.connect("gamevault.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT titulo, descripcion, imagen FROM juegos")
    juegos_usuario = cursor.fetchall()

    conn.close()

    return render_template(
        "explorar.html",
        juegos_steam=juegos_steam,
        juegos_usuario=juegos_usuario,
        nombre=session.get("nombre")
    )


# ------------------ MAIN ------------------
if __name__ == "__main__":
    app.run(debug=True)
