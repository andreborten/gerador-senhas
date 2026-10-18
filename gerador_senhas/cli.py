"""Interface de linha de comando com argparse."""
import argparse
import sys
from collections.abc import Sequence

from .core import gerar_senha
from .forca import avaliar_configuracao, formatar_tempo


def main(argv: Sequence[str] | None = None) -> int:
    """Retorna 0 no sucesso, 1 se a fonte falhar; argparse encerra com 2 no erro."""
    parser = argparse.ArgumentParser(description="Gera uma senha aleatória localmente.")
    parser.add_argument("-t", "--tamanho", type=int, default=20,
                        help="de 8 a 256 caracteres (padrão: 20)")
    for grupo in ("simbolos", "numeros", "maiusculas", "minusculas"):
        parser.add_argument(f"--sem-{grupo}", action="store_true",
                            help=f"exclui {grupo} da senha")
    parser.add_argument("--somente-senha", action="store_true",
                        help="imprime apenas a senha, sem avaliação (para scripts)")
    args = parser.parse_args(argv)
    opcoes = {
        "usar_simbolos": not args.sem_simbolos,
        "usar_numeros": not args.sem_numeros,
        "usar_maiusculas": not args.sem_maiusculas,
        "usar_minusculas": not args.sem_minusculas,
    }
    try:
        senha = gerar_senha(args.tamanho, **opcoes)
        # O mesmo conjunto de critérios evita divergência entre senha e avaliação.
        avaliacao = None if args.somente_senha else avaliar_configuracao(args.tamanho, **opcoes)
    except ValueError as erro:
        parser.error(str(erro))
    except OSError:
        print("Não foi possível acessar a fonte de aleatoriedade segura.", file=sys.stderr)
        return 1
    print(senha)
    if avaliacao is not None:
        print(f"Força: {avaliacao.classificacao} ({avaliacao.entropia_bits:.2f} bits)")
        print("Tempo médio de força bruta offline — cenários hipotéticos:")
        print(f"  Antigo (10^6 tentativas/s): {formatar_tempo(avaliacao.segundos_antigo)}")
        print(f"  Moderno (10^11 tentativas/s): {formatar_tempo(avaliacao.segundos_moderno)}")
        print("Estimativas, não garantias: dependem do hash, custo e hardware; "
              "não cobrem vazamentos ou phishing.")
    return 0
