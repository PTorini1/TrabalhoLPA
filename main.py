import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from code.interface import InterfaceCampoMinado
except ImportError as e:
    print(f"Erro ao importar módulos do jogo: {e}")
    print("Verifique se o Pygame está instalado: pip install pygame")
    sys.exit(1)

def main():
    try:
        jogo = InterfaceCampoMinado()
        jogo.executar()
    except Exception as e:
        print(f"Erro ao executar o jogo: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
