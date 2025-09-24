# Sistema de Reseñas de Películas

Un sistema de reseñas de películas desarrollado con Python y el framework Flask. Permite a los usuarios ver una lista de películas, dejar sus propias reseñas y calificarlas. El proyecto se enfoca en la **simplicidad**, **usabilidad** y **seguridad**, utilizando tecnologías ligeras para un rendimiento óptimo.

## Características Principales

* **Página Principal:** Muestra una lista de películas con sus reseñas.
* **Reseñas de Usuarios:** Permite a los usuarios calificar y dejar comentarios en las películas.
* **Rendimiento:** Implementa caché para acelerar las consultas a la base de datos.
* **Interfaz de Usuario (UI):** Diseño minimalista y responsivo con **Dark Mode** por defecto.
* **Optimización SEO:** Usa **Server-Side Rendering (SSR)** para una mejor indexación en buscadores.
* **Seguridad:** Incluye protecciones contra inyecciones SQL y XSS.

## Tecnologías Utilizadas

* **Backend:** Python 🐍, Flask
* **Base de Datos:** SQLite
* **Frontend:** Pico.css
* **Pruebas:** Pytest, Selenium

## Cómo Usar

### Instalación

1.  Clona este repositorio:
    ```bash
    git clone [https://github.com/santiagourdaneta/Sistema-de-Resenas-de-Peliculas-](https://github.com/santiagourdaneta/Sistema-de-Resenas-de-Peliculas-)
    cd Sistema-de-Resenas-de-Peliculas-
    ```

2.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

3.  Crea la base de datos:
    ```bash
    python crear_bd.py
    ```

4.  Inicia la aplicación:
    ```bash
    python app.py
    ```

5.  Abre tu navegador y visita `http://127.0.0.1:5000`.

## Contribuciones

Siéntete libre de abrir un issue o enviar un pull request. Todas las contribuciones son bienvenidas.

---