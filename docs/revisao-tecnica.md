# Revisão técnica, segurança e qualidade

Data: 18/10/2026. Entrega de manutenção: v1.3.1. Revisão do código atual, requisitos RF01–RF18/RNF01–RNF13, documentação, dependências e testes. Decisões: [decisoes.md](decisoes.md).

## Conclusão

O programa atende ao requisito real: gerar senhas locais configuráveis, apresentar força e estimativas com premissas, por CLI ou GUI. Há comentários e docstrings explicando decisões relevantes. Não foram identificadas dependências de execução desnecessárias. A separação de módulos favorece manutenção, mas não se afirma conformidade completa com todos os princípios SOLID.

A revisão encontrou e corrigiu lacunas de robustez, ampliou os testes e não detectou vulnerabilidades conhecidas nas verificações executadas. Isso não constitui certificação, pentest ou garantia de ausência de falhas.

## Achados e ações

| Achado | Impacto | Ação / estado |
| --- | --- | --- |
| Tkinter ou sessão gráfica indisponível causava traceback na inicialização | Diagnóstico ruim para o usuário | Entrada gráfica com mensagem orientativa, código 1 e indicação da CLI |
| classificar aceitava NaN como super forte; formatar_tempo aceitava duração negativa ou falhava sem diagnóstico para NaN | Resultado incorreto no uso direto dos auxiliares; geração normal não produzia esses valores | Validação explícita de tipos, finitude e sinal, com testes |
| CLI repetia parâmetros de geração e avaliação | Risco de divergência em futuras alterações | Um único dicionário de opções, avaliação antes de emitir senha |
| Construção da GUI concentrava estilo, estado e layout em um método longo | Dificuldade de manutenção | Métodos separados com docstrings |
| Falha após revelação deixava estado de visibilidade ativo, embora sem senha no campo | Estado visual inconsistente | Limpeza restaura máscara em sucesso, alteração e erro |
| Documentos ainda descreviam etapas anteriores como atuais | Ambiguidade sobre GUI, testes e limitações | README e documentos de uso atualizados; histórico identificado |

## Comentários e Clean Code

Os módulos e funções de produção possuem docstrings; a revisão acrescentou a do construtor da GUI. Comentários explicam por que bool não é comprimento válido, por que Decimal evita overflow, por que geração/avaliação compartilham parâmetros e por que TclError é tolerado ao destruir uma janela já fechada. Não foram adicionados comentários repetindo cada linha.

Nomes são descritivos, validação é centralizada, núcleo não depende de Tk/CLI, dados de avaliação são imutáveis, exceções são específicas e não há estado global mutável de senhas. GUI ainda tem um método de montagem de widgets relativamente extenso, mas sem regra criptográfica embutida. Extrair cada widget em uma classe não traria benefício suficiente ao MVP. Testes têm algumas utilidades compartilhadas via importação entre módulos de teste; conftest.py é uma evolução possível, não necessária para o funcionamento.

## Avaliação de SOLID

| Princípio | Avaliação | Evidência / limite |
| --- | --- | --- |
| SRP — responsabilidade única | Atendido em boa parte | Geração, força, interfaces e inicialização separadas; GUI agrega estado visual e widgets |
| OCP — aberto a extensão | Parcial | Nova interface reutiliza núcleo, mas novos alfabetos, faixas ou políticas exigem editar código |
| LSP — substituição | Não aplicável à arquitetura atual | Não há hierarquia própria de classes substituíveis; não se deve declarar aprovação sem cenário |
| ISP — interfaces pequenas | Compatível com o desenho funcional | Funções focadas, sem interface abstrata extensa que imponha métodos não usados |
| DIP — inversão de dependência | Parcial | Núcleo independe de apresentação, porém interfaces importam funções concretas; não há contrato injetado |

Decidiu-se manter funções simples. Protocolos e injeção explícita devem ser considerados se aparecerem provedores ou algoritmos alternativos, não apenas para marcar todos os princípios como atendidos.

## Verificação de segurança

**Modelo de ameaça:** proteger a geração e a apresentação local de uma senha aleatória em máquina confiável; considerar atacante offline conhecendo tamanho, grupos e algoritmo. Não proteger contra administrador malicioso, malware, keylogger, captura de tela ou serviço que armazene senhas incorretamente.

| Área | Resultado e risco residual |
| --- | --- |
| Aleatoriedade | secrets.choice, sem random ou fallback; candidatas inválidas descartadas |
| Viés | Rejeição preserva uniformidade sob as premissas; ausência de colisões não é garantida |
| Entradas | Comprimento limitado a 8–256, booleanos explícitos e ao menos um grupo; entradas não são executadas |
| Rede e armazenamento | Código de execução sem chamadas de rede, gravação de senha ou logs de senha |
| Injeção | Nenhum eval/exec, desserialização insegura ou comando shell no núcleo/GUI/CLI; iniciar.bat é um lançador local, não deve receber comandos montados de entrada não confiável |
| Exposição | CLI imprime texto claro; GUI mascara visualmente. Memória, cópia manual e redirecionamento continuam riscos |
| Força | Configurações curtas/alfabetos pequenos podem ser fracos; rótulos e taxas são educativos, não garantias |
| Credenciais | Busca por formatos comuns em 23 arquivos rastreados do estado anterior às adições desta revisão: nenhum achado; não verifica todo segredo possível nem histórico Git |
| Gitignore | .env, credentials.json, .venv e caches verificados como ignorados; não substitui inspeção humana |
| Infraestrutura | Python, Tcl/Tk, sistema operacional e ferramentas externas não foram auditados como produtos completos |

## Dependências e ferramentas

Aplicação: biblioteca padrão e Tkinter/Tcl/Tk para a GUI. Testes: pytest==9.1.1. ORM, validação externa, web framework e bibliotecas de IA não são necessários. Ferramentas de revisão não foram adicionadas ao requirements.txt.

- `pip check`: nenhuma dependência instalada quebrada no ambiente principal.
- Bandit 1.9.4: pacote gerador_senhas + gerador.py + interface.py; nenhum achado, erro de leitura ou supressão no relatório.
- pip-audit 2.10.1 com requirements.txt: nenhuma vulnerabilidade conhecida nos 5 pacotes resolvidos naquela consulta (pytest 9.1.1, pluggy 1.7.0, colorama 0.4.6, iniconfig 2.3.1 e pygments 2.21.0). O resultado depende da data e da base consultada; não abrange automaticamente Python/Tcl/Tk ou dependências não declaradas.
- Auditoria estática e de dependências em ambiente isolado Python 3.12; tentativa no 3.15 exigiu compilação de PyYAML e foi abandonada sem instalar compilador.

## Testes e cobertura

Validação final no Windows/Python 3.15.0: **195 testes passaram, sem ignorados**. coverage 7.16.2 mediu **95% combinando instruções e ramificações** no pacote gerador_senhas. core.py e forca.py atingiram 100% na medição. Isso não significa 100% de correção.

A medição é do processo pytest e não agrega subprocessos. Por isso __main__.py aparece sem cobertura e parte da impressão da CLI não é contabilizada, embora esses fluxos sejam exercitados pelos testes de subprocesso. Não foram criados testes artificiais apenas para elevar o percentual.

| Área | Cobertura comportamental |
| --- | --- |
| Núcleo | 15 combinações, tamanhos mínimo/padrão/máximo, tipos e valores inválidos, candidata rejeitada e fonte indisponível |
| Avaliação | Contagem independente, fórmulas conhecidas, quatro classes e limites, taxas, tempos extremos, NaN/infinito/negativos |
| CLI | Script/módulo, flags, ajuda, saída simples/relatório, erros sem senha e execução sem Tkinter |
| GUI | Widgets reais, todas as combinações e quatro classes, máscara, limpeza de estado, fonte indisponível e janela |
| Inicialização | Tkinter ausente, ausência de display, erro interno não ocultado e encerramento normal |

Teste adicional em Python 3.12: a suíte intermediária de 194 casos teve 193 aprovados e 1 ignorado por falha de init.tcl da distribuição local. O subconjunto GUI confirmou essa limitação (31 aprovados, 1 ignorado). Não se declara validação completa nesse ambiente; o último teste de independência da CLI foi adicionado depois. Não houve execução em Linux/macOS ou Python 3.10.

## Reproduzir a revisão

No ambiente principal:

```shell
python -m pip install -r requirements.txt
python -m pip check
python -m pytest -q
python -m pip install coverage==7.16.2
python -m coverage run --branch --source=gerador_senhas -m pytest -q
python -m coverage report -m
```

Em ambiente separado com Python 3.12 e pacotes compatíveis:

```shell
python -m pip install bandit==1.9.4 pip-audit==2.10.1
python -m bandit -r gerador_senhas gerador.py interface.py
python -m pip_audit -r requirements.txt
```

Os comandos de auditoria de dependências precisam de rede. A aplicação não precisa. Os relatórios temporários e ambientes ficam em .venv, ignorada pelo Git.

## Limitações e próximos passos

Prioridades: CI em múltiplos sistemas/versões; testes visuais em diferentes DPI e leitores de tela; revisão periódica das dependências e do runtime; diagnóstico de falhas de saída/encoding em terminais incomuns. Não há teste de intrusão, análise formal da fonte do sistema, benchmark de hardware nem auditoria completa do histórico de segredos. O tratamento de erros conhecidos é adequado ao MVP; falhas inesperadas e ambiente comprometido continuam fora dessa garantia.
