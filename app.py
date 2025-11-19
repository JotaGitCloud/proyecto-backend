from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response
import sqlite3, os, hashlib, requests
import time

app = Flask(__name__)
app.secret_key = "gamevault_key"
DB_PATH = os.path.join(os.getcwd(), 'database', 'gamevault.db')

CACHE_TTL = 60 * 5  
_cache = {"games": None, "ts": 0}


STEAM_APPIDS = [381210, 367520, 394360, 570, 730]

def conectar_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def inicio():
    if 'usuario_id' in session:
        return render_template('base.html', nombre=session['nombre'])
    return redirect(url_for('login'))

@app.route('/initdb')
def init_db():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        contrasena TEXT NOT NULL,
        avatar TEXT
    );
    ''')
    conn.commit()
    conn.close()
    return '', 204

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        datos = request.form
        conn = conectar_db()
        cursor = conn.cursor()
        hash_pass = hashlib.sha256(datos['contrasena'].encode()).hexdigest()
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, contrasena) VALUES (?, ?, ?)",
            (datos['nombre'], datos['email'], hash_pass)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contrasena = request.form['contrasena']
        hash_pass = hashlib.sha256(contrasena.encode()).hexdigest()

        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email=? AND contrasena=?", (email, hash_pass))
        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            session['usuario_id'] = usuario['id']
            session['nombre'] = usuario['nombre']
            return redirect(url_for('inicio'))
        else:
            return render_template('login.html', error=True)

    return render_template('login.html', error=False)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/juegos_steam')
def juegos_steam():
    import requests, random

    try:
       
        url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
        resp = requests.get(url, timeout=10)

        if resp.status_code != 200:
            return {"error": "Steam no respondió correctamente"}, 500

        data = resp.json()

        juegos = data.get("applist", {}).get("apps", [])
        if not juegos:
            return {"error": "No se encontraron juegos"}, 500

        seleccion = random.sample(juegos, 20)

        juegos_final = []
        for j in seleccion:
            appid = j["appid"]
            nombre = j["name"]

            img_url = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{appid}/header.jpg"

            juegos_final.append({
                "id": appid,
                "nombre": nombre,
                "imagen": img_url
            })

        return {"juegos": juegos_final}, 200

    except Exception as e:
        return {"error": f"Error interno: {str(e)}"}, 500

def fetch_steam_app(appid, lang="spanish"):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}&l={lang}"
    try:
        r = requests.get(url, timeout=6)
        r.raise_for_status()
        data = r.json().get(str(appid), {})
        if data.get("success") and data.get("data"):
            d = data["data"]
            return {
                "id": appid,
                "titulo": d.get("name"),
                "descripcion": d.get("short_description") or d.get("about_the_game") or "",
                "imagen": d.get("header_image") or d.get("screenshots",[{}])[0].get("path_thumbnail"),
                "metacritic": d.get("metacritic", {}).get("score"),
            }
    except Exception:
        return None
    return None

def get_games():
    now = time.time()
    if _cache["games"] and (now - _cache["ts"] < CACHE_TTL):
        return _cache["games"]
    results = []
    for aid in STEAM_APPIDS:
        g = fetch_steam_app(aid)
        if g:
            results.append(g)
    if not results:
       
        results = [
            {"id": 381210, "titulo": "Dead by Daylight", "descripcion": "Horror multijugador 4v1.", "imagen": "https://cdn.cloudflare.steamstatic.com/steam/apps/381210/header.jpg"},
            {"id": 367520, "titulo": "Hollow Knight", "descripcion": "Aventura metroidvania.", "imagen": "https://cdn.cloudflare.steamstatic.com/steam/apps/367520/header.jpg"},
            {"id": 394360, "titulo": "Hearts of Iron IV", "descripcion": "Estrategia militar.", "imagen": "https://cdn.cloudflare.steamstatic.com/steam/apps/394360/header.jpg"},
        ]
    _cache["games"] = results
    _cache["ts"] = now
    return results

@app.route("/")
def index():
    return render_template("base.html")

@app.route("/api/juegos")
def api_juegos():
    juegos = get_games()
    resp = make_response(jsonify(juegos))
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp
