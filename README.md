#Proyecto: GAMEVAULT

GameVault es una plataforma web donde los usuarios pueden descubrir, compartir y subir juegos indie. 
Incluye integración con la API de Steam, sistema de usuarios, carga de juegos y navegación dinámica estilo SPA.

## ✨ Características

- Sistema de registro e inicio de sesión
- Exploración de juegos populares desde la API de Steam
- Subida de juegos creados por los usuarios (SQLite)
- Navegación dinámica sin recargar la página (SPA)
- Diseño moderno y responsivo

- ## 📁 Estructura del proyecto (¡Tener en cuenta que, a la hora de descargar los archivos y probar el proyecto via VSCode, los archivos deben estar ubicados en su ruta correspondiente!)
  GameVault/
├── app.py
├── crear_tablas.py
├── database/
│   └── gamevault.db
├── static/
│   ├── estilos.css
│   └── scripts.js
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── registro.html
│   └── explorar.html
└── README.md


## 📦 Requisitos

- Python 3.10+
- Flask
- SQLite3
- Requests

