from flask import Flask, render_template, request, redirect, url_for
import sqlite3
# Importamos la nueva biblioteca
from flask_caching import Cache

app = Flask(__name__)

# Crea una instancia de Cache sin inicializarla aún
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
# Ahora, inicialízala con tu aplicación
cache.init_app(app)



app.config['SECRET_KEY'] = '39F6:8E89:4CCC:FAC3:1315:12A5:2153:E9E8'

def obtener_pelicula(pelicula_id):
    conexion = sqlite3.connect('pelis.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT id, titulo, sinopsis FROM peliculas WHERE id = ?', (pelicula_id,))
    pelicula = cursor.fetchone()
    conexion.close()
    return pelicula

def obtener_reseñas(pelicula_id):
    conexion = sqlite3.connect('pelis.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT calificacion, comentario FROM reseñas WHERE pelicula_id = ?', (pelicula_id,))
    reseñas = cursor.fetchall()
    conexion.close()
    return reseñas

# Usamos el decorador del caché para la función 'inicio'
@app.route('/')
@app.route('/pagina/<int:pagina>')
@cache.cached(timeout=300)
def inicio(pagina=1):
    peliculas_por_pagina = 5
    offset = (pagina - 1) * peliculas_por_pagina

    conexion = sqlite3.connect('pelis.db')
    cursor = conexion.cursor()
    cursor.execute(f'SELECT COUNT(*) FROM peliculas')
    total_peliculas = cursor.fetchone()[0]

    cursor.execute(f'SELECT id, titulo, sinopsis FROM peliculas LIMIT {peliculas_por_pagina} OFFSET {offset}')
    peliculas_db = cursor.fetchall()
    conexion.close()

    peliculas_con_reseñas = []
    for peli in peliculas_db:
        pelicula_dicc = {
            'id': peli[0],
            'titulo': peli[1],
            'sinopsis': peli[2],
            'reseñas': obtener_reseñas(peli[0])
        }
        peliculas_con_reseñas.append(pelicula_dicc)
    
    return render_template('index.html', 
                           peliculas=peliculas_con_reseñas, 
                           pagina_actual=pagina,
                           total_paginas=(total_peliculas + peliculas_por_pagina - 1) // peliculas_por_pagina)
@app.route('/buscar')
def buscar():
    query = request.args.get('q', '').strip()
    if not query:
        return redirect(url_for('inicio'))
        
    conexion = sqlite3.connect('pelis.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT id, titulo, sinopsis FROM peliculas WHERE titulo LIKE ?', ('%' + query + '%',))
    peliculas_db = cursor.fetchall()
    conexion.close()
    
    peliculas_con_reseñas = []
    for peli in peliculas_db:
        pelicula_dicc = {
            'id': peli[0],
            'titulo': peli[1],
            'sinopsis': peli[2],
            'reseñas': obtener_reseñas(peli[0])
        }
        peliculas_con_reseñas.append(pelicula_dicc)
    
    return render_template('index.html', peliculas=peliculas_con_reseñas, pagina_actual=1, total_paginas=1)

@app.route('/review/<int:pelicula_id>')
def pagina_reseña(pelicula_id):
    pelicula = obtener_pelicula(pelicula_id)
    if pelicula is None:
        return "Película no encontrada", 404
    
    pelicula_dicc = {'id': pelicula[0], 'titulo': pelicula[1], 'sinopsis': pelicula[2]}
    return render_template('review.html', pelicula=pelicula_dicc)

@app.route('/review/<int:pelicula_id>', methods=['POST'])
def enviar_reseña(pelicula_id):
    calificacion = request.form['calificacion']
    comentario = request.form['comentario']
    
    conexion = sqlite3.connect('pelis.db')
    cursor = conexion.cursor()
    cursor.execute(
        'INSERT INTO reseñas (calificacion, comentario, pelicula_id) VALUES (?, ?, ?)',
        (calificacion, comentario, pelicula_id)
    )
    conexion.commit()
    conexion.close()
    
    # Después de guardar una nueva reseña, debemos borrar el caché para que se vea el cambio.
    cache.clear()
    
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(debug=True)