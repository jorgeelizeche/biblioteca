import psycopg2
import random

# Conexión a la base de datos
conn = psycopg2.connect(
    host="localhost",
    database="biblioteca",
    user="postgres",
    password="123"
)
cur = conn.cursor()
'''cur.execute("DELETE FROM libros_calificacion;")
conn.commit()'''

# Obtener libros y usuarios existentes
cur.execute("SELECT id FROM libros_libro;")
libros = [row[0] for row in cur.fetchall()]

cur.execute("SELECT id FROM auth_user;")
usuarios = [row[0] for row in cur.fetchall()]

if len(usuarios) < 1:
    raise Exception("Debe haber al menos 1 usuario en la base de datos.")

min_calificaciones = 0
max_calificaciones = 8

for libro_id in libros:
    cantidad_calificaciones = random.randint(min_calificaciones, max_calificaciones)
    usuarios_disponibles = usuarios.copy()
    random.shuffle(usuarios_disponibles)
    usuarios_elegidos = usuarios_disponibles[:cantidad_calificaciones]

    for user_id in usuarios_elegidos:
        # Verificar si ya existe la calificación
        cur.execute("""
            SELECT 1 FROM libros_calificacion
            WHERE libro_id = %s AND usuario_id = %s
        """, (libro_id, user_id))

        if cur.fetchone():
            continue  # Ya existe, no insertar

        puntaje = round(random.uniform(1.0, 5.0), 1)

        cur.execute("""
            INSERT INTO libros_calificacion (libro_id, usuario_id, puntuacion)
            VALUES (%s, %s, %s)
        """, (libro_id, user_id, puntaje))

conn.commit()
cur.close()
conn.close()

print("✅ Calificaciones aleatorias insertadas correctamente.")
