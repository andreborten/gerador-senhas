# Gerador de senhas seguras

Aplicação de linha de comando (CLI) em Python que gera senhas aleatórias
localmente, usando `secrets` para aleatoriedade criptográfica. Permite escolher
comprimento e inclusão de símbolos, sem dependências externas ou serviços web.

[Repositório](https://github.com/andreborten/gerador-senhas) ·
[Arquitetura Mermaid](docs/arquitetura.mmd) · [Licença MIT](LICENSE)

## Funcionalidades

- Senhas com **20 caracteres por padrão**; tamanho configurável de 8 a 256.
- Presença obrigatória de letras minúsculas, maiúsculas e números.
- Símbolos habilitados por padrão: `!@#$%&*+-=?_`.
- Opção de gerar somente letras e números.
- Mensagens de ajuda e rejeição de argumentos inválidos.
- Execução local: não grava senhas em arquivos e não as envia pela rede.

## Tecnologias utilizadas

| Tecnologia | Uso |
| --- | --- |
| Python 3.15.0 | Versão de referência para reproduzir a entrega |
| `argparse` | Leitura de argumentos e ajuda da CLI |
| `secrets` | Sorteio criptograficamente adequado de caracteres |
| `string` | Conjuntos de letras e números |
| `unittest` e `unittest.mock` | Testes unitários e simulação de falhas |
| `subprocess`, `sys` e `pathlib` | Testes de integração executando a CLI |
| Git e GitHub | Versionamento e publicação |
| Mermaid | Documentação da arquitetura proposta |
| OpenAI Codex, baseado em GPT-6 | Assistência na implementação, documentação e testes |

A IA foi usada como assistência ao desenvolvimento; o programa não chama
modelos de IA e não precisa de chave de API. Não há dependência do GitHub Copilot.
Click é uma alternativa ao `argparse`; Node.js e HTML/CSS/JavaScript são
alternativas para futuras versões, não tecnologias utilizadas nesta entrega.

## Configuração do ambiente

Pré-requisitos: Git e Python 3.10 ou superior. Para reproduzir o ambiente de
referência, use **Python 3.15.0**, também registrado em `.python-version`.
Esse arquivo informa a versão a gerenciadores compatíveis; não instala Python.

### 1. Clonar o projeto

```sh
git clone https://github.com/andreborten/gerador-senhas.git
cd gerador-senhas
python --version
```

No Linux/macOS, caso `python` não exista, use `python3` para criar o ambiente.

### 2. Criar um ambiente virtual

```sh
python -m venv .venv
```

Ative-o conforme seu terminal:

**Windows — Prompt de Comando:**

```bat
.venv\Scripts\activate.bat
```

**Windows — PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a ativação, use diretamente
`.\.venv\Scripts\python.exe` no lugar de `python` nos próximos comandos.
Não é necessário alterar a política de execução.

**Linux/macOS:**

```sh
source .venv/bin/activate
```

### 3. Verificar dependências

```sh
python -m pip install -r requirements.txt
```

O arquivo `requirements.txt` está incluído e documenta que não existem pacotes
externos para instalar. Os módulos de execução e testes acompanham o Python;
por isso não são listados como pacotes do PyPI. Nenhum banco de dados, ORM,
Pydantic ou arquivo `.env` é necessário.

### 4. Executar

```sh
python gerador.py
```

O comando imprime uma senha e encerra. A saída varia a cada execução; senhas
reais não são incluídas nos exemplos desta documentação.

## Exemplos de uso

```sh
# Ajuda e opções disponíveis
python gerador.py --help

# Senha padrão de 20 caracteres com símbolos
python gerador.py

# Senha de 24 caracteres com símbolos
python gerador.py --tamanho 24

# Senha de 32 caracteres sem símbolos
python gerador.py -t 32 --sem-simbolos

# Exemplo inválido: retorna erro e não imprime senha
python gerador.py --tamanho 7
```

| Argumento | Padrão | Efeito |
| --- | --- | --- |
| `-t`, `--tamanho` | `20` | Comprimento inteiro entre 8 e 256 |
| `--sem-simbolos` | Desabilitado | Remove símbolos do alfabeto |
| `-h`, `--help` | — | Exibe ajuda |

O código de saída é `0` para sucesso/ajuda e `2` para argumentos inválidos.
A aplicação não oferece API HTTP. A função Python pode ser importada:

```python
from gerador import gerar_senha

senha = gerar_senha(tamanho=24, usar_simbolos=False)
# Use a senha no destino pretendido; evite registrá-la em logs.
```

A função espera tamanho inteiro e `usar_simbolos` booleano; lança `ValueError`
para comprimento fora do intervalo. A CLI valida a conversão para inteiro.

## Segurança

O gerador usa escolhas uniformes por meio de `secrets.choice`. Se a candidata
não contiver todos os tipos exigidos, ela é descartada e uma nova é sorteada.
A rejeição preserva a distribuição uniforme entre as senhas aceitas.

O mínimo de 8 caracteres é um limite de compatibilidade, não uma recomendação
para todas as situações. Prefira o padrão de 20 ou mais, conforme o serviço
permita. Uma senha deve ser exclusiva por conta; armazene-a em um gerenciador
de senhas e habilite autenticação multifator quando disponível.

A senha é exibida em texto no terminal. Gravações de sessão, captura de tela,
redirecionamentos e o histórico visual do terminal podem expô-la. O programa
não protege contra malware, phishing ou comprometimento do dispositivo.

O `.gitignore` exclui caches, ambientes, logs, credenciais comuns e chaves.
Ele não detecta segredos inseridos diretamente no código nem remove conteúdo
já commitado. Revise os arquivos preparados com `git diff --cached`.

## Testes automatizados

Execute a partir da raiz do projeto, usando o ambiente virtual:

```sh
python -m unittest discover -s tests -v
```

A suíte contém **12 testes**, cobrindo:

- **Unitários:** tamanho padrão, limites, alfabeto permitido, presença dos tipos,
  ausência de símbolos e rejeição de tamanhos inválidos.
- **Fluxos controlados:** descarte de candidata inválida e propagação de falha
  da fonte aleatória, sem substituição por um gerador inseguro.
- **Integração:** execução real da CLI, opções, ajuda, erros e códigos de saída.

O resultado esperado é `Ran 12 tests` seguido de `OK`. Os testes não comprovam
imprevisibilidade criptográfica; ela depende de `secrets` e do sistema operacional.
Não há teste probabilístico exigindo que duas senhas sejam diferentes.

## Estrutura do projeto

```text
.
├── gerador.py
├── requirements.txt
├── .python-version
├── .gitignore
├── README.md
├── LICENSE
├── docs/
│   └── arquitetura.mmd
└── tests/
    └── test_gerador.py
```

## Limitações e Próximos Passos

O diagrama Mermaid descreve a arquitetura de evolução. Na implementação atual,
as responsabilidades estão concentradas em funções de `gerador.py`.

Ainda não implementado:

- Seleção individual de números, maiúsculas e minúsculas.
- Estimativa de força/entropia e avisos para configurações fracas.
- Modo de frase-senha com palavras sorteadas de uma lista adequada.
- Interface web, saída mascarada e integração com gerenciadores de senhas.
- Pipeline de integração contínua e validação em múltiplos sistemas operacionais.
- Validação explícita de todos os tipos de argumentos da função importável.

A entrega foi validada no Windows com Python 3.15.0. Python 3.10 é o mínimo
declarado, mas esta entrega não inclui uma matriz de testes para todas as versões.
Não há armazenamento, histórico de senhas ou banco de dados; qualquer expansão
nessa direção exigirá um projeto específico de proteção de segredos.

## Versão de entrega

A tag **[v1.0.0](https://github.com/andreborten/gerador-senhas/tree/v1.0.0)**
marca a primeira entrega da CLI documentada e testada. Ela cobre as funções
atuais; os itens de evolução acima não fazem parte dessa versão.

Para obter exatamente a entrega:

```sh
git fetch --tags
git switch --detach v1.0.0
```

Para contribuir a partir dela, crie uma branch com `git switch -c minha-melhoria`.
Use mensagens no padrão Conventional Commits, como `feat:`, `fix:`, `test:`
e `docs:`. Uma tag marca o código; não foi criada uma página de Release separada.

## Créditos e licença

- Autoria e manutenção: [andreborten](https://github.com/andreborten).
- Assistência de desenvolvimento: OpenAI Codex, baseado em GPT-6.
- Bibliotecas utilizadas: biblioteca padrão do Python e seus contribuidores.

Distribuído sob a **licença MIT**. Consulte [LICENSE](LICENSE) para os termos
completos, incluindo aviso de copyright e ausência de garantia.
