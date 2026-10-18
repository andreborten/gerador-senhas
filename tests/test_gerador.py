"""Testes de propriedades, validação, fonte aleatória e interface real."""
import itertools
import string
import subprocess
import sys
from pathlib import Path

import pytest

from gerador import gerar_senha
from gerador_senhas import core, cli

ROOT = Path(__file__).resolve().parents[1]
GRUPOS = (string.ascii_lowercase, string.ascii_uppercase, string.digits, core.SIMBOLOS)
OPCOES = ("usar_minusculas", "usar_maiusculas", "usar_numeros", "usar_simbolos")
COMBINACOES = list(itertools.product((False, True), repeat=4))[1:]


@pytest.mark.parametrize("ativos", COMBINACOES)
@pytest.mark.parametrize("tamanho", [8, 20, 256])
def test_grupos_e_tamanho(ativos, tamanho):
    senha = gerar_senha(tamanho, **dict(zip(OPCOES, ativos)))
    grupos = [grupo for ativo, grupo in zip(ativos, GRUPOS) if ativo]
    assert len(senha) == tamanho
    assert set(senha) <= set("".join(grupos))
    assert all(set(senha) & set(grupo) for grupo in grupos)


def test_padrao():
    senha = gerar_senha()
    assert len(senha) == 20
    assert all(set(senha) & set(grupo) for grupo in GRUPOS)


@pytest.mark.parametrize("tamanho", [-1, 0, 7, 257])
def test_tamanho_invalido(tamanho):
    with pytest.raises(ValueError):
        gerar_senha(tamanho)


@pytest.mark.parametrize("tamanho", [True, 20.0, "20", None])
def test_tipo_tamanho(tamanho):
    with pytest.raises(TypeError):
        gerar_senha(tamanho)


@pytest.mark.parametrize("opcao", OPCOES)
@pytest.mark.parametrize("valor", [0, 1, "sim", None])
def test_tipo_opcao(opcao, valor):
    with pytest.raises(TypeError):
        gerar_senha(**{opcao: valor})


def test_sem_grupos():
    with pytest.raises(ValueError):
        gerar_senha(**dict.fromkeys(OPCOES, False))


def test_rejeita_candidata_incompleta(monkeypatch):
    caracteres = iter("aaaaaaaaAa1!bcde")
    chamadas = []
    def escolher(alfabeto):
        chamadas.append(alfabeto)
        return next(caracteres)
    monkeypatch.setattr(core.secrets, "choice", escolher)
    assert gerar_senha(8) == "Aa1!bcde"
    assert chamadas == ["".join(GRUPOS)] * 16


def falhar(_):
    raise OSError("fonte indisponível")


def test_fonte_falha_sem_alternativa(monkeypatch):
    monkeypatch.setattr(core.secrets, "choice", falhar)
    with pytest.raises(OSError):
        gerar_senha()


def test_cli_fonte_falha(monkeypatch, capsys):
    monkeypatch.setattr(core.secrets, "choice", falhar)
    assert cli.main([]) == 1
    saida = capsys.readouterr()
    assert saida.out == ""
    assert "aleatoriedade" in saida.err


def executar(*args, modulo=False, relatorio=False):
    if not relatorio:
        args = (*args, "--somente-senha")
    comando = ["-m", "gerador_senhas"] if modulo else [str(ROOT / "gerador.py")]
    return subprocess.run([sys.executable, *comando, *args], cwd=ROOT,
                          capture_output=True, text=True, timeout=15)


@pytest.mark.parametrize("ativos", COMBINACOES)
def test_cli_combinacoes(ativos):
    flags = ["--sem-" + opcao.removeprefix("usar_")
             for ativo, opcao in zip(ativos, OPCOES) if not ativo]
    resultado = executar("--tamanho", "24", *flags)
    assert resultado.returncode == 0
    assert resultado.stderr == ""
    assert len(resultado.stdout.splitlines()) == 1
    senha = resultado.stdout.strip()
    grupos = [grupo for ativo, grupo in zip(ativos, GRUPOS) if ativo]
    assert len(senha) == 24
    assert set(senha) <= set("".join(grupos))
    assert all(set(senha) & set(grupo) for grupo in grupos)


@pytest.mark.parametrize("args", [
    ["-t", "7"], ["-t", "257"], ["-t", "abc"], ["--inexistente"],
    ["--sem-simbolos", "--sem-numeros", "--sem-maiusculas", "--sem-minusculas"],
])
def test_cli_erros(args):
    resultado = executar(*args)
    assert resultado.returncode == 2
    assert resultado.stdout == ""
    assert resultado.stderr


@pytest.mark.parametrize("modulo", [False, True])
def test_entradas_e_ajuda(modulo):
    resultado = executar(modulo=modulo)
    assert resultado.returncode == 0
    assert len(resultado.stdout.strip()) == 20
    ajuda = executar("--help", modulo=modulo)
    assert ajuda.returncode == 0
    for flag in ("--tamanho", "--sem-simbolos", "--sem-numeros", "--sem-maiusculas", "--sem-minusculas"):
        assert flag in ajuda.stdout
