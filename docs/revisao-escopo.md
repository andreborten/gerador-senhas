# Revisão de aderência ao MVP

Data: 18/10/2026. Escopo de referência: [escopo-mvp.md](escopo-mvp.md).

## Diagnóstico e correções

| Aspecto | Antes da revisão | Entrega revisada |
| --- | --- | --- |
| CLI Python/argparse | Implementada | Mantida com entrada por módulo e script |
| Comprimento configurável | Implementado | Mantido e validado também quanto ao tipo na API |
| Quatro grupos configuráveis | Apenas símbolos eram opcionais | Todos os quatro grupos podem ser excluídos independentemente |
| Fonte segura | secrets com rejeição | Preservada; falha testada e tratada na CLI |
| Organização | Um script sem tipagem | Pacote com núcleo e CLI separados, tipos e docstrings |
| Testes | 12 testes unittest | 96 casos pytest, incluindo as 15 combinações válidas |
| Objetivo, RF e RNF | Sem documento próprio de escopo | Documento completo com critérios de aceite |
| Mermaid | Incluía medidor de força proposto | Alinhado à implementação, com setas e erros |
| Dependências | Biblioteca padrão | Execução segue padrão; pytest fixado para testes |
| README | Documentava a versão anterior | Instalação, opções, API, testes e limites atualizados |

## Validação e conclusão

Executado `python -m pytest -q`: 96 testes passaram no Windows com Python 3.15.0. Os testes cobrem RF01–RF11 e verificam as propriedades dos requisitos de geração e validação. RNF03–RNF09 também dependem da inspeção do código, arquivos e documentação; não se afirma que a suíte prove segurança criptográfica.

O programa atende ao escopo principal pela alternativa Python CLI. Não é necessário entregar também uma interface web. A contribuição de IA contempla lógica, testes e interface. O documento de escopo explicita objetivo, requisitos funcionais e não funcionais, fluxo, critérios de aceite e evoluções futuras.

Limitações remanescentes são declaradas: configurações fracas continuam possíveis, saída no terminal não é mascarada, não há matriz de plataformas executada, indicador de força, persistência ou API. Nenhuma dessas funções é apresentada como implementada.
