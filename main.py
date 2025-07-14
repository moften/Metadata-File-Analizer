# main.py

import os
from banner import show_banner
from scanner import select_path, scan_metadata
from cleaner import clean_metadata

def main():
    show_banner()
    while True:
        print("\n¿Qué deseas hacer?")
        print("1. Revisar metadatos")
        print("2. Eliminar metadatos")
        print("3. Salir")

        choice = input("\nSelecciona una opción (1/2/3): ")

        if choice == "1":
            path = select_path()
            scan_metadata(path)
        elif choice == "2":
            path = select_path()
            clean_metadata(path)
        elif choice == "3":
            print("¡Hasta pronto, hacker del metadato!")
            break
        else:
            print("Opción no válida, intenta de nuevo.")

if __name__ == "__main__":
    main()