from utils.helper import (
    imprimir_error,
    imprimir_mensaje,
    validar_input_string,
    validar_input_int,
    validar_input_float,
    imprimir_titulo,
    imprimir_exito,
    imprimir_listado,
)
from utils import db_manager
import sys

def mostrar_tabla_productos(productos):
    if not productos:
        print("no se encontraron productos")
        return
    print(f"{'ID':<5} {'Nombre':<20} {'Descripción':<30} {'Cantidad':<10} {'Precio':<10} {'Categoría':<15}")
    print("-" * 90)
    for prod in productos:
        print(f"{prod[0]:<5} {prod[1]:<20} {prod[2]:<30} {prod[3]:<10} {prod[4]:<10.2f} {prod[5]:<15}")
    print("-" * 90)

def menu_registrar():
    imprimir_titulo("Registrar Nuevo Producto: ")
    nombre = validar_input_string("Ingrese el nombre del producto")
    descripcion = validar_input_string("Ingrese la descripción del producto: ")
    categoria = validar_input_string("Ingrese la categoría del producto: ")
    cantidad = validar_input_int("Ingrese la cantidad del producto: ")
    precio = validar_input_float("Ingrese el precio del producto: ")

    if db_manager.registrar_producto(nombre, descripcion, cantidad, precio, categoria):
        imprimir_exito("Producto registrado exitosamente.")

def menu_mostrar_productos():
    imprimir_listado("Listado de Productos:")
    productos = db_manager.obtener_productos()
    mostrar_tabla_productos(productos)

def menu_actualizar_producto():
    imprimir_titulo("Actualizar Producto:")
    menu_mostrar_productos()
    producto_id = validar_input_int("Ingrese el ID del producto a actualizar")
    producto = db_manager.buscar_producto_por_id(producto_id)
    if not producto:
        imprimir_error("Producto no encontrado.")
        return
    imprimir_mensaje(f"Actualizando producto: {producto[1]}")
    print("dejar vacio el campo que no quiera modificar")
    nuevo_nombre = input(f"Nuevo nombre (actual: {producto[1]}): ").strip() or producto[1]
    nueva_descripcion = input(f"Nueva descripción (actual: {producto[2]}): ").strip() or producto[2]
    nueva_categoria = input(f"Nueva categoría (actual: {producto[5]}): ").strip() or producto[5]
    nueva_cantidad_input = input(f"Nueva cantidad (actual: {producto[3]}): ").strip()
    if nueva_cantidad_input:
        try:
            nueva_cantidad = int(nueva_cantidad_input)
            if nueva_cantidad < 0:
                raise ValueError
        except ValueError:
            imprimir_error("Cantidad inválida. Debe ser un entero positivo.")
            return
    else:
        nueva_cantidad = producto[3]

    nuevo_precio_input = input(f"Nuevo precio (actual: {producto[4]}): ").strip()
    if nuevo_precio_input:
        try:
            nuevo_precio = float(nuevo_precio_input)
            if nuevo_precio < 0:
                raise ValueError
        except ValueError:
            imprimir_error("Precio inválido. Debe ser un número positivo.")
            return
    else:
        nuevo_precio = producto[4]

    if db_manager.actualizar_producto(producto_id, nuevo_nombre, nueva_descripcion, nueva_cantidad, nuevo_precio, nueva_categoria):
        imprimir_exito("Producto actualizado exitosamente.")

def menu_eliminar_producto():
    imprimir_titulo("Eliminar Producto:")
    producto_id = validar_input_int("Ingrese el ID del producto a eliminar")
    producto = db_manager.buscar_producto_por_id(producto_id)
    if not producto:
        imprimir_error("Producto no encontrado.")
        return
    confirmar = input(f"¿Está seguro que desea eliminar el producto '{producto[1]}'? (s/n): ").strip().lower()
    if confirmar == 's':
        if db_manager.eliminar_producto(producto_id):
            imprimir_exito("Producto eliminado exitosamente.")
    else:
        imprimir_mensaje("Operación cancelada por el usuario.")

def menu_buscar():
    imprimir_listado("Buscar Productos:")
    print("1) Buscar por ID")
    print("2) Buscar por texto")
    opcion = input("Seleccione una opción (1/2): ").strip()
    if opcion == '1':
        id_producto = validar_input_int("Ingrese el ID del producto a buscar")
        producto = db_manager.buscar_producto_por_id(id_producto)
        if producto:
            imprimir_listado("Producto encontrado:")
            mostrar_tabla_productos([producto])
        else:
            imprimir_error("Producto no encontrado.")
    elif opcion == '2':
        texto = validar_input_string("Ingrese el texto a buscar")
        productos = db_manager.buscar_producto_por_texto(texto)
        imprimir_listado(f"Resultados de búsqueda para '{texto}':")
        mostrar_tabla_productos(productos)
    else:
        imprimir_error("Opción inválida.")
def menu_reporte_bajo_stock():
    imprimir_titulo("Reporte de Productos con Bajo Stock:")
    limite = validar_input_int("Ingrese el límite de stock")
    productos = db_manager.reporte_bajo_stock(limite)
    imprimir_listado(f"Productos con stock menor o igual a {limite}:")
    mostrar_tabla_productos(productos)

def main():
    while True:
        imprimir_titulo("Sistema de Gestión de Inventario")
        print("1) Registrar Nuevo Producto")
        print("2) Mostrar Todos los Productos")
        print("3) Actualizar Producto")
        print("4) Eliminar Producto")
        print("5) Buscar Producto")
        print("6) Reporte de Bajo Stock")
        print("7) Salir")
        opcion = input("Seleccione una opción (1-7): ").strip()

        if opcion == '1':
            menu_registrar()
        elif opcion == '2':
            menu_mostrar_productos()
        elif opcion == '3':
            menu_actualizar_producto()
        elif opcion == '4':
            menu_eliminar_producto()
        elif opcion == '5':
            menu_buscar()
        elif opcion == '6':
            menu_reporte_bajo_stock()
        elif opcion == '7':
            imprimir_mensaje("Saliendo del sistema. ¡Hasta luego!")
            sys.exit()
        else:
            imprimir_error("Opción inválida. Por favor, seleccione una opción del 1 al 7.")
if __name__ == "__main__":
    main()
