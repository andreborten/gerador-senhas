# Revisão de aderência ao MVP

Apresentação do produto entregue e roteiro de demonstração: [MVP](mvp.md).

Data: 18/10/2026. Escopo de referência: [escopo-mvp.md](escopo-mvp.md).

## Diagnóstico e correções

| Aspecto | Antes da revisão | Entrega revisada |
| --- | --- | --- |
| CLI Python/argparse | Implementada | Mantida com entrada por módulo e script |
| Comprimento configurável | Implementado | Mantido e validado também quanto ao tipo na API |
| Quatro grupos configuráveis | Apenas símbolos eram opcionais | Todos os quatro grupos podem ser excluídos independentemente |
| Fonte segura | secrets com rejeição | Preservada; falha testada e tratada na CLI |
| Organização | Um script sem tipagem | Pacote com núcleo e CLI separados, tipos e docstrings |
| Testes | 12 testes unittest | 144 casos pytest, incluindo as 15 combinações válidas |
| Objetivo, RF e RNF | Sem documento próprio de escopo | Documento completo com critérios de aceite |
| Mermaid | Incluía medidor de força proposto | Alinhado à implementação, com setas e erros |
| Dependências | Biblioteca padrão | Execução segue padrão; pytest fixado para testes |
| README | Documentava a versão anterior | Instalação, opções, API, testes e limites atualizados |
| Força da senha | Não implementada | Super forte, forte, média ou fraca conforme entropia do espaço válido |
| Força bruta | Não implementada | Tempos médios para taxas hipotéticas antiga (10^6/s) e moderna (10^11/s) |
| Saída para scripts | Uma linha por padrão | Relatório por padrão; `--somente-senha` mantém uma linha |

## Validação e conclusão

Executado `python -m pytest -q`: 144 testes passaram no Windows com Python 3.15.0. Os testes cobrem RF01–RF15 e verificam as propriedades dos requisitos de geração e validação. RNF03–RNF11 também dependem da inspeção do código, arquivos e documentação; não se afirma que a suíte prove segurança criptográfica.

O programa atende ao escopo principal pela alternativa Python CLI. Não é necessário entregar também uma interface web. A contribuição de IA contempla lógica, testes e interface. O documento de escopo explicita objetivo, requisitos funcionais e não funcionais, fluxo, critérios de aceite e evoluções futuras.

Limitações remanescentes são declaradas: configurações fracas continuam possíveis, saída no terminal não é mascarada, não há matriz de plataformas executada, benchmark real de hardware, persistência ou API. Nenhuma dessas funções é apresentada como implementada.

## Aceite da avaliação de força

A versão v1.2.0 implementa RF12–RF15. Os testes incluem fronteiras de 40/60/80 bits, as quatro classes via CLI, comparação da contagem com enumeração independente, fórmula de dois grupos, tempos conhecidos para oito dígitos e ausência de overflow em 256 caracteres para todas as combinações. Total: 144 casos aprovados.

As estimativas usam o tamanho e grupos da geração uniforme, incluindo as restrições de composição. Classificações e taxas são convenções ilustrativas do projeto, não garantia de segurança nem benchmark. [Metodologia completa, fórmulas e fontes](forca-senha.md). A documentação e o Mermaid agora representam essa funcionalidade como entregue.

## Incremento v1.3.0 — Interface gráfica

Implementados RF16–RF18 e RNF12–RNF13: interface Tkinter/ttk com os mesmos critérios da CLI, senha mascarada, classificação em texto/cor, estimativas e mensagens de erro locais. O resultado é limpo ao alterar opções. `iniciar.bat` abre a GUI quando executado sem argumentos. A CLI continua disponível.

Validação atual: **154 testes passaram**, incluindo 10 casos de GUI com widgets reais em Windows/Python 3.15.0/Tk 9.0. Um teste de geometria detectou inicialmente corte no rodapé; o espaçamento foi ajustado e a verificação passou. As seções anteriores preservam a revisão da versão v1.2.0. [Guia da interface](interface-grafica.md).
