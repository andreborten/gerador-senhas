"""Integração real dos widgets Tk; exige ambiente gráfico disponível."""
import pytest

tk = pytest.importorskip("tkinter")
from gerador_senhas import gui
from test_gerador import COMBINACOES, OPCOES, GRUPOS


@pytest.fixture
def app():
    try:
        janela = tk.Tk()
    except tk.TclError as erro:
        pytest.skip(f"Ambiente gráfico indisponível: {erro}")
    janela.withdraw()
    aplicacao = gui.Aplicacao(janela)
    yield aplicacao
    janela.destroy()


def test_geracao_mascara_e_visibilidade(app):
    app.botao_gerar.invoke()
    assert len(app.senha.get()) == 20
    assert app.classe.get() == "Super forte"
    assert app.campo_senha.cget("show") == "*"
    app.mostrar.set(True)
    app.alternar_visibilidade()
    assert app.campo_senha.cget("show") == ""
    app.gerar()
    assert app.campo_senha.cget("show") == "*"


@pytest.mark.parametrize("tamanho", ["", "abc", "7", "257", "20.5"])
def test_tamanho_invalido_limpa_resultado(app, tamanho):
    app.gerar()
    app.tamanho.set(tamanho)
    app.gerar()
    assert app.senha.get() == ""
    assert "inteiro" in app.status.get() or "entre 8 e 256" in app.status.get()


def test_sem_grupos(app):
    for opcao in app.opcoes.values():
        opcao.set(False)
    app.gerar()
    assert app.senha.get() == ""
    assert "ao menos" in app.status.get()


def test_numerica_e_configuracao_alterada(app):
    app.tamanho.set("8")
    for nome, opcao in app.opcoes.items():
        opcao.set(nome == "usar_numeros")
    app.gerar()
    assert app.senha.get().isdigit()
    assert len(app.senha.get()) == 8
    assert app.classe.get() == "Fraca"
    assert "50.00 segundos" in app.antigo.get()
    assert "menos de 1 segundo" in app.moderno.get()
    app.tamanho.set("25")
    assert app.senha.get() == ""
    assert app.classe.get() == "Aguardando geração"


def test_fonte_falha(app, monkeypatch):
    def falha(*args, **kwargs):
        raise OSError("falha simulada")
    monkeypatch.setattr(gui, "gerar_senha", falha)
    app.gerar()
    assert app.senha.get() == ""
    assert "aleatoriedade segura" in app.status.get()


def test_maximo_e_janela(app):
    app.tamanho.set("256")
    app.gerar()
    app.janela.deiconify()
    app.janela.update()
    assert len(app.senha.get()) == 256
    assert "anos" in app.moderno.get()
    limite = app.rotulo_status.winfo_rooty() + app.rotulo_status.winfo_height()
    assert limite <= app.janela.winfo_rooty() + app.janela.winfo_height()



@pytest.mark.parametrize("ativos", COMBINACOES)
def test_gui_todos_os_grupos(app, ativos):
    app.tamanho.set("8")
    for nome, ativo in zip(OPCOES, ativos):
        app.opcoes[nome].set(ativo)
    app.gerar()
    senha = app.senha.get()
    grupos = [grupo for ativo, grupo in zip(ativos, GRUPOS) if ativo]
    assert len(senha) == 8
    assert set(senha) <= set("".join(grupos))
    assert all(set(senha) & set(grupo) for grupo in grupos)


@pytest.mark.parametrize("tamanho,classe", [(8, "Fraca"), (16, "Média"), (20, "Forte"), (25, "Super forte")])
def test_gui_classes(app, tamanho, classe):
    app.tamanho.set(str(tamanho))
    for nome, opcao in app.opcoes.items():
        opcao.set(nome == "usar_numeros")
    app.gerar()
    assert app.classe.get() == classe


def test_falha_apos_resultado_limpa_dados(app, monkeypatch):
    app.gerar()
    app.mostrar.set(True)
    app.alternar_visibilidade()
    def falhar(*args, **kwargs):
        raise OSError("indisponível")
    monkeypatch.setattr(gui, "gerar_senha", falhar)
    app.gerar()
    assert app.senha.get() == ""
    assert app.campo_senha.cget("show") == "*"
    assert app.antigo.get() == "—"
    assert app.moderno.get() == "—"


def test_sem_sessao_grafica(monkeypatch, capsys):
    def falhar():
        raise tk.TclError("sem display")
    monkeypatch.setattr(tk, "Tk", falhar)
    assert gui.main() == 1
    assert capsys.readouterr().out == ""


def test_ciclo_principal_fecha_janela(monkeypatch):
    janela = tk.Tk()
    janela.withdraw()
    monkeypatch.setattr(tk, "Tk", lambda: janela)
    janela.after(10, janela.destroy)
    assert gui.main() == 0
