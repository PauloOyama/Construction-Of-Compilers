# Projeto de Construção de Compiladores

## Como rodar o projeto 

Para rodar o projeto você primeiro terá que ter instalado a linguagem python(Até o presente momento é o Python 3.10.6), após instalado deve rodar o comando

```
pip install -r requirements.txt
```

Em todas as linguagens é necessário um arquivo com os comandos da linguagem, no nosso caso ele será arquivo *text.txt* (*pode ser mudado*) e as especificações da linguagens estão mais abaixo.

Após escrever um arquivo conforme as restrições da linguagem, é possível rodar o código utilizando o comando 

```
python -m src.main text.txt
```

**OBS. Somente fizemos a parte léxica e semântica da linguagem também chamada de etapa de *front-end*, em vista disso o programa não gerará um executável ou uma resposta equivalente ao sentido do arquivo, mas sim gerará a árvore de comandos do arquivo de acordo com a instrução da linguagem e escolha dos projetistas.**

O retorno será a árvore de comandos, caso queira ver mais especificadamente redirecione a saída para um arquivo *.txt* chamado *tree* dessa forma

```
python -m src.main text.txt > tree.txt
```


------
