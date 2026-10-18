"""Validação e geração, independentes da interface CLI."""
import secrets
import string

SIMBOLOS = "!@#$%&*+-=?_"


def gerar_senha(
    tamanho: int = 20,
    usar_simbolos: bool = True,
    *,
    usar_numeros: bool = True,
    usar_maiusculas: bool = True,
    usar_minusculas: bool = True,
) -> str:
    """Gera uma senha com ao menos um caractere de cada grupo habilitado.

    Aceita tamanhos entre 8 e 256 e exige ao menos um grupo. Rejeita tipos
    incorretos com TypeError e configurações inválidas com ValueError.
    Falhas da fonte criptográfica são propagadas, sem fonte alternativa.
    A amostragem por rejeição preserva uniformidade entre senhas permitidas.
    """
    grupos = selecionar_grupos(tamanho, usar_simbolos, usar_numeros=usar_numeros,
                              usar_maiusculas=usar_maiusculas,
                              usar_minusculas=usar_minusculas)
    alfabeto = "".join(grupos)
    while True:
        senha = "".join(secrets.choice(alfabeto) for _ in range(tamanho))
        if all(any(caractere in grupo for caractere in senha) for grupo in grupos):
            return senha


def selecionar_grupos(
    tamanho: int, usar_simbolos: bool = True, *, usar_numeros: bool = True,
    usar_maiusculas: bool = True, usar_minusculas: bool = True,
) -> list[str]:
    """Valida a configuração e retorna os alfabetos disjuntos habilitados."""
    if type(tamanho) is not int:
        raise TypeError("O tamanho deve ser um número inteiro.")
    if not 8 <= tamanho <= 256:
        raise ValueError("O tamanho deve estar entre 8 e 256 caracteres.")
    opcoes = (
        (usar_minusculas, string.ascii_lowercase),
        (usar_maiusculas, string.ascii_uppercase),
        (usar_numeros, string.digits),
        (usar_simbolos, SIMBOLOS),
    )
    if any(type(ativo) is not bool for ativo, _ in opcoes):
        raise TypeError("As opções de caracteres devem ser booleanas.")
    grupos = [grupo for ativo, grupo in opcoes if ativo]
    if not grupos:
        raise ValueError("Selecione ao menos um tipo de caractere.")
    return grupos
