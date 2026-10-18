"""Estimativas para senhas uniformes deste gerador, não para senhas humanas."""
from dataclasses import dataclass
from decimal import Decimal, localcontext
from itertools import combinations
from math import log2

from .core import selecionar_grupos

TAXA_ANTIGA = 10**6
TAXA_MODERNA = 10**11


@dataclass(frozen=True)
class Avaliacao:
    """Espaço válido, entropia e tempos médios em cenários hipotéticos offline."""

    combinacoes: int
    entropia_bits: float
    classificacao: str
    segundos_antigo: Decimal
    segundos_moderno: Decimal


def classificar(entropia_bits: float) -> str:
    """Aplica faixas do projeto: <40, <60, <80 e >=80 bits."""
    if entropia_bits < 40:
        return "fraca"
    if entropia_bits < 60:
        return "média"
    if entropia_bits < 80:
        return "forte"
    return "super forte"


def avaliar_configuracao(
    tamanho: int = 20, usar_simbolos: bool = True, *, usar_numeros: bool = True,
    usar_maiusculas: bool = True, usar_minusculas: bool = True,
) -> Avaliacao:
    """Avalia o espaço de senhas geradas com esta configuração.

    Inclusão-exclusão conta somente cadeias com todos os grupos obrigatórios.
    Pressupõe atacante que conhece configuração e algoritmo, enumera sem
    repetição e sorteio uniforme. Média exata de tentativas: (N + 1) / 2.
    Taxas ilustrativas fixas; não são benchmarks de máquinas ou hashes reais.
    """
    grupos = selecionar_grupos(tamanho, usar_simbolos, usar_numeros=usar_numeros,
                              usar_maiusculas=usar_maiusculas,
                              usar_minusculas=usar_minusculas)
    tamanhos = [len(grupo) for grupo in grupos]
    total = sum(tamanhos)
    espaco = sum(
        (-1)**quantidade * (total - sum(subconjunto))**tamanho
        for quantidade in range(len(tamanhos) + 1)
        for subconjunto in combinations(tamanhos, quantidade)
    )
    bits = log2(espaco)
    # Decimal suporta os resultados de 256 caracteres sem overflow de float.
    with localcontext() as contexto:
        contexto.prec = 28
        antigo = Decimal(espaco + 1) / Decimal(2 * TAXA_ANTIGA)
        moderno = Decimal(espaco + 1) / Decimal(2 * TAXA_MODERNA)
    return Avaliacao(espaco, bits, classificar(bits), antigo, moderno)


def formatar_tempo(segundos: Decimal) -> str:
    """Exibe duração aproximada; tempos muito grandes usam notação científica."""
    if segundos < 1:
        return "menos de 1 segundo"
    for limite, divisor, unidade in (
        (60, 1, "segundos"), (3600, 60, "minutos"),
        (86400, 3600, "horas"), (31557600, 86400, "dias"),
    ):
        if segundos < limite:
            return f"{segundos / divisor:.2f} {unidade}"
    anos = segundos / Decimal(31557600)
    return f"{anos:.2E} anos" if anos >= 10**6 else f"{anos:.2f} anos"
