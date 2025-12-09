import os
from colorama import init, Fore, Style
init(autoreset=True)
def limpiar_pantalla():
    """Limpia la pantalla de la terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def imprimir_titulo(texto):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}==={texto.upper()}==={Style.RESET_ALL}\n")

def imprimir_error(texto):
    print(f"{Fore.RED} {Style.BRIGHT}ERROR: {texto}{Style.RESET_ALL}")

def imprimir_exito(texto):
    print(f"{Fore.GREEN}{Style.BRIGHT}ÉXITO: {texto}{Style.RESET_ALL}")

def validar_input_string(prompt):
    while True:
        dato = input(f"{Fore.YELLOW}{prompt}: {Style.RESET_ALL} ").strip()  #ingresa el nombre del producto 
        if dato: 
            return dato
        imprimir_error("El campo no puede estar vacío.")

def validar_input_float(prompt):
    while True:
        try:
            dato = float(input(f"{Fore.YELLOW}{prompt}: {Style.RESET_ALL} ").strip())
            if dato >= 0:
                return dato

        except ValueError:
            imprimir_error("Por favor, ingrese un número positivo.")
def validar_input_int(prompt):
    while True:
        try:
            dato = int(input(f"{Fore.YELLOW}{prompt}: {Style.RESET_ALL} ").strip())
            if dato >= 0:
                return dato

        except ValueError:
            imprimir_error("Por favor, ingrese un número entero positivo.") 