import sqlite3
from utils.helper import imprimir_error
from config import BD_NAME, table_name

def conectar_db():
    return sqlite3.connect(BD_NAME)

def inicializar_db():
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    descripcion TEXT,
                    cantidad INTEGER NOT NULL,
                    precio REAL NOT NULL,
                    categoria TEXT
                )
            ''')
            conn.commit()
    except sqlite3.Error as e:
        imprimir_error(f"Error al inicializar la base de datos: {e}")

def registrar_producto(nombre, descripcion, cantidad, precio, categoria):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                INSERT INTO {table_name} (nombre, descripcion, cantidad, precio, categoria)
                VALUES (?, ?, ?, ?, ?)
            ''', (nombre, descripcion, cantidad, precio, categoria))
            conn.commit()
        return True
    except sqlite3.Error as e:
        imprimir_error(f"Error al registrar el producto: {e}")
        return False

def obtener_productos():
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute(f'SELECT * FROM {table_name}')
            productos = cursor.fetchall()
        return productos
    except sqlite3.Error as e:
        imprimir_error(f"Error al leer los datos: {e}")
        return []

def buscar_producto_por_id(producto_id):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute(f'SELECT * FROM {table_name} WHERE id = ?', (producto_id,))
            producto = cursor.fetchone()
        return producto
    except sqlite3.Error as e:
        imprimir_error(f"Error al buscar el producto: {e}")
        return None

def buscar_producto_por_texto(texto):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                SELECT * FROM {table_name}
                WHERE nombre LIKE ? OR descripcion LIKE ? OR categoria LIKE ?
            ''', (f'%{texto}%', f'%{texto}%', f'%{texto}%'))
            productos = cursor.fetchall()
        return productos
    except sqlite3.Error as e:
        imprimir_error(f"Error al buscar productos: {e}")
        return []

def actualizar_producto(producto_id, nombre, descripcion, cantidad, precio, categoria):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                UPDATE {table_name}
                SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ?
                WHERE id = ?
            ''', (nombre, descripcion, cantidad, precio, categoria, producto_id))
            conn.commit()
        return True
    except sqlite3.Error as e:
        imprimir_error(f"Error al actualizar el producto: {e}")
        return False

def eliminar_producto(producto_id):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute(f'DELETE FROM {table_name} WHERE id = ?', (producto_id,))
            conn.commit()
        return True
    except sqlite3.Error as e:
        imprimir_error(f"Error al eliminar el producto: {e}")
        return False

def reporte_bajo_stock(limite):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute(f'SELECT * FROM {table_name} WHERE cantidad <= ?', (limite,))
            productos = cursor.fetchall()
        return productos
    except sqlite3.Error as e:
        imprimir_error(f"Error en el reporte de bajo stock: {e}")
        return []