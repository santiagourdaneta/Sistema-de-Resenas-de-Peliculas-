# En tests/test_app.py
import pytest, sqlite3
from app import app, obtener_pelicula

# La función debe empezar con 'test_'
def test_obtener_pelicula():
    # Suponemos que la película con ID 1 existe en tu base de datos
    pelicula = obtener_pelicula(1)
    # Verificamos que la función devolvió un resultado
    assert pelicula is not None
    # Verificamos que el título de la película es el que esperamos
    assert pelicula[1] == 'El Rey León'

def test_obtener_pelicula_no_existente():
    # Probamos con un ID que no existe
    pelicula = obtener_pelicula(9999)
    # Verificamos que la función devolvió 'None'
    assert pelicula is None

def test_enviar_reseña():
    # Creamos un cliente de prueba
    cliente = app.test_client()

    # Simulamos que alguien envía una reseña a la película con ID 1
    # 'data' es lo que el usuario escribió en el formulario
    respuesta = cliente.post('/review/1', data={
        'calificacion': '5',
        'comentario': '¡Esta es mi película favorita!'
    })

    # Verificamos que la aplicación nos redirigió a la página principal (código 302)
    assert respuesta.status_code == 302

    # Verificamos que la reseña se guardó en la base de datos
    conexion = sqlite3.connect('pelis.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT comentario FROM reseñas WHERE pelicula_id = 1 AND comentario = ?', ('¡Esta es mi película favorita!',))
    reseña_guardada = cursor.fetchone()
    conexion.close()

    # Si la reseña existe en la base de datos, la prueba pasa
    assert reseña_guardada is not None