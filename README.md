# Gerador de senhas

O [diagrama Mermaid de arquitetura](docs/arquitetura.mmd) descreve a evolução
proposta. Alguns componentes ainda não estão implementados no código atual.

Programa de terminal em Python 3.10 ou superior, sem dependências externas.
Usa `secrets`, a biblioteca padrão para aleatoriedade criptográfica.

## Tecnologias e dependências

A implementação escolhida é Python com `argparse` para CLI. Click é uma
alternativa ao argparse; JavaScript com Node.js para CLI e HTML/CSS/JS para
Web são alternativas de implementação, não dependências desta versão.

O código atual usa `argparse`, `secrets` e `string`. A evolução prevista no
Mermaid pode usar `math` para estimar a força e `unittest` para testes.
Todos esses módulos pertencem à biblioteca padrão e não exigem instalação
via pip. O `requirements.txt` documenta a ausência de dependências externas.
Não há persistência de dados prevista; ORM e Pydantic não são necessários.

## Executar

```sh
python gerador.py
python gerador.py --tamanho 24
python gerador.py --tamanho 20 --sem-simbolos
```

As senhas incluem letras minúsculas, maiúsculas e números. Símbolos são
incluídos por padrão. O tamanho permitido é de 8 a 256 caracteres.
A senha é exibida no terminal; o programa não a grava em arquivos nem a
envia pela rede. Evite executar em terminais compartilhados ou com gravação.

## Git e GitHub

O repositório Git local foi iniciado na branch `main`.
Para publicar, crie um repositório vazio no GitHub e, nesta pasta, execute:

```sh
git add .
git commit -m "Inicia gerador de senhas"
git remote add origin https://github.com/SEU_USUARIO/gerador-senhas.git
git push -u origin main
```

Substitua a URL pela URL real do seu repositório. Nunca salve senhas geradas
no código, nos commits ou no README.

O `.gitignore` exclui ambientes, caches, builds, logs e arquivos comuns de
credenciais. README e diagramas em `docs/` são mantidos no versionamento.
Arquivos `.env.example` e `.env.sample` devem conter apenas valores fictícios.
As regras não detectam segredos inseridos no código nem removem arquivos já
versionados; revise `git diff --cached` antes de cada commit.

