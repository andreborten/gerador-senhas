"""Entrada compatível para execução e importação do gerador."""
from gerador_senhas import gerar_senha
from gerador_senhas.cli import main

__all__ = ["gerar_senha", "main"]

if __name__ == "__main__":
    raise SystemExit(main())
