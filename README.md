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

## A estrutura da linguagem

A estrutura representável pela linguagem é variada, passando por declaração de uma ou múltiplas variáveis, indo para condicionais e parando em laços de repetição, ela também possui espaço para operações ariméticas como soma e subtração, um exemplo de sintaxe aceito é o seguinte,

```txt
function prog3 ()
{
    /* Programa com erro sintatico */
    int : x, y;

    x = 0;
    y = 0;

    enquanto (x <> 10) faca
    {

        x = x + 1;
	/* este comentario nao estah errado */
        se (x > 10) entao
        {
            y=1;
        }

    }
}
```

# Especificação Detalhada

Para maiores detalhes consultar o documento pdf **"Projeto_Compiladores (2022-2)"** onde está o objetivo dado pelo nosso orientador na matéria, assim também como os diagramas e as tabelas de parser que construímos está no arquivo pdf **"Especificação Projeto Compiladores"**.

O trabalho foi inspirado no livro **"Compiladores: Princípios, Técnicas e Ferramentas"**, 2 Edição dos autores, **Alfred V. Aho, Ravi Sethi, Monica S. Lam, Jeffrey D. Ullman.**