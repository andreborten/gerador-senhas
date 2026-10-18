# Guia da interface gráfica

## Interface gráfica desktop

A interface usa **Tkinter e ttk**, bibliotecas do Python para janelas e widgets. Execute `python interface.py` ou `python -m gerador_senhas.entrada_gui`. No Windows, abra `iniciar.bat` por duplo clique. Com argumentos, esse iniciador continua executando a CLI; `python gerador.py` também permanece disponível.

A janela contém campo de comprimento (8–256), quatro caixas de seleção, botão **Gerar senha**, campo de senha oculto por padrão, opção **Mostrar senha**, classificação em texto e cor, entropia e tempos dos cenários antigo e moderno. Enter também gera. Senhas longas podem ser percorridas horizontalmente no campo. Ao alterar os critérios, o resultado anterior é limpo; cada nova geração volta a ocultar a senha. Erros aparecem na janela sem fechar a aplicação.

A máscara é apenas visual: não protege contra comprometimento da máquina nem garante limpeza da memória. A aplicação não copia automaticamente para a área de transferência, não salva e não envia senhas. As mesmas regras e premissas da CLI valem na interface gráfica.

### Instalação do Tkinter

`requirements.txt` documenta Tkinter/ttk, mas não declara um pacote pip chamado tkinter: ele é fornecido com Python e Tcl/Tk. No instalador oficial do Python para Windows, habilite o componente Tcl/Tk. Verifique com `python -m tkinter`, que deve abrir uma janela de diagnóstico. Em distribuições Linux, instale o pacote Tk da distribuição quando necessário (em Debian/Ubuntu, normalmente `python3-tk`). A interface exige sessão gráfica disponível; a CLI não exige Tkinter.

Referência: [documentação oficial do Tkinter](https://docs.python.org/3/library/tkinter.html). A instalação local foi validada com Python 3.15.0 e Tk 9.0. A execução não ganhou dependências pip; pytest continua sendo a dependência de testes.

### Testes da interface

`python -m pytest -q` inclui testes com widgets Tk reais: geração, máscara e revelação, erros, alterações de configuração, falha da fonte aleatória e tamanho máximo. Sem Tk ou sessão gráfica, esses testes são explicitamente ignorados; os testes de CLI e núcleo continuam disponíveis. Na validação local, **201 testes passaram, sem testes ignorados**.

## Revisão de manutenção

A revisão v1.3.1 acrescenta diagnóstico de Tkinter/sessão gráfica indisponível, mantém a CLI independente da GUI e testa limpeza do resultado e restauração da máscara em erro. Consulte [decisões técnicas](decisoes.md) e [revisão técnica, segurança e testes](revisao-tecnica.md).

Revisão atual de contratos e limites: [refatoração v1.3.2](revisao-refatoracao.md).
