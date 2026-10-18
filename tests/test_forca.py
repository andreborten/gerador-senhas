"""Validação matemática independente e integração do relatório de força."""
from decimal import Decimal
from itertools import product
from math import log2

import pytest

from gerador_senhas import avaliar_configuracao
from gerador_senhas import forca
from test_gerador import executar, COMBINACOES, OPCOES, GRUPOS


@pytest.mark.parametrize("bits,esperada", [
    (0, "fraca"), (39.999, "fraca"), (40, "média"), (59.999, "média"),
    (60, "forte"), (79.999, "forte"), (80, "super forte"), (1000, "super forte"),
])
def test_limites_classificacao(bits, esperada):
    assert forca.classificar(bits) == esperada


def test_alfabeto_numerico_calculo_conhecido():
    avaliacao = avaliar_configuracao(8, False, usar_maiusculas=False, usar_minusculas=False)
    assert avaliacao.combinacoes == 10**8
    assert avaliacao.entropia_bits == pytest.approx(8 * log2(10))
    assert avaliacao.classificacao == "fraca"
    assert avaliacao.segundos_antigo == Decimal("50.0000005")
    assert avaliacao.segundos_moderno == Decimal("0.000500000005")


def test_dois_grupos_formula_fechada():
    avaliacao = avaliar_configuracao(8, False, usar_numeros=False)
    assert avaliacao.combinacoes == 52**8 - 2 * 26**8


@pytest.mark.parametrize("grupos", [["ab"], ["ab", "c"], ["a", "b", "c"], ["a", "b", "c", "d"]])
def test_contagem_por_enumeracao_independente(monkeypatch, grupos):
    monkeypatch.setattr(forca, "selecionar_grupos", lambda *a, **kw: grupos)
    esperado = sum(all(set(candidata) & set(grupo) for grupo in grupos)
                   for candidata in product("".join(grupos), repeat=8))
    assert avaliar_configuracao(8).combinacoes == esperado


@pytest.mark.parametrize("ativos", COMBINACOES)
def test_combinacoes_estimativas(ativos):
    opcoes = dict(zip(OPCOES, ativos))
    curta = avaliar_configuracao(8, **opcoes)
    longa = avaliar_configuracao(256, **opcoes)
    alfabeto = sum(len(g) for ativo, g in zip(ativos, GRUPOS) if ativo)
    assert 0 < curta.combinacoes <= alfabeto**8
    assert longa.combinacoes > curta.combinacoes
    assert longa.entropia_bits > curta.entropia_bits
    assert longa.segundos_antigo.is_finite()
    assert longa.segundos_moderno.is_finite()
    assert longa.segundos_antigo / longa.segundos_moderno == pytest.approx(Decimal(100000))
    assert "anos" in forca.formatar_tempo(longa.segundos_moderno)


@pytest.mark.parametrize("kwargs,erro", [
    ({"tamanho": 7}, ValueError), ({"tamanho": 257}, ValueError),
    ({"tamanho": True}, TypeError), ({"usar_simbolos": 1}, TypeError),
    (dict.fromkeys(OPCOES, False), ValueError),
])
def test_validacao_compartilhada(kwargs, erro):
    with pytest.raises(erro):
        avaliar_configuracao(**kwargs)


@pytest.mark.parametrize("segundos,esperado", [
    ("0.01", "menos de 1 segundo"), ("1", "1.00 segundos"),
    ("60", "1.00 minutos"), ("3600", "1.00 horas"),
    ("86400", "1.00 dias"), ("31557600", "1.00 anos"),
    ("31557600000000", "1.00E+6 anos"),
])
def test_formatacao(segundos, esperado):
    assert forca.formatar_tempo(Decimal(segundos)) == esperado


@pytest.mark.parametrize("tamanho,classe", [(8, "fraca"), (16, "média"), (20, "forte"), (25, "super forte")])
def test_cli_classes_numericas(tamanho, classe):
    resultado = executar("-t", str(tamanho), "--sem-simbolos", "--sem-maiusculas",
                         "--sem-minusculas", relatorio=True)
    assert resultado.returncode == 0
    assert resultado.stderr == ""
    linhas = resultado.stdout.splitlines()
    assert len(linhas[0]) == tamanho and linhas[0].isdigit()
    assert f"Força: {classe}" in resultado.stdout
    assert "10^6 tentativas/s" in resultado.stdout
    assert "10^11 tentativas/s" in resultado.stdout
    assert "Estimativas, não garantias" in resultado.stdout


@pytest.mark.parametrize("modulo", [False, True])
def test_cli_relatorio_padrao_e_maximo(modulo):
    for args in ([], ["-t", "256"]):
        resultado = executar(*args, modulo=modulo, relatorio=True)
        assert resultado.returncode == 0
        assert "Força: super forte" in resultado.stdout
        assert "anos" in resultado.stdout


def test_cli_invalida_sem_relatorio():
    resultado = executar("-t", "7", relatorio=True)
    assert resultado.returncode == 2
    assert resultado.stdout == ""


@pytest.mark.parametrize("valor", [float("nan"), float("inf"), float("-inf"), -1])
def test_entropia_invalida(valor):
    with pytest.raises(ValueError):
        forca.classificar(valor)


@pytest.mark.parametrize("valor", [True, "80", None])
def test_tipo_entropia(valor):
    with pytest.raises(TypeError):
        forca.classificar(valor)


@pytest.mark.parametrize("valor", ["NaN", "sNaN", "Infinity", "-Infinity", "-1"])
def test_duracao_invalida(valor):
    with pytest.raises(ValueError):
        forca.formatar_tempo(Decimal(valor))


def test_tipo_duracao():
    with pytest.raises(TypeError):
        forca.formatar_tempo(1.0)


@pytest.mark.parametrize("valor", [10**1000, -(10**1000)], ids=["positivo", "negativo"])
def test_entropia_inteira_grande(valor):
    if valor < 0:
        with pytest.raises(ValueError):
            forca.classificar(valor)
    else:
        assert forca.classificar(valor) == "super forte"


def test_avaliacao_independe_contexto_decimal():
    from decimal import Inexact, localcontext
    esperada = avaliar_configuracao()
    with localcontext() as contexto:
        contexto.prec = 2
        contexto.traps[Inexact] = True
        assert avaliar_configuracao() == esperada


def test_formatacao_independe_contexto_decimal():
    from decimal import Inexact, localcontext
    duracao = Decimal("123456789")
    esperado = forca.formatar_tempo(duracao)
    with localcontext() as contexto:
        contexto.prec = 2
        contexto.traps[Inexact] = True
        assert forca.formatar_tempo(duracao) == esperado
