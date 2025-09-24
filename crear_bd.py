import sqlite3

conexion = sqlite3.connect('pelis.db')
cursor = conexion.cursor()

# Creamos la tabla 'peliculas'
cursor.execute('''
    CREATE TABLE IF NOT EXISTS peliculas (
        id INTEGER PRIMARY KEY,
        titulo TEXT NOT NULL,
        sinopsis TEXT
    );
''')

# Creamos la tabla 'reseñas'
cursor.execute('''
    CREATE TABLE IF NOT EXISTS reseñas (
        id INTEGER PRIMARY KEY,
        calificacion INTEGER NOT NULL,
        comentario TEXT,
        pelicula_id INTEGER,
        FOREIGN KEY (pelicula_id) REFERENCES peliculas (id)
    );
''')

# Insertamos algunas películas de ejemplo
peliculas_ejemplo = [
    ('El Rey León', 'Un joven león debe reclamar su reino.'),
    ('Toy Story', 'Un vaquero de juguete se pone celoso de un nuevo juguete espacial.'),
    ('Buscando a Nemo', 'Un pez payaso viaja por el océano para encontrar a su hijo.'),
    ('Shrek', 'Un ogro se embarca en una aventura para salvar a una princesa.'),
]

# Usamos 'executemany' para insertar varias películas a la vez, ¡es más rápido!
cursor.executemany('INSERT INTO peliculas (titulo, sinopsis) VALUES (?, ?)', peliculas_ejemplo)

# Guardamos los cambios y cerramos la conexión
conexion.commit()
conexion.close()

print("¡La base de datos y las tablas se crearon con éxito, y se agregaron películas!")