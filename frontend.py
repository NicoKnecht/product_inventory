import os
from colorama import Fore, Back, Style, init
from backend import *

init(autoreset=True)  # Inicializa colorama


def limpiar_pantalla():
    """
    Limpia la pantalla de la terminal según el sistema operativo.
    """
    os.system("cls" if os.name == "nt" else "clear")


def pausa():
    """
    Pausa la ejecución hasta que el usuario presione una tecla.
    """
    os.system(
        "pause"
        if os.name == "nt"
        else 'read -e -n 1 -p "Presione una tecla para continuar..."'
    )
    return None


def imprimir_titulo(texto):
    """
    Imprime un título destacado.
    """
    print(Fore.GREEN + Style.BRIGHT + f"\n{texto}" + Style.RESET_ALL)


def imprimir_tabla(productos):
    """
    Imprime los productos en formato de tabla simple y clara.
    Cada producto es una tupla con los campos de la base de datos.
    """
    if not productos:
        print("No hay productos registrados.")
        return

    # Encabezados de la tabla
    print(
        "{:<4} | {:<15} | {:<20} | {:<8} | {:<10} | {:<12} | {}".format(
            "ID",
            "Nombre",
            "Descripción",
            "Cantidad",
            "Precio",
            "Categoría",
            "Fecha y hora",
        )
    )
    print("-" * 100)

    # Imprime cada producto con formato fijo
    for p in productos:
        print(
            "{:<4} | {:<15} | {:<20} | {:<8} | {:<10} | {:<12} | {}".format(
                p[0], str(p[1])[:15], str(p[2])[:20], p[3], p[4], str(p[5])[:12], p[6]
            )
        )


def mostrar_menu():
    """
    Muestra el menú de opciones disponibles para el usuario.
    """
    imprimir_titulo("Menú de opciones")
    print(Fore.CYAN + "1. Agregar producto" + Style.RESET_ALL)
    print(Fore.CYAN + "2. Visualizar productos" + Style.RESET_ALL)
    print(Fore.CYAN + "3. Actualizar producto" + Style.RESET_ALL)
    print(Fore.CYAN + "4. Eliminar producto" + Style.RESET_ALL)
    print(Fore.CYAN + "5. Buscar producto" + Style.RESET_ALL)
    print(Fore.CYAN + "6. Reporte de bajo stock" + Style.RESET_ALL)
    print(Fore.CYAN + "7. Limpiar pantalla" + Style.RESET_ALL)
    print(Fore.CYAN + "8. Salir" + Style.RESET_ALL)


def main_menu():
    """
    Función principal que ejecuta el menú y gestiona la interacción con el usuario.
    """
    crear_base_y_tabla()
    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción: ").strip()
        if opcion == "1":
            agregar_producto()
            pausa()
        elif opcion == "2":
            productos = (
                obtener_productos()
            )  # Llama al backend para obtener los productos
            imprimir_tabla(productos)  # Imprime la tabla en el frontend
            pausa()
        elif opcion == "3":
            actualizar_producto()
            pausa()
        elif opcion == "4":
            eliminar_producto()
            pausa()
        elif opcion == "5":
            buscar_producto()
            pausa()
        elif opcion == "6":
            reporte_bajo_stock()
            pausa()
        elif opcion == "7":
            limpiar_pantalla()
        elif opcion == "8":
            print(
                Fore.MAGENTA + "Saliendo del programa. ¡Hasta luego!" + Style.RESET_ALL
            )
            break
        else:
            print(Back.RED + "Opción no válida. Intente nuevamente." + Style.RESET_ALL)
            pausa()
