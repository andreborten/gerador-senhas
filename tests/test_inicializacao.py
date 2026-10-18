"""Diagnóstico de instalação sem depender de uma sessão Tk."""
import builtins
import types

import pytest

from gerador_senhas import entrada_gui


@pytest.mark.parametrize("nome", ["tkinter", "_tkinter"])
def test_tk_ausente(monkeypatch, capsys, nome):
    original = builtins.__import__
    def importar(name, *args, **kwargs):
        if name == "gui":
            raise ModuleNotFoundError("ausente", name=nome)
        return original(name, *args, **kwargs)
    monkeypatch.setattr(builtins, "__import__", importar)
    assert entrada_gui.main() == 1
    saida = capsys.readouterr()
    assert saida.out == ""
    assert "Tkinter" in saida.err and "gerador.py" in saida.err


def test_importacao_interna_nao_ocultada(monkeypatch):
    original = builtins.__import__
    def importar(name, *args, **kwargs):
        if name == "gui":
            raise ModuleNotFoundError("defeito interno", name="modulo_interno")
        return original(name, *args, **kwargs)
    monkeypatch.setattr(builtins, "__import__", importar)
    with pytest.raises(ModuleNotFoundError):
        entrada_gui.main()


def test_entrada_retorna_status_da_gui(monkeypatch):
    original = builtins.__import__
    def importar(name, *args, **kwargs):
        if name == "gui":
            return types.SimpleNamespace(main=lambda: 0)
        return original(name, *args, **kwargs)
    monkeypatch.setattr(builtins, "__import__", importar)
    assert entrada_gui.main() == 0


def test_cli_funciona_sem_tkinter():
    import subprocess
    import sys
    from pathlib import Path
    codigo = """
import builtins, runpy, sys
original = builtins.__import__
def importar(name, *args, **kwargs):
    if name.startswith('tkinter') or name == '_tkinter':
        raise ModuleNotFoundError('Tk ausente', name=name)
    return original(name, *args, **kwargs)
builtins.__import__ = importar
sys.argv = ['gerador_senhas', '--somente-senha']
runpy.run_module('gerador_senhas', run_name='__main__')
"""
    resultado = subprocess.run([sys.executable, "-c", codigo], capture_output=True,
                               text=True, timeout=15, cwd=Path(__file__).resolve().parents[1])
    assert resultado.returncode == 0
    assert resultado.stderr == ""
    assert len(resultado.stdout.strip()) == 20
