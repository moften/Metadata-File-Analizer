from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter
from banner import show_banner
from scanner import scan_metadata
from cleaner import clean_metadata
import os

def clean_path(path: str) -> str:
    return os.path.expanduser(path.strip().replace('\\ ', ' '))

def main():
    show_banner()
    while True:
        print("\n¿Qué deseas hacer?")
        print("1. Revisar metadatos")
        print("2. Eliminar metadatos")
        print("3. Salir")

        choice = prompt("\nSelecciona una opción (1/2/3): ")

        if choice == "1":
            path = prompt("Introduce la ruta del archivo o carpeta a procesar: ", completer=PathCompleter())
            scan_metadata(clean_path(path))
        elif choice == "2":
            path = prompt("Introduce la ruta del archivo o carpeta a procesar: ", completer=PathCompleter())
            clean_metadata(clean_path(path))
        elif choice == "3":
            print("¡Hasta pronto, hacker del metadato!")
            break
        else:
            print("Opción no válida, intenta de nuevo.")

if __name__ == "__main__":
    main()