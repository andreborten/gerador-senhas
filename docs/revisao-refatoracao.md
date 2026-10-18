# Revisão técnica e refatoração — v1.3.2

Data: 18/10/2026. Complementa a [revisão anterior](revisao-tecnica.md); os resultados antigos são históricos. Objetivo: DRY, SRP, nomes semânticos, funções coesas, validação e preservação de comportamento.

## Achados comprovados e correções

| Achado | Reprodução e impacto | Correção |
| --- | --- | --- |
| classificar aceitava inteiros, mas convertia implicitamente para float via isfinite | `classificar(10**1000)` causava OverflowError; negativos enormes também não seguiam o contrato ValueError | Inteiros são tratados como finitos, sem conversão; teste de finitude aplicado apenas a float |
| Contexto Decimal do chamador podia alterar resultado ou provocar erro | Precisão reduzida e trap Inexact faziam avaliação/formatação falhar | Contexto Decimal novo, precisão 28 e política própria em cada operação |
| CLI misturava declaração dos argumentos, fluxo e relatório | Função principal concentrava responsabilidades | criar_parser e formatar_relatorio separados; main coordena entrada, geração e saída |
| GUI tinha métodos longos e conversão aninhada | Montagem e atualização difíceis de revisar | Métodos para configuração, resultado, leitura de tamanho e exibição; nomes explícitos |
| Contagem matemática estava embutida na avaliação | Intenção da fórmula menos visível | _contar_combinacoes extrai a operação sobre grupos já validados |

As falhas numéricas afetam uso direto/reutilização da API, não são evidência de senhas inseguras geradas com a configuração padrão. Quatro novos testes falharam na versão anterior e passaram após a correção.

## DRY, SRP e contrato preservado

A validação central continua em selecionar_grupos. Não foi duplicada dentro das novas funções privadas; elas recebem dados já validados. Geração criptográfica, limite de comprimento, grupos permitidos, classes, taxas, assinaturas públicas existentes, textos de saída e códigos de erro permanecem compatíveis para entradas anteriormente válidas em contexto padrão.

A CLI separa parser, coordenação e relatório. A GUI separa controles, resultado e apresentação; regras criptográficas permanecem fora dos widgets. Nomes como configuracao, _ler_tamanho e _exibir_resultado explicitam intenção. Não foram criadas hierarquias ou dependências adicionais. A limitação de SOLID documentada anteriormente continua válida: OCP/DIP são parciais, LSP não é aplicável ao desenho atual.

## Evidência de regressão

- Baseline antes de alterar produção: 195 testes passaram.
- Quatro casos reproduziram falhas numéricas antes da correção.
- Dois testes de contrato verificam exatamente texto, linhas, stderr e código de saída da CLI, com senha de exemplo controlada e opção --somente-senha.
- Resultado final: **201 testes passaram, sem ignorados**, no Windows/Python 3.15.0.
- coverage 7.16.2: **98% combinando instruções e ramificações** do pacote. core, forca e cli: 100% na medição. Subprocessos não são agregados; algumas entradas de módulo ficam fora da contagem.
- Bandit 1.9.4: nenhum achado no código de execução após a refatoração.
- Um erro de renomeação introduzido durante extração de widgets foi detectado pela suíte e corrigido antes da entrega.

Não se promete ausência absoluta de regressões: a evidência cobre o ambiente e os cenários executados. A auditoria de dependências da revisão anterior não foi repetida, pois requirements.txt não mudou; seu resultado conserva a data e o alcance originais.

## Onde ainda faltam validações ou testes

| Área | Situação / risco residual |
| --- | --- |
| Saída do terminal | Encoding restritivo, stdout fechado e pipe interrompido não têm tratamento completo; podem gerar erro de saída |
| Ambiente de instalação | Iniciador depende de Python disponível e caminhos locais; falta teste automatizado de lançamento real em instalação limpa |
| Contexto de GUI | Tk/display ausente tem diagnóstico; DPI, telas pequenas e leitores de tela não foram validados em matriz |
| Intervalo completo | Grupos são cobertos nas 15 combinações; comprimentos intermediários não são exercitados exaustivamente em todas elas |
| Compatibilidade declarada | Python 3.10+ é requisito de sintaxe; testes completos somente em Windows/3.15, com evidência parcial anterior em 3.12 |

Não foi adicionado tratamento genérico de Exception para esconder esses riscos. As entradas normais de tamanho/grupos, tipos incorretos, NaN, infinito e valores negativos já têm validação e testes. Valores negativos e enormes de entropia agora respeitam seu contrato.

## Cinco testes prioritários para a próxima release

Os itens abaixo são um plano, não testes já concluídos. A ordem considera impacto e lacuna de evidência.

| Prioridade | Teste / cenário | Critério de aceite | Por que priorizar |
| --- | --- | --- | --- |
| 1 | Saída CLI interrompida e encoding restritivo | Subprocesso com pipe fechado e saída ASCII termina com status definido, sem traceback ou senha em diagnóstico; --somente-senha mantém saída ASCII válida | Automação pode quebrar mesmo com geração correta; requer definir e implementar política de erro de saída |
| 2 | Instalação limpa e iniciar.bat real | Em Windows isolado, caminhos com espaços/acentos e cwd diferente: GUI abre sem argumentos; flags abrem CLI; falta de Python/Tk produz orientação e não fechamento silencioso | Abertura por duplo clique já foi problema real e ainda depende do ambiente |
| 3 | Matriz de versões e sistemas | Executar núcleo/CLI em Python mínimo declarado e versão de referência, Windows/Linux/macOS; GUI com display real/virtual quando disponível, registrando skips | Sustenta a compatibilidade anunciada no README |
| 4 | Propriedades para todo comprimento permitido | Para 8–256 e 15 combinações, verificar comprimento, alfabeto, presença de grupos, contagem positiva e estimativas finitas; testes determinísticos de rejeição separados | Cobre intermediários sem usar ausência de colisões como teste de segurança |
| 5 | GUI em DPI elevado, tela pequena e teclado | Controles, erros e ressalvas acessíveis em tamanhos/DPI definidos; tabulação, Enter e máscara corretos; leitor de tela recebe rótulos | A geometria local atual não prova acessibilidade e apresentação em outras máquinas |

## Checklist do README

| Pergunta | Resultado |
| --- | --- |
| O que o projeto resolve? | Seção explícita sobre geração conforme critérios e compreensão da força estimada; não é gerenciador de senhas |
| Como instalar? | Git, Python, venv, dependências de teste e Tcl/Tk documentados |
| Como executar? | GUI por iniciar.bat/interface.py e CLI com exemplos, flags e códigos de erro |
| Como rodar testes? | python -m pytest -q, resultado atual e comportamento sem ambiente gráfico |
| Quais são os limites? | Taxas hipotéticas, exposição local, ausência de web/persistência, compatibilidade parcial e limitações de terminal/DPI |

Reprodução: comandos de testes e cobertura da [revisão técnica](revisao-tecnica.md). Decisões atualizadas em [decisoes.md](decisoes.md).
