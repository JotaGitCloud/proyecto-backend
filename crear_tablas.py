#Laverde lctm, me dañaste el código :c, tendré que crear este archivo para crear las tablas de la base de datos de nuevo que me dañaste :c
import sqlite3
import os

# Ruta absoluta de la carpeta del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Carpeta donde estará la base de datos
DB_FOLDER = os.path.join(BASE_DIR, "database")

# Crear carpeta si no existe
if not os.path.exists(DB_FOLDER):
    os.makedirs(DB_FOLDER)

# Ruta del archivo de base de datos
DB_PATH = os.path.join(DB_FOLDER, "gamevault.db")

print("Creando base de datos en:", DB_PATH)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Tabla usuarios
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    contrasena TEXT NOT NULL
);
""")

# Tabla juegos
cursor.execute("""
CREATE TABLE IF NOT EXISTS juegos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descripcion TEXT,
    imagen TEXT,
    usuario_id INTEGER,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
""")

conn.commit()
conn.close()

print("Listo. Base de datos creada correctamente.")
