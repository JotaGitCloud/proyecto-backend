from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/explorar')
def explorar():
    return "<h2>Sección Explorar (en construcción)</h2>"

@app.route('/comunidad')
def comunidad():
    return "<h2>Sección Comunidad (en construcción)</h2>"

@app.route('/login')
def login():
    return "<h2>Pantalla de inicio de sesión (en construcción)</h2>"

@app.route('/registrarse')
def registrarse():
    return "<h2>Pantalla de registro (en construcción)</h2>"

if __name__ == '__main__':
    app.run(debug=True)