# Proyecto Api Rest en Python - Django

## Versiones de las herramientas

Este proyecto usa las siguientes librerías principales:

- Django 5.2.4
- djangorestframework 3.16.0
- djangorestframework-simplejwt 5.5.0
- psycopg2-binary 2.9.10
- pandas 2.3.0
- matplotlib 3.10.3
- seaborn 0.13.2
- tabulate 0.9.0

## Instalación del Entorno y Configuración del Proyecto
### Requisitos previos
Asegurate de tener instalados:

- Python 3.12 o superior
- PostgreSQL
- Git (opcional)

### Crear y activar entorno virtual
```bash
# Crear entorno virtual
python -m venv venv

# Activar en Windows
.\venv\Scripts\activate
```
### Instalar Django y dependencias
```bash
pip install django djangorestframework psycopg2-binary djangorestframework-simplejwt pandas matplotlib seaborn tabulate
```

Si ya tenés un archivo requirements.txt:

```bash
pip install -r requirements.txt
```

### Crear un nuevo proyecto Django
```bash
django-admin startproject biblioteca
cd biblioteca
```

### Crear la aplicación principal
```bash
python manage.py startapp libros
```
### Configurar base de datos PostgreSQL
Asegurate de tener creada la base de datos desde PostgreSQL. Luego, edita biblioteca/settings.py y reemplazá la sección de DATABASES por:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nombre_de_tu_base',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
### Migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### Ejecutar el servidor
```bash
python manage.py runserver
```
Accedé desde tu navegador a: http://127.0.0.1:8000

## Descripción del programa

Este proyecto es una aplicación web desarrollada con Django que funciona como un sistema de gestión de libros, usuarios, calificaciones y recomendaciones. A través de una API REST construida con Django REST Framework, los usuarios pueden:

Registrarse y autenticarse (con JWT).

Consultar, agregar y calificar libros.

Consultar autores y géneros.

Obtener recomendaciones personalizadas por género.

Generar reportes y gráficos basados en los datos almacenados.

## Estructura del sistema
El sistema se divide en dos aplicaciones principales:

- usuarios/: Módulo para autenticación, registro y login mediante JWT.
- libros/: Módulo principal que gestiona libros, autores, géneros y calificaciones.

Se utilizan los modelos de Django para representar las entidades y relaciones:

- Libro: representa un libro, relacionado con un autor y un género.
- Genero: representa una categoría literaria.
- Autor: representa a un escritor.
- Calificacion: representa una puntuación dada por un usuario a un libro.
- User: el modelo de usuario incorporado de Django.

## ¿Cómo funciona?
### API REST
A través de endpoints definidos con ViewSets y routers, se puede consumir y manipular toda la información. Por ejemplo:

- GET /libros/ para listar libros.
- POST /calificaciones/ para calificar un libro (requiere autenticación).
- POST /register/ para registrar un nuevo usuario.

### Autenticación con JWT
Se utiliza el paquete djangorestframework-simplejwt para la autenticación. Los usuarios reciben un token JWT tras autenticarse en el endpoint /login/.

### Comandos personalizados (scripts internos)
El sistema incluye comandos internos que se ejecutan desde la consola para análisis y visualización de datos:

- python manage.py reporte_libros: genera 10 gráficos diferentes usando pandas, seaborn y matplotlib, que se guardan en una carpeta graficos/.

- python manage.py recomendar_libros --genero=ID: muestra por consola una tabla con los libros mejor calificados para un género específico.

Estos comandos aprovechan el ORM de Django y las bibliotecas de análisis de datos para generar información visual de valor.

## Prueba en Postman

### Registro de usuarios
Url de la api:
```http
POST http://127.0.0.1:8000/register/
```
Se pasan los datos en el body:
```json
{
  "username": "jorgeelizeche",
  "email": "jorge.elizeche.268@alumnos.uninorte.edu.py",
  "password": "1234"
}
```
Respuesta esperada:

<img width="1494" height="406" alt="Image" src="https://github.com/user-attachments/assets/b527a8e1-35dd-494a-8613-8edf4882b03d" />

Codigo para el registro:
```python
class RegistroView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Usuario creado satisfactoriamente."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### Inicio de Sesion
Url de la api:
```http
POST http://127.0.0.1:8000/login/
```
Se pasan las credenciales en el body:
```json
{
  "username": "jorgeelizeche",
  "password": "1234"
}
```
Se genera un jwt token, que nos va a servir para autenticar las demas aplicaciones.

Respuesta esperada:

<img width="1486" height="496" alt="Image" src="https://github.com/user-attachments/assets/b14ff283-b723-4342-a379-81beb79f5f85" />

### Prueba Api Libros
### Listar Todos los libros:
Url de la api:
```http
GET http://127.0.0.1:8000/api/libros/
```
Se pasa el jwt generado en el login para autenticar.

Respuesta esperada:

<img width="1490" height="880" alt="Image" src="https://github.com/user-attachments/assets/0bb2be16-12c9-441c-a399-531d3e76cd83" />

Codigo para listar todos:
```python
def list(self, request):
        libros = self.get_queryset()
        serializer = self.get_serializer(libros, many=True)
        return Response(serializer.data)
```

### Listar libro por id:
Url de la api:
```http
GET http://127.0.0.1:8000/api/libros/22/
```
Se pasa el id del libro que se quiere listar en la url.

Se pasa el jwt generado en el login para autenticar.

Respuesta esperada:

<img width="1494" height="528" alt="Image" src="https://github.com/user-attachments/assets/ff2b3b92-d96e-4f22-b859-667c1cba2f5f" />

Codigo para listar por id:
```python
def retrieve(self, request, pk=None):
        try:
            libro = self.get_object()
            serializer = self.get_serializer(libro)
            return Response(serializer.data)
        except Libro.DoesNotExist:
            return Response({'detail': 'Libro no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

```

### Insertar libro:
Url de la api:
```http
POST http://127.0.0.1:8000/api/libros/
```
Se pasa el jwt generado en el login para autenticar.

Se pasan los datos en el body:
```json
{
    "titulo": "La paloma",
    "autor_id": 23,
    "genero_id": 1,
    "fecha_de_lanzamiento": "1987-01-01",
    "url_del_libro": "https://example.com/paloma"
  }
```

Respuesta esperada:

<img width="1486" height="720" alt="Image" src="https://github.com/user-attachments/assets/32787a62-ab87-4b73-839e-2e84c06be951" />

Codigo para insertar libro:
```python
def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### Actualizar libro:
Url de la api:
```http
PUT http://127.0.0.1:8000/api/libros/51/
```
Se pasa el id del libro que se quiere actualizar en la url.

Se pasa el jwt generado en el login para autenticar.

Se pasan los datos en el body:
```json
{
    "titulo": "El contrabajo",
    "autor_id": 23,
    "genero_id": 1,
    "fecha_de_lanzamiento": "1981-01-01",
    "url_del_libro": "https://example.com/contrabajo"
}
```

Respuesta esperada:

<img width="1490" height="646" alt="Image" src="https://github.com/user-attachments/assets/70783035-2d69-4c1d-869d-10caa95b5e38" />

Codigo para actualizar libro:
```python
def update(self, request, pk=None):
        libro = self.get_object()
        serializer = self.get_serializer(libro, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```


### Eliminar libro:
Url de la api:
```http
DELETE http://127.0.0.1:8000/api/libros/51/
```
Se pasa el id del libro que se quiere eliminar en la url.

Se pasa el jwt generado en el login para autenticar.

Respuesta esperada:

<img width="1484" height="412" alt="Image" src="https://github.com/user-attachments/assets/98fd3370-03bb-43a4-9c66-a16aeae66af0" />

Codigo para eliminar libro:
```python
    def destroy(self, request, pk=None):
        libro = self.get_object()
        libro.delete()
        return Response({'detail': 'Libro eliminado correctamente.'}, status=status.HTTP_204_NO_CONTENT)
```

## Reportes del sistema de biblioteca

El sistema genera 10 reportes gráficos automáticos utilizando datos reales de la base de datos. Los gráficos son creados usando Pandas, Seaborn, Matplotlib, y se guardan en una carpeta llamada graficos/.

Para generar los gráficos, ejecuta el comando:

```bash
python manage.py reporte_libros
```
A continuación, se describen los 10 gráficos generados:

### 📘 1. Cantidad de libros por género
Descripción: Muestra cuántos libros hay en cada género.

Visualización: Gráfico de barras verticales, con etiquetas encima de cada barra.

Archivo generado: 1_libros_por_genero.png

<img width="984" height="584" alt="Image" src="https://github.com/user-attachments/assets/4182d3f8-5e33-48be-bedb-f6e59cdb0861" />


### 🖋️ 2. Top 10 autores con más libros
Descripción: Lista los 10 autores que han publicado más libros en el sistema.

Visualización: Gráfico de barras horizontales ordenado de mayor a menor.

Archivo generado: 2_autores_mas_libros.png

<img width="712" height="485" alt="Image" src="https://github.com/user-attachments/assets/b830e007-8751-4896-a499-5b49d6485ae1" />


### 📚 3. Top 10 libros más calificados
Descripción: Muestra los libros que más calificaciones han recibido.

Visualización: Gráfico de barras horizontales.

Archivo generado: 3_libros_mas_calificados.png

<img width="797" height="485" alt="Image" src="https://github.com/user-attachments/assets/bfd6a739-acbb-4920-99ea-a6331ae7eac2" />

### 🌟 4. Promedio de calificación por género
Descripción: Calcula y muestra el promedio de calificaciones de los libros agrupados por género.

Visualización: Barras con valores flotantes redondeados a 2 decimales encima.

Archivo generado: 4_promedio_genero.png

<img width="984" height="584" alt="Image" src="https://github.com/user-attachments/assets/2c2adb79-23c8-4f5b-b352-40b332ded1c0" />

### 📕 5. Top 10 libros con mejor promedio de calificación
Descripción: Lista los 10 libros con el mayor promedio de calificación.

Visualización: Gráfico de barras horizontales.

Archivo generado: 5_promedio_libro.png

<img width="801" height="485" alt="Image" src="https://github.com/user-attachments/assets/49ac1763-d739-4897-a4cb-5bd6fe2e56df" />

### 👤 6. Promedio de calificación por usuario
Descripción: Muestra el promedio de puntuaciones que cada usuario ha dado.

Visualización: Barras verticales con nombres rotados y valores flotantes.

Archivo generado: 6_promedio_usuario.png

<img width="1384" height="584" alt="Image" src="https://github.com/user-attachments/assets/4f332735-71f1-45aa-9b6a-9848473f0618" />

### 🧑‍💻 7. Top 10 usuarios con más calificaciones
Descripción: Lista los usuarios que más libros han calificado.

Visualización: Gráfico de barras horizontales con etiquetas al final de cada barra.

Archivo generado: 7_usuarios_mas_calificaron.png

<img width="984" height="584" alt="Image" src="https://github.com/user-attachments/assets/7157d335-35b8-4e23-ae57-ff81123bdf6f" />

### 🔥 8. Mapa de calor: usuario vs género
Descripción: Tabla de calor que muestra el promedio de calificaciones que cada usuario ha dado por género.

Visualización: Heatmap con anotaciones numéricas.

Archivo generado: 8_mapa_calor_usuario_genero.png

<img width="1020" height="704" alt="Image" src="https://github.com/user-attachments/assets/4b0c1310-a3e8-47b8-9d1d-c8926d818af4" />

### 🔥 9. Mapa de calor: usuario vs libro
Descripción: Heatmap que cruza usuarios y libros con las calificaciones que han otorgado.

Visualización: Mapa de calor con escala de colores e información flotante.

Archivo generado: 9_heatmap_puntuaciones.png

<img width="1828" height="1484" alt="Image" src="https://github.com/user-attachments/assets/8c3037a3-3723-4778-9fb9-8ed1c33ea107" />

### ⚖️ 10. Comparación entre cantidad y promedio de calificaciones
Descripción: Muestra los 10 libros con más calificaciones, comparando cantidad vs. promedio.

Visualización: Gráfico de dispersión con etiquetas de título en cada punto.

Archivo generado: 10_cantidad_vs_promedio.png

<img width="1184" height="684" alt="Image" src="https://github.com/user-attachments/assets/15a30b0c-bc69-4b61-9a62-3d9bef04af46" />

### 🗂️ Ubicación de los gráficos
Todos los archivos se generan dentro de la carpeta:

```bash
biblioteca/graficos/
```

## Recomendador de libros por género
El sistema incluye un comando personalizado que permite al usuario obtener recomendaciones de libros por género, ordenados por promedio de calificaciones.

### 📌 ¿Qué hace este comando?
Este script lee todos los libros de un género específico (identificado por su ID), calcula el promedio de calificaciones para cada uno y muestra los 10 mejores libros con mayor puntuación promedio.

### 🛠 Cómo ejecutar el comando
Ejecuta el siguiente comando desde la raíz del proyecto:

```bash
python manage.py recomendar_libros --genero=<ID_DEL_GENERO>
```
Por ejemplo, si quieres recomendaciones del género con ID 3:

```bash
python manage.py recomendar_libros --genero=3
```

🔍 ¿Qué muestra?
El resultado se imprime en consola en forma de tabla, utilizando tabulate (si está instalado). La tabla contiene:

<img width="620" height="446" alt="Image" src="https://github.com/user-attachments/assets/74e0f8a7-3ee0-43de-b193-5b92132e53c9" />

### 🧠 ¿Cómo funciona internamente?
- Lee el argumento --genero=N desde consola.
- Verifica si el ID corresponde a un género existente.
- Filtra los libros de ese género con al menos 1 calificación.
- Calcula el promedio de puntuación y cuenta cuántas calificaciones recibió cada libro.
- Ordena por promedio de mayor a menor y muestra los 10 primeros.
- La salida se imprime en consola en formato tabla elegante (fancy_grid) si tabulate está disponible.

### 📦 Requisitos
Este comando utiliza:

pandas para manipular los datos

tabulate (opcional) para mostrar la salida en forma de tabla

Instalación recomendada:

```bash
pip install pandas tabulate
```


## Licencia
Este proyecto está licenciado bajo los términos de la MIT License.

Esto significa que:

- ✅ Puedes usar el código libremente en proyectos personales o comerciales.
- 🔧 Puedes modificar y redistribuir el código.
- 📢 Debes mantener el aviso de copyright y la licencia original.
- ❌ No hay garantía de ningún tipo: el software se ofrece "tal cual".

Licencias de terceros:
```text
 Name                           Version      License
 Django                         5.2.4        BSD License
 PyJWT                          2.9.0        MIT License
 asgiref                        3.9.0        BSD License
 contourpy                      1.3.2        BSD License
 cycler                         0.12.1       BSD License
 djangorestframework            3.16.0       BSD License
 djangorestframework_simplejwt  5.5.0        MIT License
 fonttools                      4.58.5       MIT
 kiwisolver                     1.4.8        BSD License
 matplotlib                     3.10.3       Python Software Foundation License
 numpy                          2.3.1        BSD License
 packaging                      25.0         Apache Software License; BSD License
 pandas                         2.3.0        BSD License
 pillow                         11.3.0       UNKNOWN
 psycopg2-binary                2.9.10       GNU Library or Lesser General Public License (LGPL)
 pyparsing                      3.2.3        MIT License
 python-dateutil                2.9.0.post0  Apache Software License; BSD License
 pytz                           2025.2       MIT License
 seaborn                        0.13.2       BSD License
 six                            1.17.0       MIT License
 sqlparse                       0.5.3        BSD License
 tabulate                       0.9.0        MIT License
 tzdata                         2025.2       Apache Software License
```
