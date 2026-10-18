"""Inicialização gráfica com diagnóstico de instalação, sem exigir Tk na CLI."""
import sys


def main() -> int:
    """Carrega Tk apenas ao abrir a GUI; falhas internas não são ocultadas."""
    try:
        from .gui import main as abrir_janela
    except ModuleNotFoundError as erro:
        if erro.name not in {"tkinter", "_tkinter"}:
            raise
        print("Tkinter não está instalado. Habilite Tcl/Tk no instalador Python "
              "ou instale o pacote Tk do sistema. A CLI continua disponível: "
              "python gerador.py", file=sys.stderr)
        return 1
    return abrir_janela()


if __name__ == "__main__":
    raise SystemExit(main())
