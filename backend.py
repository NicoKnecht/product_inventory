import sqlite3
from datetime import datetime


def crear_base_y_tabla():
    """
    Crea la base de datos 'inventario.db' y la tabla 'productos' si no existen.
    """
    conexion = sqlite3.connect("inventario.db")
    try:
        conexion.execute("BEGIN")
        cursor = conexion.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL,
                categoria TEXT,
                fecha_hora TEXT
            )
        """
        )
        conexion.commit()
    except Exception as e:
        conexion.rollback()
        print(f"Error al crear la base de datos: {e}")
    finally:
        conexion.close()


def agregar_producto():
    """
    Solicita al usuario los datos de un producto, valida cada entrada y lo agrega a la base de datos.
    Registra la fecha y hora de alta del producto.
    """
    while True:
        nombre = input("Ingrese el nombre del producto: ").strip()
        if nombre:
            break
        print("El nombre no puede estar vacío. Intente nuevamente.")

    descripcion = input("Ingrese la descripción del producto: ").strip()

    while True:
        cantidad_input = input("Ingrese la cantidad disponible: ").strip()
        if not cantidad_input:  # si no se ingresa nada
            print("La cantidad no puede estar vacía. Intente nuevamente.")
            continue
        try:
            cantidad = int(cantidad_input)
            if cantidad < 0:
                print("La cantidad no puede ser negativa.")
                continue
            break
        except ValueError:
            print("La cantidad debe ser un número entero. Intente nuevamente.")

    while True:
        precio_input = input("Ingrese el precio del producto: ").strip()
        if not precio_input:
            print("El precio no puede estar vacío. Intente nuevamente.")
            continue
        try:
            precio = float(precio_input)
            if precio < 0:
                print("El precio no puede ser negativo.")
                continue
            break
        except ValueError:
            print("El precio debe ser un número. Intente nuevamente.")

    categoria = input("Ingrese la categoría del producto: ").strip()
    fecha_hora = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )  # fecha y hora actual y formato

    conexion = sqlite3.connect("inventario.db")
    try:
        conexion.execute("BEGIN")
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria, fecha_hora) VALUES (?, ?, ?, ?, ?, ?)",
            (nombre, descripcion, cantidad, precio, categoria, fecha_hora),
        )
        conexion.commit()
        print("Producto agregado exitosamente.")
    except Exception as e:
        conexion.rollback()
        print(f"Error al agregar producto: {e}")
    finally:
        conexion.close()


def obtener_productos():
    """
    Devuelve una lista de todos los productos registrados en la base de datos.
    Cada producto es una tupla con los campos de la tabla.
    """
    conexion = sqlite3.connect("inventario.db")
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT id, nombre, descripcion, cantidad, precio, categoria, fecha_hora FROM productos"
        )
        productos = cursor.fetchall()  # obtiene todos los productos
        return productos
    except Exception as e:
        print(f"Error al consultar productos: {e}")
        return []
    finally:
        conexion.close()


# def imprimir_tabla(productos) es quien imprimira por pantalla en ferontend.py


def actualizar_producto():
    """
    Actualiza los datos de un producto mediante su ID.
    """
    try:
        id_input = input("Ingrese el ID del producto a actualizar: ").strip()
        id_producto = int(id_input)
    except ValueError:
        print("Debe ingresar un ID válido.")
        return

    conexion = sqlite3.connect("inventario.db")
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
        producto = cursor.fetchone()  # se obtiene el producto por su id
        if not producto:
            print("No se encontró un producto con ese ID.")
            return

        print("Deje en blanco para mantener el valor actual.")
        nombre = input(f"Nuevo nombre [{producto[1]}]: ").strip() or producto[1]
        descripcion = (
            input(f"Nueva descripción [{producto[2]}]: ").strip() or producto[2]
        )

        while True:
            cantidad_input = input(f"Nueva cantidad [{producto[3]}]: ").strip()
            if not cantidad_input:
                cantidad = producto[3]
                break
            try:
                cantidad = int(cantidad_input)
                if cantidad < 0:
                    print("La cantidad no puede ser negativa.")
                    continue
                break
            except ValueError:
                print("La cantidad debe ser un número entero.")

        while True:
            precio_input = input(f"Nuevo precio [{producto[4]}]: ").strip()
            if not precio_input:
                precio = producto[4]
                break
            try:
                precio = float(precio_input)
                if precio < 0:
                    print("El precio no puede ser negativo.")
                    continue
                break
            except ValueError:
                print("El precio debe ser un número.")

        categoria = input(f"Nueva categoría [{producto[5]}]: ").strip() or producto[5]

        try:
            conexion.execute("BEGIN")
            cursor.execute(
                """
                UPDATE productos
                SET nombre=?, descripcion=?, cantidad=?, precio=?, categoria=?
                WHERE id=?
            """,
                (nombre, descripcion, cantidad, precio, categoria, id_producto),
            )
            conexion.commit()
            print("Producto actualizado correctamente.")
        except Exception as e:
            conexion.rollback()
            print(f"Error al actualizar producto: {e}")
    except Exception as e:
        print(f"Error al buscar producto: {e}")
    finally:
        conexion.close()


def eliminar_producto():
    """
    Elimina un producto de la base de datos mediante su ID.
    """
    try:
        id_input = input("Ingrese el ID del producto a eliminar: ").strip()
        id_producto = int(id_input)
    except ValueError:
        print("Debe ingresar un ID válido.")
        return

    conexion = sqlite3.connect("inventario.db")
    try:
        conexion.execute("BEGIN")
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
        if cursor.rowcount == 0:
            print("No se encontró un producto con ese ID.")
        else:
            print("Producto eliminado correctamente.")
        conexion.commit()
    except Exception as e:
        conexion.rollback()
        print(f"Error al eliminar producto: {e}")
    finally:
        conexion.close()


def buscar_producto():
    """
    Busca productos por ID o nombre y devuelve una lista de productos encontrados.
    """
    print("Buscar por:")
    print("1. ID")
    print("2. Nombre")
    opcion = input("Seleccione una opción: ").strip()
    conexion = sqlite3.connect("inventario.db")
    try:
        cursor = conexion.cursor()
        if opcion == "1":
            id_input = input("Ingrese el ID del producto: ").strip()
            try:
                id_producto = int(id_input)
            except ValueError:
                print("Debe ingresar un ID válido.")
                return []
            cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
        elif opcion == "2":
            nombre = input("Ingrese el nombre a buscar: ").strip()
            cursor.execute(
                "SELECT * FROM productos WHERE LOWER(nombre) LIKE ?",
                ("%" + nombre.lower() + "%",),
            )
        else:
            print("Opción no válida.")
            return []
        productos = cursor.fetchall()
        return productos
    except Exception as e:
        print(f"Error al buscar producto: {e}")
        return []
    finally:
        conexion.close()


def reporte_bajo_stock():
    """
    Devuelve una lista de productos con cantidad igual o inferior a un límite especificado por el usuario.
    """
    while True:
        limite_input = input("Ingrese el límite de cantidad para el reporte: ").strip()
        try:
            limite = int(limite_input)
            break
        except ValueError:
            print("Debe ingresar un número entero.")

    conexion = sqlite3.connect("inventario.db")
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT id, nombre, descripcion, cantidad, precio, categoria, fecha_hora FROM productos WHERE cantidad <= ?",
            (limite,),
        )
        productos = cursor.fetchall()
        return productos
    except Exception as e:
        print(f"Error al generar el reporte: {e}")
        return []
    finally:
        conexion.close()
