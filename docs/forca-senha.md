# Metodologia da avaliação de senha

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
