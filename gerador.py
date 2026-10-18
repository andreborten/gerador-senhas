"""Gerador de senhas local, sem dependências externas."""

import argparse
import secrets
import string


def gerar_senha(tamanho=16, usar_simbolos=True):
    grupos = [string.ascii_lowercase, string.ascii_uppercase, string.digits]
    if usar_simbolos:
        grupos.append("!@#$%&*+-=?_")
    if not 8 <= tamanho <= 256:
        raise ValueError("O tamanho deve estar entre 8 e 256 caracteres.")
    alfabeto = "".join(grupos)
    # Rejeição mantém a distribuição uniforme entre as senhas permitidas.
    while True:
        senha = "".join(secrets.choice(alfabeto) for _ in range(tamanho))
        if all(any(caractere in grupo for caractere in senha) for grupo in grupos):
            return senha


def main():
    parser = argparse.ArgumentParser(description="Gera uma senha aleatória localmente.")
    parser.add_argument("-t", "--tamanho", type=int, default=16, help="de 8 a 256 (padrão: 16)")
    parser.add_argument("--sem-simbolos", action="store_true", help="usa apenas letras e números")
    args = parser.parse_args()
    try:
        senha = gerar_senha(args.tamanho, not args.sem_simbolos)
    except ValueError as erro:
        parser.error(str(erro))
    print(senha)


if __name__ == "__main__":
    main()
