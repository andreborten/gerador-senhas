# Escopo do MVP — Gerador de Senhas Seguras

Apresentação do produto entregue e roteiro de demonstração: [MVP](mvp.md).

## Objetivo

Oferecer uma aplicação local com interface gráfica desktop e linha de comando que gere senhas aleatórias com fonte criptográfica, conforme tamanho e tipos de caracteres definidos pelo usuário. O sistema deve também apresentar a força (super forte, forte, média ou fraca) e estimativas médias de força bruta para cenários antigo e moderno. O público são pessoas que precisam criar senhas e desenvolvedores que desejam reutilizar a função Python.

## Solução e tecnologias

Python 3.10 ou superior, Tkinter/ttk para interface desktop, `argparse` para CLI, `secrets` para sorteios, `string` para alfabetos e `pytest` para testes. A referência local é Python 3.15.0. Não há banco de dados, ORM, serviço de IA, autenticação ou dependência externa em execução. JavaScript e interface web são alternativas não escolhidas neste MVP.

A IA generativa (OpenAI Codex) auxiliou a implementação da função principal, os testes automatizados, a CLI e a documentação. Nenhuma senha é enviada a um modelo de IA.

## Requisitos funcionais

| ID | Requisito | Critério de aceite |
| --- | --- | --- |
| RF01 | Gerar uma senha por execução | Sem argumentos, imprimir senha de 20 caracteres, seguida do relatório de força e retornar 0 |
| RF02 | Configurar comprimento por `-t` ou `--tamanho` | Aceitar inteiros de 8 a 256, inclusive; rejeitar demais valores |
| RF03 | Selecionar minúsculas ASCII | Habilitadas por padrão; `--sem-minusculas` exclui `a-z` |
| RF04 | Selecionar maiúsculas ASCII | Habilitadas por padrão; `--sem-maiusculas` exclui `A-Z` |
| RF05 | Selecionar números | Habilitados por padrão; `--sem-numeros` exclui `0-9` |
| RF06 | Selecionar símbolos | Habilitados por padrão; `--sem-simbolos` exclui `!@#$%&*+-=?_` |
| RF07 | Respeitar todos os grupos escolhidos | Cada senha contém pelo menos um caractere de cada grupo habilitado e nenhum de grupos desabilitados |
| RF08 | Validar configuração | Rejeitar todos os grupos desabilitados, argumentos desconhecidos e tamanho inválido; CLI retorna 2 sem senha |
| RF09 | Disponibilizar ajuda | `--help` descreve tamanho e as quatro opções de exclusão |
| RF10 | Permitir reutilização | Exportar `gerar_senha` com tipagem; manter importação por `gerador` e entrada por script ou módulo |
| RF11 | Tratar falha da fonte segura | Propagar `OSError` na API; na CLI, mensagem em stderr, retorno 1 e nenhuma senha |
| RF12 | Classificar a força gerada | Exibir fraca (<40 bits), média (40 a <60), forte (60 a <80) ou super forte (≥80) |
| RF13 | Estimar força bruta | Calcular espaço válido N e média (N+1)/(2×taxa); mostrar cenários antigo 10^6/s e moderno 10^11/s |
| RF14 | Explicar as estimativas | Exibir ressalva e documentar taxas hipotéticas, limites, hash/hardware e ausência de garantia |
| RF15 | Preservar saída para scripts | `--somente-senha` imprime apenas a senha; API original continua retornando string |
| RF16 | Interface gráfica desktop | Tkinter/ttk com tamanho, grupos, geração, classe e tempos; mesmo núcleo da CLI |
| RF17 | Controle de exibição | Senha mascarada por padrão, opção Mostrar senha e nova geração oculta novamente |
| RF18 | Consistência da tela | Alterações limpam resultado anterior; erros aparecem sem encerrar a janela |

## Requisitos não funcionais

| ID | Requisito | Verificação |
| --- | --- | --- |
| RNF01 | Usar aleatoriedade criptográfica | `secrets.choice`, sem `random`, seed configurável ou fallback inseguro |
| RNF02 | Evitar viés introduzido pela composição | Sortear uniformemente do alfabeto e rejeitar candidatas incompletas; teste determinístico da rejeição |
| RNF03 | Operar localmente | Código de execução sem rede, telemetria, arquivos de senha ou logs de senha |
| RNF04 | Separar responsabilidades | Núcleo independente da CLI, funções com tipos e docstrings |
| RNF05 | Ser fácil de instalar | Biblioteca padrão em execução; `requirements.txt` com pytest fixado para testes |
| RNF06 | Ter testes automatizados | `python -m pytest -q` passa; testa todas as 15 combinações de grupos e limites |
| RNF07 | Documentar uso e manutenção | README com instalação, exemplos, segurança, limitações, créditos, licença e versão; Mermaid coerente com código |
| RNF08 | Evitar versionar artefatos locais | `.gitignore` cobre ambientes, caches e padrões comuns de credenciais; revisão humana continua necessária |
| RNF09 | Compatibilidade | Sintaxe compatível com Python 3.10+; execução validada em Windows/Python 3.15.0, sem alegar matriz de plataformas testada |
| RNF10 | Consistência matemática | Considerar grupos obrigatórios por inclusão-exclusão; testar por enumeração independente e fórmulas conhecidas |
| RNF11 | Robustez numérica | Suportar até 256 caracteres sem overflow, com inteiros e Decimal; apresentar anos em notação científica quando necessário |
| RNF12 | Disponibilidade da GUI | Requer Tcl/Tk e sessão gráfica; CLI continua independente de Tkinter |
| RNF13 | Interface legível | Layout organizado, uso por teclado e classificação em texto além da cor |

## Fluxo de uso

1. Usuário informa tamanho e, opcionalmente, os grupos que deseja excluir.
2. CLI valida os argumentos; núcleo valida tamanho, tipos e grupos.
3. Núcleo sorteia a candidata usando a fonte criptográfica do sistema.
4. Candidatas sem algum grupo obrigatório são descartadas e o processo se repete.
5. Após gerar, CLI calcula a avaliação com a mesma configuração e imprime senha, força e estimativas; `--somente-senha` omite o relatório. Erros não imprimem senha.

## Força e estimativa de força bruta

O programa apresenta **fraca**, **média**, **forte** ou **super forte** após gerar a senha. A avaliação usa o comprimento e o alfabeto habilitado, considerando a exigência de pelo menos um caractere de cada grupo. Não avalia senhas humanas ou textos fornecidos externamente.

| Entropia H em bits | Classificação |
| --- | --- |
| H < 40 | fraca |
| 40 ≤ H < 60 | média |
| 60 ≤ H < 80 | forte |
| H ≥ 80 | super forte |

Esses limiares são uma convenção educativa deste projeto, não uma certificação nem faixas prescritas pela OWASP ou NIST. O rótulo não garante proteção contra phishing, malware, reutilização ou vazamentos.

Se N é o número de senhas permitidas, `H = log2(N)`. N é calculado por inclusão-exclusão: para cada subconjunto de grupos, subtrai-se ou soma-se o número de cadeias que omitem esses grupos. Com um grupo de A caracteres, `N = A^L`; com dois grupos de tamanhos a e b, `N = (a+b)^L - a^L - b^L`. A fórmula completa e os testes estão em `forca.py` e `test_forca.py`. Isso evita superestimar o espaço usando simplesmente `A^L` quando há grupos obrigatórios.

Pressupõe-se senha sorteada uniformemente, atacante conhecendo tamanho e grupos, enumeração sem repetição e taxa constante. O número médio de tentativas é `(N + 1) / 2`; o tempo médio em segundos é `(N + 1) / (2 × taxa)`. Uma busca completa pode exigir N tentativas; a senha também pode ser encontrada na primeira tentativa. O valor exibido é média, não prazo mínimo ou garantia.

| Cenário hipotético offline | Taxa adotada |
| --- | --- |
| Processamento antigo | 10^6 tentativas/s (1 milhão) |
| Processamento moderno | 10^11 tentativas/s (100 bilhões) |

As taxas são hipóteses ilustrativas de menor e maior capacidade, não benchmarks históricos ou de hardware específico. Não há medição da máquina do usuário. O algoritmo de hash, seu custo, paralelismo e hardware alteram muito a velocidade; ataques online ainda dependem de limites e bloqueios. A [OWASP sobre armazenamento de senhas](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) explica a importância de funções apropriadas e do fator de trabalho. A fonte sustenta essas ressalvas, não os valores ou limiares escolhidos pelo projeto.

Exemplo verificável: oito dígitos gerados uniformemente dão N = 100.000.000, cerca de 26,58 bits e classificação fraca. A média estimada é 50,0000005 segundos no cenário antigo e 0,000500000005 segundo no moderno. A CLI arredonda a apresentação, exibindo “menos de 1 segundo” no segundo caso. Para tempos enormes, usa notação científica em anos (ano de 365,25 dias), mantendo cálculos com inteiros e Decimal para suportar até 256 caracteres.

A saída padrão contém senha, força, entropia, dois tempos e ressalva. `--somente-senha` suprime o relatório para uso em scripts; a função `gerar_senha` continua retornando apenas uma string. A API `avaliar_configuracao` recebe os mesmos parâmetros de geração e retorna `Avaliacao` com combinações, entropia, classificação e tempos em segundos. Passe exatamente a mesma configuração usada para gerar a senha.

Referência detalhada: [forca-senha.md](forca-senha.md).

## Segurança e limites do compromisso

A configuração padrão usa 20 caracteres e os quatro grupos. O mínimo de 8 é um limite de compatibilidade, não uma recomendação geral de força. Configurações curtas e alfabetos pequenos reduzem a resistência a tentativas de adivinhação. A aplicação permite essas escolhas, sem prometer que toda configuração será adequada a qualquer serviço.

A uniformidade decorre do algoritmo e da fonte criptográfica, não de observar que um pequeno lote não contém repetições. Testes automatizados verificam propriedades e o uso da fonte; não provam imprevisibilidade ou ausência de colisões. Senhas podem repetir com probabilidade não nula.

A senha é exibida em texto claro no terminal. Captura de tela, gravação de sessão, redirecionamento e ambiente comprometido podem expô-la. Não há garantia de limpeza da memória em Python. Recomenda-se senha exclusiva por conta, gerenciador de senhas e MFA.

## Fora do escopo e próximos passos

- Interface web, API HTTP, banco de dados, ORM e validação com bibliotecas externas.
- Armazenamento, sincronização, área de transferência e integração com gerenciadores.
- Consulta de vazamentos, avaliação de senhas humanas, frases-senha e benchmarks reais de hardware.
- Geração em lote, alfabetos personalizados e exclusão de caracteres ambíguos.
- CI com matriz de versões/sistemas e empacotamento para instalação via pip.

Esses itens são evoluções propostas e não funcionalidades entregues.

## Aceite da entrega

Executar os comandos do README em ambiente virtual novo e rodar a suíte pytest. Confirmar os requisitos RF01–RF18 e RNF01–RNF13 pela matriz acima, pelos testes e pela inspeção do código. Verificar documentação e diagrama versionados, licença MIT e tag de entrega no Git. O resultado da revisão está em [revisao-escopo.md](revisao-escopo.md).

## Entrega da interface desktop

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
