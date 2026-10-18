# Registro de decisões técnicas

Registro consolidado em 18/10/2026. As decisões iniciais são retrospectivas: descrevem o que foi implementado e seus motivos. Estado: aceitas para o MVP. Base: [escopo](escopo-mvp.md), [MVP](mvp.md) e [revisão técnica](revisao-tecnica.md).

## ADR-001 — Python e biblioteca padrão

**Contexto:** gerar senhas localmente, com instalação simples e possibilidade de automação.

**Decisão:** Python 3.10+; argparse na CLI; Tkinter/ttk na GUI. Nenhum serviço externo, ORM, Pydantic, Click ou framework web é necessário. Tkinter vem do Python/Tcl/Tk, não de um pacote pip.

**Consequências:** execução sem dependências pip; GUI exige ambiente gráfico e Tcl/Tk. pytest é a única dependência direta em requirements.txt. Ferramentas de auditoria são opcionais e não integram a aplicação.

## ADR-002 — Fonte criptográfica e rejeição de candidatas

**Contexto:** garantir presença de todos os grupos habilitados sem introduzir viés pela composição.

**Decisão:** usar secrets.choice; sortear do alfabeto permitido e rejeitar candidatas incompletas. Não usar random, seeds fornecidas pelo usuário ou fallback inseguro quando a fonte do sistema falhar.

**Consequências:** distribuição uniforme entre senhas válidas sob as premissas da fonte; número de tentativas de geração não possui limite determinístico. Os alfabetos fixos e tamanho mínimo de 8 mantêm a rejeição prática no uso normal. Não há promessa de unicidade absoluta.

## ADR-003 — Configuração explícita e validação compartilhada

**Decisão:** manter gerar_senha com argumentos tipados; selecionar_grupos valida tamanho inteiro entre 8 e 256, booleanos reais e ao menos um grupo. bool é rejeitado como tamanho, apesar de ser subclasse de int em Python.

**Consequências:** núcleo e avaliação compartilham a validação. API levanta TypeError para tipos incorretos e ValueError para valores inválidos. CLI e GUI traduzem entradas do usuário antes de chamar o núcleo. O mínimo de 8 é compatibilidade, não recomendação de segurança.

## ADR-004 — Avaliação por espaço válido

**Decisão:** calcular N por inclusão-exclusão, entropia log2(N), classes fraca (<40), média (<60), forte (<80) e super forte (≥80 bits). Usar inteiros arbitrários e Decimal para tempos médios (N+1)/(2×taxa).

**Consequências:** respeita os grupos obrigatórios e suporta 256 caracteres. As taxas 10^6/s e 10^11/s e as classes são convenções educativas, não benchmarks ou certificações. A avaliação só vale para senhas uniformes geradas com a configuração informada, não para senhas humanas. NaN, infinito e valores negativos são rejeitados nos auxiliares de apresentação. [Premissas completas](forca-senha.md).

## ADR-005 — Separação de responsabilidades sem hierarquia artificial

**Decisão:** core.py cuida das regras e geração; forca.py da avaliação; cli.py da apresentação textual; gui.py dos widgets e estado visual; entrada_gui.py do diagnóstico de inicialização. Avaliacao é uma dataclass imutável.

**Consequências:** o núcleo não conhece interfaces; funções pequenas permitem testes isolados. A GUI foi dividida em configuração de estilo, estado, layout e eventos. Não foram criadas interfaces abstratas ou containers de injeção para funções únicas. OCP e DIP não são plenamente atendidos: políticas e funções são concretas. Se houver múltiplos provedores ou algoritmos, considerar protocolos e injeção explícita. LSP não é avaliável por falta de hierarquia de substituição. [Análise de SOLID](revisao-tecnica.md).

## ADR-006 — Privacidade e comportamento de saída

**Decisão:** nenhuma gravação de senhas, telemetria ou envio à rede. GUI mascara por padrão, limpa o resultado ao alterar critérios e volta a mascarar antes de nova geração, inclusive em erro. CLI mantém saída explícita; --somente-senha existe para scripts.

**Consequências:** terminal e redirecionamentos podem expor senhas. A máscara não cifra a memória; não há garantia de apagamento de strings. Usuário ainda pode selecionar/copiar manualmente; o programa não gerencia ou limpa a área de transferência do sistema.

## ADR-007 — Erros específicos e falha segura

**Decisão:** não capturar Exception genericamente. Erros de configuração não imprimem senha; fonte segura indisponível interrompe a geração. A CLI avalia antes de imprimir para evitar saída parcial se a avaliação rejeitar uma configuração. Os mesmos parâmetros são usados para geração e avaliação.

**Decisão de inicialização:** interface.py e python -m gerador_senhas.entrada_gui diagnosticam ausência de tkinter/_tkinter; gui.main trata TclError ao criar a janela. Outros erros de importação são propagados para não esconder defeitos internos. Recursos Tk são liberados no encerramento.

**Consequências:** códigos CLI 0 (sucesso/ajuda), 2 (argumentos inválidos), 1 (fonte indisponível); entrada GUI retorna 1 para falhas de instalação/sessão e 0 ao encerrar normalmente. Falhas inesperadas de programação ainda podem produzir traceback; não se pretende mascará-las como erros do usuário.

## ADR-008 — Testes de propriedades e de comportamento

**Decisão:** pytest para núcleo, matemática, subprocessos CLI, inicialização e widgets Tk reais. Testar todas as combinações válidas, fronteiras, rejeição determinística, falhas injetadas e contagem independente.

**Consequências:** testes não comprovam imprevisibilidade; ausência de duplicatas não é usada como prova. GUI é ignorada quando Tk/display indisponível, com motivo registrado. Cobertura é evidência auxiliar, não meta de 100%; subprocessos não são agregados na medição atual.

## ADR-009 — Auditoria sem inflar dependências

**Decisão:** Bandit para padrões suspeitos no Python de execução, pip-audit para dependências resolvidas, busca limitada por padrões de credenciais e revisão manual. coverage mede linhas e ramificações.

**Consequências:** ferramentas não são requisitos de execução. Bandit/pip-audit foram executados em ambiente separado Python 3.12 por incompatibilidade de build de PyYAML no Python 3.15 local. Auditoria consulta bases externas de vulnerabilidades e não envia senhas; o aplicativo continua offline. Ausência de achados não é garantia de segurança nem auditoria de todo o histórico Git ou do sistema operacional.

## ADR-010 — Versionamento e documentação

**Decisão:** Conventional Commits, tags preservadas e documentação rastreável. README registra evolução; escopo define aceite; decisões explicam escolhas; relatório técnico registra evidências e limitações.

**Consequências:** versões anteriores continuam reproduzíveis; documentos históricos mantêm os números de testes de cada entrega, enquanto o README apresenta a validação atual. Não há alteração retroativa das tags.
