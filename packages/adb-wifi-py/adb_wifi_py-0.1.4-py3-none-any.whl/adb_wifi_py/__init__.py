from .main import main

def main_cli() -> None:
    try:
        main()
    except KeyboardInterrupt:
        print("\rClosing...")