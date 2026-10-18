# Escopo do MVP — Gerador de Senhas Seguras

## Objetivo

Oferecer uma aplicação local de linha de comando que gere senhas aleatórias com fonte criptográfica, conforme tamanho e tipos de caracteres definidos pelo usuário. O público são pessoas que precisam criar senhas e desenvolvedores que desejam reutilizar a função Python.

## Solução e tecnologias

Python 3.10 ou superior, `argparse` para CLI, `secrets` para sorteios, `string` para alfabetos e `pytest` para testes. A referência local é Python 3.15.0. Não há banco de dados, ORM, serviço de IA, autenticação ou dependência externa em execução. JavaScript e interface web são alternativas não escolhidas neste MVP.

A IA generativa (OpenAI Codex) auxiliou a implementação da função principal, os testes automatizados, a CLI e a documentação. Nenhuma senha é enviada a um modelo de IA.

## Requisitos funcionais

| ID | Requisito | Critério de aceite |
| --- | --- | --- |
| RF01 | Gerar uma senha por execução | Sem argumentos, imprimir uma linha com 20 caracteres e retornar 0 |
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

## Fluxo de uso

1. Usuário informa tamanho e, opcionalmente, os grupos que deseja excluir.
2. CLI valida os argumentos; núcleo valida tamanho, tipos e grupos.
3. Núcleo sorteia a candidata usando a fonte criptográfica do sistema.
4. Candidatas sem algum grupo obrigatório são descartadas e o processo se repete.
5. CLI imprime uma única senha ou informa um erro sem imprimir senha.

## Segurança e limites do compromisso

A configuração padrão usa 20 caracteres e os quatro grupos. O mínimo de 8 é um limite de compatibilidade, não uma recomendação geral de força. Configurações curtas e alfabetos pequenos reduzem a resistência a tentativas de adivinhação. A aplicação permite essas escolhas, sem prometer que toda configuração será adequada a qualquer serviço.

A uniformidade decorre do algoritmo e da fonte criptográfica, não de observar que um pequeno lote não contém repetições. Testes automatizados verificam propriedades e o uso da fonte; não provam imprevisibilidade ou ausência de colisões. Senhas podem repetir com probabilidade não nula.

A senha é exibida em texto claro no terminal. Captura de tela, gravação de sessão, redirecionamento e ambiente comprometido podem expô-la. Não há garantia de limpeza da memória em Python. Recomenda-se senha exclusiva por conta, gerenciador de senhas e MFA.

## Fora do escopo e próximos passos

- Interface web, API HTTP, banco de dados, ORM e validação com bibliotecas externas.
- Armazenamento, sincronização, área de transferência e integração com gerenciadores.
- Estimativa de entropia/força, consulta de vazamentos e frases-senha.
- Geração em lote, alfabetos personalizados e exclusão de caracteres ambíguos.
- CI com matriz de versões/sistemas e empacotamento para instalação via pip.

Esses itens são evoluções propostas e não funcionalidades entregues.

## Aceite da entrega

Executar os comandos do README em ambiente virtual novo e rodar a suíte pytest. Confirmar os requisitos RF01–RF11 e RNF01–RNF09 pela matriz acima, pelos testes e pela inspeção do código. Verificar documentação e diagrama versionados, licença MIT e tag de entrega no Git. O resultado da revisão está em [revisao-escopo.md](revisao-escopo.md).
