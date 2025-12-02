import sqlite3

DB_PATH = "database/gamevault.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

juegos_existentes = [
    {"name": "Hollow Knight", "description": "Metroidvania épico", "image": "hollow_knight.jpg"},
    {"name": "Counter Strike", "description": "Shooter táctico FPS", "image": "cs.jpg"},
    {"name": "God of War: Ragnarok", "description": "Hack & Slash de acción", "image": "gow_ragnarok.jpg"},
    {"name": "Resident Evil 7", "description": "Survival horror", "image": "re7.jpg"},
    {"name": "The Witcher 3: Wild Hunt", "description": "RPG de fantasía épica", "image": "witcher3.jpg"},
    {"name": "Cyberpunk 2077", "description": "RPG futurista de mundo abierto", "image": "cyberpunk2077.jpg"},
    {"name": "Minecraft", "description": "Construcción y supervivencia", "image": "minecraft.jpg"},
    {"name": "Among Us", "description": "Juego de deducción social", "image": "among_us.jpg"},
    {"name": "League of Legends", "description": "MOBA competitivo", "image": "lol.jpg"},
    {"name": "Valorant", "description": "Shooter táctico 5v5", "image": "valorant.jpg"},
    {"name": "Fortnite", "description": "Battle Royale creativo", "image": "fortnite.jpg"},
    {"name": "Apex Legends", "description": "Battle Royale con héroes", "image": "apex_legends.jpg"},
    {"name": "Genshin Impact", "description": "RPG de mundo abierto y acción", "image": "genshin.jpg"},
    {"name": "Assassin's Creed Valhalla", "description": "Aventura histórica", "image": "ac_valhalla.jpg"},
    {"name": "Elden Ring", "description": "RPG de fantasía oscura", "image": "elden_ring.jpg"},
    {"name": "Dark Souls III", "description": "RPG de acción desafiante", "image": "dark_souls3.jpg"},
    {"name": "Sekiro: Shadows Die Twice", "description": "Aventura y combate samurái", "image": "sekiro.jpg"},
    {"name": "DOOM Eternal", "description": "Shooter rápido y frenético", "image": "doom_eternal.jpg"},
    {"name": "Resident Evil Village", "description": "Survival horror moderno", "image": "re_village.jpg"},
    {"name": "Fall Guys", "description": "Battle Royale de minijuegos", "image": "fall_guys.jpg"},
    {"name": "Stardew Valley", "description": "Simulación de granja y vida", "image": "stardew.jpg"},
    {"name": "Terraria", "description": "Aventura y construcción 2D", "image": "terraria.jpg"},
    {"name": "Cuphead", "description": "Plataformas y boss fights", "image": "cuphead.jpg"},
    {"name": "Dead by Daylight", "description": "Survival horror multijugador", "image": "dbd.jpg"},
    {"name": "Overwatch", "description": "Shooter de héroes competitivo", "image": "overwatch.jpg"},
    {"name": "The Legend of Zelda: Breath of the Wild", "description": "Aventura y exploración", "image": "zelda_botw.jpg"},
    {"name": "Super Mario Odyssey", "description": "Plataformas 3D icónicas", "image": "mario_odyssey.jpg"},
    {"name": "Mario Kart 8 Deluxe", "description": "Carreras divertidas", "image": "mario_kart.jpg"},
    {"name": "Pokémon Scarlet", "description": "RPG de criaturas", "image": "pokemon_scarlet.jpg"},
    {"name": "Pokémon Violet", "description": "RPG de criaturas", "image": "pokemon_violet.jpg"},
    {"name": "Call of Duty: Modern Warfare II", "description": "Shooter militar", "image": "cod_mw2.jpg"},
    {"name": "Battlefield 2042", "description": "Shooter bélico masivo", "image": "bf2042.jpg"},
    {"name": "FIFA 23", "description": "Simulación de fútbol realista", "image": "fifa23.jpg"},
    {"name": "NBA 2K23", "description": "Simulación de baloncesto", "image": "nba2k23.jpg"},
    {"name": "Rocket League", "description": "Fútbol con autos", "image": "rocket_league.jpg"},
    {"name": "Ghost of Tsushima", "description": "Aventura samurái abierta", "image": "ghost_tsushima.jpg"},
    {"name": "Metal Gear Solid V", "description": "Sigilo y acción", "image": "mgs_v.jpg"},
    {"name": "Persona 5 Royal", "description": "JRPG con historia profunda", "image": "persona5.jpg"},
    {"name": "Final Fantasy VII Remake", "description": "RPG clásico reimaginado", "image": "ff7_remake.jpg"},
    {"name": "Monster Hunter Rise", "description": "Caza de monstruos épica", "image": "mhr.jpg"},
    {"name": "Splatoon 3", "description": "Shooter colorido multijugador", "image": "splatoon3.jpg"},
    {"name": "It Takes Two", "description": "Aventura cooperativa", "image": "it_takes_two.jpg"},
    {"name": "Hades", "description": "Rogue-like de acción", "image": "hades.jpg"},
    {"name": "Celeste", "description": "Plataformas desafiante", "image": "celeste.jpg"},
    {"name": "Dead Cells", "description": "Rogue-like de acción y plataformas", "image": "dead_cells.jpg"},
    {"name": "Valheim", "description": "Supervivencia vikinga", "image": "valheim.jpg"},
    {"name": "Terraria", "description": "Exploración y construcción 2D", "image": "terraria.jpg"},
    {"name": "The Sims 4", "description": "Simulación de vida", "image": "sims4.jpg"},
    {"name": "Brawlhalla", "description": "Plataformas de lucha", "image": "brawlhalla.jpg"},
]

for juego in juegos_existentes:
    cur.execute("SELECT id FROM juegos WHERE name=? AND publisher='existente'", (juego["name"],))
    if cur.fetchone():
        continue
    cur.execute("""
        INSERT INTO juegos (name, publisher, description, image, file)
        VALUES (?, ?, ?, ?, ?)
    """, (juego["name"], "existente", juego.get("description", ""), juego.get("image", ""), ""))

conn.commit()
conn.close()
print("Juegos existentes insertados correctamente.")
