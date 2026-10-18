# Gerador de Senhas Seguras

Aplicação Python com interface gráfica desktop e linha de comando que gera senhas localmente com aleatoriedade criptográfica. Permite configurar o tamanho e selecionar letras maiúsculas, minúsculas, números e símbolos, sem enviar senhas pela rede. Apresenta a força e tempos médios estimados de força bruta para cenários hipotéticos de processamento antigo e moderno.

[Repositório](https://github.com/andreborten/gerador-senhas) · [MVP: apresentação e demonstração](docs/mvp.md) · [Escopo e requisitos](docs/escopo-mvp.md) · [Revisão do MVP](docs/revisao-escopo.md) · [Mermaid](docs/arquitetura.mmd) · [Decisões técnicas](docs/decisoes.md) · [Revisão técnica e segurança](docs/revisao-tecnica.md) · [Licença MIT](LICENSE)

## Funcionalidades

- Uma senha por execução; padrão de 20 caracteres com os quatro grupos.
- Comprimento entre 8 e 256 caracteres, inclusive.
- Exclusão independente de símbolos, números, maiúsculas e minúsculas.
- Pelo menos um caractere de cada grupo habilitado; nenhum dos grupos excluídos.
- Validação de configuração, ajuda integrada e função reutilizável em Python.

- Avaliação: super forte, forte, média ou fraca; entropia e dois tempos estimados.

## Instalação e ambiente

Requer Git e Python 3.10+. A versão de referência é 3.15.0, registrada em `.python-version`; a validação local foi feita em Windows com essa versão. Não é necessário instalar ORM, banco de dados, Node.js ou configurar chave de API.

```shell
git clone https://github.com/andreborten/gerador-senhas.git
cd gerador-senhas
python -m venv .venv
```

Ative o ambiente conforme seu terminal:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bat
:: Windows Prompt de Comando
.venv\Scripts\activate.bat
```

```sh
# Linux/macOS (use python3 para criar o ambiente se necessário)
source .venv/bin/activate
```

Instale as dependências de teste:

```shell
python -m pip install -r requirements.txt
```

A execução usa apenas a biblioteca padrão; `pytest==9.1.1` é a única dependência direta externa, usada para testes. O pip também instala suas dependências transitivas. O arquivo não é um lock completo dessas dependências.

Se o PowerShell bloquear a ativação, use diretamente `.\.venv\Scripts\python.exe` no lugar de `python`; não é necessário alterar a política de execução.

## Interface gráfica desktop

A interface usa **Tkinter e ttk**, bibliotecas do Python para janelas e widgets. Execute `python interface.py` ou `python -m gerador_senhas.entrada_gui`. No Windows, abra `iniciar.bat` por duplo clique. Com argumentos, esse iniciador continua executando a CLI; `python gerador.py` também permanece disponível.

A janela contém campo de comprimento (8–256), quatro caixas de seleção, botão **Gerar senha**, campo de senha oculto por padrão, opção **Mostrar senha**, classificação em texto e cor, entropia e tempos dos cenários antigo e moderno. Enter também gera. Senhas longas podem ser percorridas horizontalmente no campo. Ao alterar os critérios, o resultado anterior é limpo; cada nova geração volta a ocultar a senha. Erros aparecem na janela sem fechar a aplicação.

A máscara é apenas visual: não protege contra comprometimento da máquina nem garante limpeza da memória. A aplicação não copia automaticamente para a área de transferência, não salva e não envia senhas. As mesmas regras e premissas da CLI valem na interface gráfica.

### Instalação do Tkinter

`requirements.txt` documenta Tkinter/ttk, mas não declara um pacote pip chamado tkinter: ele é fornecido com Python e Tcl/Tk. No instalador oficial do Python para Windows, habilite o componente Tcl/Tk. Verifique com `python -m tkinter`, que deve abrir uma janela de diagnóstico. Em distribuições Linux, instale o pacote Tk da distribuição quando necessário (em Debian/Ubuntu, normalmente `python3-tk`). A interface exige sessão gráfica disponível; a CLI não exige Tkinter.

Referência: [documentação oficial do Tkinter](https://docs.python.org/3/library/tkinter.html). A instalação local foi validada com Python 3.15.0 e Tk 9.0. A execução não ganhou dependências pip; pytest continua sendo a dependência de testes.

### Testes da interface

`python -m pytest -q` inclui testes com widgets Tk reais: geração, máscara e revelação, erros, alterações de configuração, falha da fonte aleatória e tamanho máximo. Sem Tk ou sessão gráfica, esses testes são explicitamente ignorados; os testes de CLI e núcleo continuam disponíveis. Na validação local, **195 testes passaram, sem testes ignorados**.

Guia dedicado: [interface gráfica](docs/interface-grafica.md).

## Uso pela CLI

```shell
python gerador.py
python gerador.py --tamanho 24
python gerador.py -t 32 --sem-simbolos
python gerador.py -t 20 --sem-numeros --sem-maiusculas
python gerador.py -t 24 --sem-simbolos --sem-numeros --sem-maiusculas
python -m gerador_senhas --tamanho 24
python gerador.py --help
```

Cada geração bem-sucedida imprime a senha na primeira linha, seguida da classificação, entropia e estimativas com ressalvas. Para obter somente uma linha de senha, use `python gerador.py --somente-senha`. Essa opção preserva o formato de saída anterior para scripts. O último exemplo de geração com três exclusões usa somente minúsculas. Os caracteres permitidos são `a-z`, `A-Z`, `0-9` e `!@#$%&*+-=?_`. Todos os grupos começam habilitados; as opções `--sem-*` removem grupos.

| Opção | Comportamento |
| --- | --- |
| `-t`, `--tamanho` | Inteiro entre 8 e 256; padrão 20 |
| `--sem-simbolos` | Exclui símbolos |
| `--sem-numeros` | Exclui números |
| `--sem-maiusculas` | Exclui letras maiúsculas |
| `--sem-minusculas` | Exclui letras minúsculas |
| `--somente-senha` | Omite o relatório, imprimindo somente a senha |
| `-h`, `--help` | Mostra ajuda |

### Erros

```shell
python gerador.py --tamanho 7
python gerador.py --sem-simbolos --sem-numeros --sem-maiusculas --sem-minusculas
```

Ambos os comandos são inválidos. A CLI informa o motivo em stderr, não imprime senha e encerra com código 2. Sucesso e ajuda retornam 0. Falha de acesso à fonte criptográfica retorna 1, sem gerar uma senha alternativa.

### Uso em código Python

```python
from gerador_senhas import gerar_senha, avaliar_configuracao

senha = gerar_senha(24, usar_simbolos=False, usar_numeros=True,
                    usar_maiusculas=True, usar_minusculas=True)
avaliacao = avaliar_configuracao(24, usar_simbolos=False, usar_numeros=True,
                                usar_maiusculas=True, usar_minusculas=True)
print(avaliacao.classificacao)
```

A importação antiga `from gerador import gerar_senha` continua funcionando. A API exige tamanho inteiro (não aceita booleanos) e opções booleanas. Tipos incorretos geram `TypeError`; tamanho fora da faixa ou ausência de grupos gera `ValueError`; falhas da fonte segura propagam `OSError`.

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

Detalhamento: [metodologia e premissas](docs/forca-senha.md).

## Tecnologias e IA generativa

| Tecnologia | Uso |
| --- | --- |
| Python 3.10+ | Linguagem; referência local 3.15.0 |
| `tkinter` / `ttk` | Interface gráfica desktop, fornecida com Python/Tcl/Tk |
| `argparse` | Processamento de argumentos e ajuda |
| `secrets` e `string` | Sorteios criptográficos e alfabetos |
| `math`, `decimal`, `itertools` e `dataclasses` | Entropia, contagem e estimativas sem dependências adicionais |
| pytest 9.1.1 | Testes unitários e integração da CLI |
| Git / GitHub | Versionamento e distribuição |
| Mermaid | Diagrama de fluxo e comunicação dos componentes |
| OpenAI Codex | Assistência na lógica, testes, interface e documentação |

IA é usada durante o desenvolvimento, não na execução. Não há modelo de IA embarcado, chamada de API ou dependência de Copilot. A versão exata do modelo de assistência não é fixada pelo projeto. Python/argparse é a alternativa escolhida do escopo; Click, JavaScript, ORM e Pydantic não são necessários ao MVP.

## Segurança

O núcleo usa `secrets.choice`, apoiado pela fonte criptográfica do sistema operacional. Cada candidata é sorteada uniformemente do alfabeto habilitado. Candidatas que não contêm todos os grupos escolhidos são rejeitadas: isso preserva a distribuição uniforme entre senhas válidas, sem inserir caracteres obrigatórios em posições previsíveis.

O padrão usa 20 caracteres. Aceitar 8 caracteres atende compatibilidade, mas não torna qualquer configuração forte: comprimento e alfabeto importam. Use senhas únicas por conta, um gerenciador de senhas e MFA quando disponível.

A aplicação não grava senhas em arquivos ou logs e não usa rede. A saída é texto claro no terminal; gravações de sessão, capturas de tela e redirecionamento podem expô-la. Não há apagamento garantido de memória. `.gitignore` cobre padrões comuns de credenciais e caches, mas não detecta segredos inseridos em código.

## Testes automatizados

```shell
python -m pytest -q
```

A suíte contém 195 casos: todas as 15 combinações não vazias de grupos nos tamanhos 8, 20 e 256; presença e exclusão de caracteres; valores e tipos inválidos; rejeição de candidata incompleta; falha da fonte criptográfica; ajuda, entradas por script/módulo e códigos de saída. A CLI também é executada em subprocessos reais. A avaliação é testada por enumeração independente de alfabetos pequenos, fórmulas conhecidas, limites das quatro classes, tempos, formatação, configurações inválidas e o máximo de 256 caracteres.

A rejeição e a falha da fonte são testadas com substituições controladas. Não usamos ausência de duplicatas em uma amostra como prova de segurança. Os testes não demonstram imprevisibilidade criptográfica nem garantem ausência de colisões. Resultado local da revisão: **195 testes passaram em Windows/Python 3.15.0**.

## Arquitetura e comunicação

`forca.py` calcula espaço válido, entropia, classificação e tempos; `core.py` concentra validação e geração; `cli.py` recebe argumentos e controla saída/erros. `gerador.py` preserva a entrada anterior e o pacote suporta execução por módulo.

```mermaid
flowchart TD
    U["Usuário"] -->|"Argumentos: tamanho e grupos"| CLI["CLI: argparse"]
    U -->|"Abrir interface.py"| INI["entrada_gui: diagnóstico de Tkinter e sessão"]
    INI -->|"Instalação ou sessão indisponível"| E
    INI -->|"Abre janela"| GUI
    U -->|"Campos e botão Gerar"| GUI["GUI: Tkinter e ttk"]
    GUI -->|"Mesma configuração"| V
    GUI -->|"Configuração válida"| F
    G -->|"Senha válida"| GUI
    F -->|"Classe, bits e tempos"| GUI
    GUI -->|"Senha mascarada, relatório ou erro"| U
    CLI -->|"Configuração"| V{"Validação: 8 a 256 e algum grupo?"}
    V -->|"Não: erro, saída 2"| E["Erro sem senha: stderr na CLI ou mensagem na GUI"]
    V -->|"Sim: alfabeto permitido"| G["Núcleo: gerar_senha"]
    G -->|"Solicita caracteres"| S["secrets.choice: fonte criptográfica do sistema"]
    S -->|"Caracteres sorteados"| G
    S -->|"Falha: saída 1"| E
    G -->|"Senha candidata"| C{"Contém todos os grupos selecionados?"}
    C -->|"Não: descarta candidata"| G
    C -->|"Sim: senha válida"| O["stdout: senha na primeira linha, saída 0"]
    CLI -->|"Mesma configuração, salvo --somente-senha"| F["forca.py: conta espaço válido e entropia"]
    F -->|"Bits: limites 40, 60 e 80"| K["fraca / média / forte / super forte"]
    F -->|"Média de tentativas e taxas hipotéticas"| B["Força bruta offline: antigo 10^6/s; moderno 10^11/s"]
    K -->|"Classificação e bits"| O
    B -->|"Tempos médios e ressalvas"| O
    O -->|"Exibição local"| U
    T["pytest: propriedades, validação, rejeição e CLI"] -.->|"Verifica"| V
    T -.->|"Verifica"| G
    T -.->|"Verifica"| CLI
    T -.->|"Verifica contagem, faixas e tempos"| F
```

O arquivo fonte está em [docs/arquitetura.mmd](docs/arquitetura.mmd). O diagrama representa apenas componentes implementados.

## Organização

```text
gerador-senhas/
├── interface.py
├── iniciar.bat
├── gerador.py
├── gerador_senhas/
│   ├── __init__.py
│   ├── __main__.py
│   ├── entrada_gui.py
│   ├── gui.py
│   ├── forca.py
│   ├── core.py
│   └── cli.py
├── tests/test_gerador.py
├── tests/test_forca.py
├── tests/test_gui.py
├── tests/test_inicializacao.py
├── docs/
│   ├── arquitetura.mmd
│   ├── forca-senha.md
│   ├── decisoes.md
│   ├── revisao-tecnica.md
│   ├── interface-grafica.md
│   ├── mvp.md
│   ├── escopo-mvp.md
│   └── revisao-escopo.md
├── requirements.txt
├── .gitignore
├── .python-version
├── LICENSE
└── README.md
```

## Limitações e Próximos Passos

- Interfaces locais desktop e CLI: não há web, API HTTP, persistência ou sincronização.
- A força é estimada para senhas uniformes deste gerador; não há avaliação de senhas humanas, verificação de vazamentos ou frases-senha.
- Taxas de ataque fixas são ilustrativas; não há benchmark nem previsão específica por hash/hardware.
- Há máscara visual na GUI; a CLI exibe texto claro. Não há integração com gerenciadores ou limpeza garantida de memória.
- Não há geração em lote ou alfabetos personalizados.
- Python 3.10+ é o mínimo de sintaxe; validação completa em Windows/3.15 e parcial em 3.12, sem matriz de sistemas.
- Próximas evoluções: CI multiplataforma, empacotamento, frases-senha e opções adicionais de alfabeto.

Veja os limites e critérios de aceite completos no [escopo do MVP](docs/escopo-mvp.md).

## Versionamento e entrega

As tags `v1.0.0` e `v1.1.0` preservam entregas anteriores. A versão `v1.3.1` melhora diagnóstico, validações e organização após revisão técnica. A versão `v1.3.0` adiciona a interface Tkinter. A versão `v1.2.0` inclui força e estimativas; a saída padrão passa a incluir o relatório. Scripts que dependem de uma única linha devem usar `--somente-senha`. Tags identificam pontos de entrega; não pressupõem a criação de uma página GitHub Release.

```shell
git fetch --tags
git switch --detach v1.3.1
```

Para contribuir, crie uma branch, execute os testes e use Conventional Commits, por exemplo `feat: adiciona frases-senha` ou `docs: esclarece instalação`.

## Evolução da implementação

| Etapa / versão | Implementação e motivo | Registro |
| --- | --- | --- |
| Estrutura inicial | Script CLI, dependências, README e diagrama inicial | `4ee4c6c`, `0816d44` |
| Sincronização | Conciliação dos históricos local e remoto | `b9ec2be` |
| v1.0.0 | Geração com secrets, tamanho e símbolos opcionais, 12 testes unittest, licença e documentação de entrega | `68c91cc` |
| v1.1.0 | Pacote modular, quatro grupos independentes, tipagem, validação e 96 casos pytest; escopo formal e revisão | `203aa82`; correção documental `f5dfa06` |
| v1.2.0 | Força, entropia e tempos hipotéticos com contagem do espaço válido; 144 testes; --somente-senha mantém saída para scripts | `b54f1fb` |
| Apresentação do MVP | Jornada, demonstração, aceite e limites consolidados | `15ada2d` |
| Abertura no Windows | iniciar.bat mantém resultado visível, resolvendo o fechamento da janela ao terminar a CLI | `6fceffc` |
| v1.3.0 | GUI Tkinter/ttk com configuração, máscara, força e tempos; 154 testes; iniciador abre GUI sem argumentos | `cbd5514` |
| v1.3.1 | Revisão de segurança/SOLID/Clean Code; tratamento de inicialização Tk, validação numérica, parâmetros únicos na CLI, organização da GUI, 195 testes e registro de decisões | Revisão atual |

Os commits vazios `4ef3815` e `cd61c30` marcam entregas solicitadas, sem mudanças funcionais. Tags antigas são preservadas. O diagnóstico e as escolhas de cada etapa estão em [decisões técnicas](docs/decisoes.md).

## Qualidade, segurança e manutenção

A revisão atual registrou **195 testes aprovados** no Windows/Python 3.15.0 e **95% de cobertura medida**, incluindo ramificações; subprocessos não estão agregados na medição. Bandit não encontrou achados e pip-audit não encontrou vulnerabilidades conhecidas nos pacotes resolvidos na consulta de 18/10/2026. Não se trata de certificação ou garantia de ausência de falhas.

O código tem comentários e docstrings nas funções de produção. As responsabilidades estão separadas, mas a aderência a SOLID é parcial: SRP é favorecido, OCP/DIP têm limites, LSP não é aplicável à ausência de hierarquia própria e não foram introduzidas abstrações artificiais. Nenhuma dependência externa é necessária em execução; ferramentas de auditoria são opcionais.

A inicialização por `interface.py` ou `python -m gerador_senhas.entrada_gui` informa falta de Tkinter/sessão gráfica e indica a CLI. Valores inválidos não geram senha; falhas inesperadas de programação não são ocultadas. Riscos residuais incluem exposição no terminal/memória, máquina comprometida, configurações fracas e interpretação indevida de estimativas.

Veja a [revisão técnica completa](docs/revisao-tecnica.md) para achados, correções, comandos de reprodução, matriz dos testes e limitações.

## Créditos e licença

Autor: [andreborten](https://github.com/andreborten). Desenvolvimento assistido por OpenAI Codex. Projeto distribuído sob a [licença MIT](LICENSE).
