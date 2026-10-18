"""Interface gráfica local com Tkinter/ttk e núcleo compartilhado com a CLI."""
import sys
import tkinter as tk
from tkinter import ttk

from .core import gerar_senha
from .forca import avaliar_configuracao, formatar_tempo

CORES = {"fraca": "#b42318", "média": "#946200", "forte": "#1766b1", "super forte": "#08765a"}


class Aplicacao:
    """Janela de configuração, geração e avaliação de senhas."""

    def __init__(self, janela: tk.Tk) -> None:
        """Conecta estado, aparência, controles e eventos da janela recebida."""
        self.janela = janela
        janela.title("Gerador de Senhas Seguras")
        janela.geometry("780x730")
        janela.minsize(700, 690)
        janela.configure(background="#eef2f7")
        self._configurar_estilo()
        self._iniciar_variaveis()
        self._montar_layout()
        self.tamanho.trace_add("write", self.invalidar)
        for variavel in self.opcoes.values():
            variavel.trace_add("write", self.invalidar)
        janela.bind("<Return>", lambda evento: self.gerar())
        self.campo_tamanho.focus_set()

    def _configurar_estilo(self) -> None:
        """Centraliza aparência, sem regras de geração."""
        estilo = ttk.Style(self.janela)
        estilo.theme_use("clam")
        estilo.configure("TFrame", background="#eef2f7")
        estilo.configure("Card.TFrame", background="white")
        estilo.configure("TLabel", background="white", foreground="#18283b", font=("Segoe UI", 10))
        estilo.configure("Title.TLabel", background="#eef2f7", font=("Segoe UI", 20, "bold"))
        estilo.configure("Sub.TLabel", background="#eef2f7", foreground="#526178")
        estilo.configure("Heading.TLabel", font=("Segoe UI", 12, "bold"))
        estilo.configure("TCheckbutton", background="white", font=("Segoe UI", 10))
        estilo.configure("Primary.TButton", background="#225ac7", foreground="white",
                         font=("Segoe UI", 12, "bold"), padding=(18, 8))
        estilo.map("Primary.TButton", background=[("active", "#1849a4")])
        estilo.configure("TButton", font=("Segoe UI", 10), padding=6)

    def _iniciar_variaveis(self) -> None:
        """Inicializa o estado de apresentação da janela."""
        self.tamanho = tk.StringVar(value="20")
        self.opcoes = {nome: tk.BooleanVar(value=True) for nome in
                       ("usar_minusculas", "usar_maiusculas", "usar_numeros", "usar_simbolos")}
        self.senha = tk.StringVar()
        self.mostrar = tk.BooleanVar(value=False)
        self.classe = tk.StringVar(value="Aguardando geração")
        self.entropia = tk.StringVar(value="Configure e clique em Gerar senha.")
        self.antigo = tk.StringVar(value="—")
        self.moderno = tk.StringVar(value="—")
        self.status = tk.StringVar(value="Pronto. A senha não é salva nem enviada pela rede.")

    def _montar_layout(self) -> None:
        """Organiza controles e resultado em seções visuais."""
        container = ttk.Frame(self.janela, padding=16)
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=1)
        ttk.Label(container, text="Gerador de Senhas", style="Title.TLabel").grid(sticky="w")
        ttk.Label(container, text="Segurança local. Configuração simples. Sem cadastro.",
                  style="Sub.TLabel").grid(sticky="w", pady=(4, 12))
        config = ttk.Frame(container, style="Card.TFrame", padding=12)
        config.grid(row=2, sticky="ew")
        config.columnconfigure(1, weight=1)
        ttk.Label(config, text="1. Personalize sua senha", style="Heading.TLabel").grid(
            row=0, columnspan=2, sticky="w", pady=(0, 12))
        ttk.Label(config, text="Comprimento (8 a 256)").grid(row=1, column=0, sticky="w")
        self.campo_tamanho = ttk.Spinbox(config, from_=8, to=256, textvariable=self.tamanho, width=8)
        self.campo_tamanho.grid(row=1, column=1, sticky="e")
        rotulos = ("Minúsculas  a–z", "Maiúsculas  A–Z", "Números  0–9", "Símbolos  !@#$…")
        for i, ((_, variavel), rotulo) in enumerate(zip(self.opcoes.items(), rotulos)):
            ttk.Checkbutton(config, text=rotulo, variable=variavel).grid(
                row=2 + i // 2, column=i % 2, sticky="w", pady=(10, 0))
        self.botao_gerar = ttk.Button(container, text="Gerar senha", style="Primary.TButton", command=self.gerar)
        self.botao_gerar.grid(row=3, sticky="ew", pady=10)
        resultado = ttk.Frame(container, style="Card.TFrame", padding=12)
        resultado.grid(row=4, sticky="ew")
        resultado.columnconfigure(0, weight=1)
        ttk.Label(resultado, text="2. Sua senha", style="Heading.TLabel").grid(sticky="w")
        self.campo_senha = ttk.Entry(resultado, textvariable=self.senha, state="readonly",
                                     font=("Consolas", 14), show="*")
        self.campo_senha.grid(row=1, sticky="ew", pady=(10, 6))
        ttk.Checkbutton(resultado, text="Mostrar senha", variable=self.mostrar,
                        command=self.alternar_visibilidade).grid(row=2, sticky="w")
        self.rotulo_classe = ttk.Label(resultado, textvariable=self.classe, font=("Segoe UI", 15, "bold"))
        self.rotulo_classe.grid(row=3, sticky="w", pady=(8, 2))
        ttk.Label(resultado, textvariable=self.entropia).grid(row=4, sticky="w")
        ttk.Separator(resultado).grid(row=5, sticky="ew", pady=8)
        ttk.Label(resultado, text="Tempo médio de força bruta • cenários hipotéticos",
                  style="Heading.TLabel").grid(row=6, sticky="w")
        ttk.Label(resultado, textvariable=self.antigo).grid(row=7, sticky="w", pady=(8, 4))
        ttk.Label(resultado, textvariable=self.moderno).grid(row=8, sticky="w")
        ttk.Label(container, text="Estimativas, não garantias. Taxas: antigo 10⁶/s; moderno 10¹¹/s. "
                  "O tempo real depende do hash, custo e hardware. Não cobre phishing ou vazamentos.",
                  style="Sub.TLabel", wraplength=680).grid(row=5, sticky="ew", pady=(12, 6))
        self.rotulo_status = ttk.Label(container, textvariable=self.status, style="Sub.TLabel", wraplength=680)
        self.rotulo_status.grid(row=6, sticky="ew")

    def invalidar(self, *_: str) -> None:
        """Remove resultado anterior quando critérios mudam, evitando avaliação desatualizada."""
        self.senha.set("")
        self.mostrar.set(False)
        self.alternar_visibilidade()
        self.classe.set("Aguardando geração")
        self.rotulo_classe.configure(foreground="#18283b")
        self.entropia.set("Clique em Gerar senha para aplicar os critérios.")
        self.antigo.set("—")
        self.moderno.set("—")
        self.status.set("Configuração alterada. Gere uma nova senha.")

    def alternar_visibilidade(self) -> None:
        """Alterna máscara visual; não implica proteção ou limpeza da memória."""
        self.campo_senha.configure(show="" if self.mostrar.get() else "*")

    def gerar(self) -> None:
        """Gera e avalia a mesma configuração, mostrando erros na própria janela."""
        self.invalidar()
        try:
            try:
                tamanho = int(self.tamanho.get())
            except ValueError:
                raise ValueError("Informe um comprimento inteiro entre 8 e 256.") from None
            opcoes = {nome: valor.get() for nome, valor in self.opcoes.items()}
            senha = gerar_senha(tamanho, **opcoes)
            avaliacao = avaliar_configuracao(tamanho, **opcoes)
        except ValueError as erro:
            self.status.set(str(erro))
            return
        except OSError:
            self.status.set("Não foi possível acessar a fonte de aleatoriedade segura. Tente novamente.")
            return
        self.mostrar.set(False)
        self.alternar_visibilidade()
        self.senha.set(senha)
        self.classe.set(avaliacao.classificacao.capitalize())
        self.rotulo_classe.configure(foreground=CORES[avaliacao.classificacao])
        self.entropia.set(f"{avaliacao.entropia_bits:.2f} bits • {tamanho} caracteres")
        self.antigo.set(f"Antigo: {formatar_tempo(avaliacao.segundos_antigo)}")
        self.moderno.set(f"Moderno: {formatar_tempo(avaliacao.segundos_moderno)}")
        self.status.set("Senha gerada. Use Mostrar senha para visualizar. Use uma senha única por conta.")


def main() -> int:
    """Abre a janela; informa ausência de ambiente gráfico sem traceback."""
    try:
        janela = tk.Tk()
    except tk.TclError:
        print("Não foi possível abrir a interface gráfica. Verifique Tcl/Tk e a sessão "
              "gráfica, ou execute python gerador.py para usar a CLI.", file=sys.stderr)
        return 1
    try:
        Aplicacao(janela)
        janela.mainloop()
    finally:
        # Libera recursos Tk também se a construção da interface falhar.
        try:
            janela.destroy()
        except tk.TclError:
            pass  # A janela pode já ter sido destruída pelo botão de fechar.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
