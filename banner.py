# banner.py

from colorama import Fore, Style, init
init(autoreset=True)

def show_banner():
    banner = f"""
{Fore.CYAN}
███████╗███╗   ███╗███████╗████████╗ █████╗  ██████╗ ███████╗
██╔════╝████╗ ████║██╔════╝╚══██╔══╝██╔══██╗██╔════╝ ██╔════╝
█████╗  ██╔████╔██║█████╗     ██║   ███████║██║  ███╗█████╗  
██╔══╝  ██║╚██╔╝██║██╔══╝     ██║   ██╔══██║██║   ██║██╔══╝  
███████╗██║ ╚═╝ ██║███████╗   ██║   ██║  ██║╚██████╔╝███████╗
╚══════╝╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
{Style.RESET_ALL}
                Revisión y limpieza de metadatos 🧽
                By m10sec (tremendo flipador de tools)
        Compatible con PDF, DOCX, ZIP, JPG, PNG, TXT...
    """
    print(banner)