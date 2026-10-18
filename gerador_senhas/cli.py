"""Interface de linha de comando com argparse."""
import argparse
import sys
from collections.abc import Sequence

from .core import gerar_senha


def main(argv: Sequence[str] | None = None) -> int:
    """Retorna 0 no sucesso, 1 se a fonte falhar; argparse encerra com 2 no erro."""
    parser = argparse.ArgumentParser(description="Gera uma senha aleatória localmente.")
    parser.add_argument("-t", "--tamanho", type=int, default=20,
                        help="de 8 a 256 caracteres (padrão: 20)")
    for grupo in ("simbolos", "numeros", "maiusculas", "minusculas"):
        parser.add_argument(f"--sem-{grupo}", action="store_true",
                            help=f"exclui {grupo} da senha")
    args = parser.parse_args(argv)
    try:
        senha = gerar_senha(
            args.tamanho,
            usar_simbolos=not args.sem_simbolos,
            usar_numeros=not args.sem_numeros,
            usar_maiusculas=not args.sem_maiusculas,
            usar_minusculas=not args.sem_minusculas,
        )
    except ValueError as erro:
        parser.error(str(erro))
    except OSError:
        print("Não foi possível acessar a fonte de aleatoriedade segura.", file=sys.stderr)
        return 1
    print(senha)
    return 0
