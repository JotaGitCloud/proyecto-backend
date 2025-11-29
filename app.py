from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3, os, hashlib

app = Flask(__name__)
app.secret_key = "gamevault_key"
DB_PATH = os.path.join(os.getcwd(), 'database', 'gamevault.db')

def conectar_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def inicio():
    if 'usuario_id' in session:
        # Cuando el usuario ya está logueado, le pasamos su nombre real a base.html
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
            # Guardamos en sesión los datos del usuario
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

if __name__ == '__main__':
    if not os.path.exists('database'):
        os.makedirs('database')
    app.run(debug=True)
