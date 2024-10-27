# <div align="center">Lista de Exercícios - AV2</div>

## <div align="center">Alunos: Guilherme de Farias Loureiro (2214635) e Nilo José Martins Jereissati (2110887)</div>

---

Lista de exercícios para composição de notas da AV2 de Computação Paralela e Concorrente.

Esta lista de prática pode ser feita individualmente ou em dupla. Caso sejam detectados trabalhos iguais, os mesmos serão ZERADOS.

**Prazo de entrega:** 30/10/2024  
A entrega deste trabalho deve ser feita via AVA, disponibilizando o link do GitHub.

Para a realização deste trabalho, pode-se utilizar QUAISQUER LINGUAGENS DE PROGRAMAÇÃO, DESDE QUE A MESMA APRESENTE UMA ESTRUTURA PARA LIDAR COM PARALELISMO E CONCORRÊNCIA.

---

### Questão única:

A multiplicação de matrizes é uma ferramenta poderosa que permite que sistemas computacionais realizem uma ampla variedade de tarefas, desde o processamento de imagens até a tomada de decisões complexas em sistemas de inteligência artificial. Por exemplo, a multiplicação de matrizes é a base de muitos algoritmos de aprendizado de máquina, como redes neurais artificiais, que aprendem a partir de dados através de ajustes em matrizes de pesos. As matrizes são excelentes estruturas para representar dados estruturados, como imagens e gráficos. A eficiência dessa operação é fundamental para o desempenho de muitos algoritmos e aplicações.

Outro exemplo prático é a análise de redes sociais, onde os usuários podem ser representados como linhas e colunas de uma matriz. Imagine uma rede social com 5 usuários: Alice, Bob, Carol, David e Paul. A matriz de adjacência representa quem segue quem. Se Alice segue Bob, na posição (Alice, Bob) da matriz teremos um 1. Caso contrário, será 0. Considere a seguinte matriz de adjacência A como base desta análise.

|       | Alice | Bob | Carol | David | Paul |
|-------|-------|-----|-------|-------|------|
| Alice | 0     | 1   | 0     | 1     | 0    |
| Bob   | 0     | 0   | 1     | 0     | 1    |
| Carol | 1     | 0   | 0     | 1     | 0    |
| David | 0     | 1   | 0     | 0     | 1    |
| Paul  | 1     | 0   | 1     | 0     | 0    |

Com esta matriz, é possível realizar duas análises simples ao calcularmos \(A^2\):

1. **Conexões de segundo grau (amigos dos amigos):** Ao multiplicar a matriz de adjacência por ela mesma, encontramos conexões de segundo grau.
2. **Influenciadores:** A coluna que possui linhas com valores altos na matriz resultante indica usuários seguidos por muitos outros, ou seja, influenciadores.

Para exemplificar:

- **Exemplo 1:** Se o valor de \(z\) (posição Alice, Bob) for 2, isso significa que Alice pode chegar até Bob através de dois caminhos de comprimento 2: Alice -> Carol -> Bob e Alice -> David -> Bob.
- **Exemplo 2:** Um valor alto nas linhas da coluna de um usuário indica que muitos outros usuários estão conectados a ele de alguma forma, seja diretamente ou indiretamente.

### Instruções para a resolução

Considere a matriz supracitada e realize as operações de multiplicação de maneira **PARALELA**. Calcule \(A^2\) e responda:

> Ps: as questões serão respondidas baseado na saída gerada pela execução de [produto_matricial_paralelo.py](produto_matricial_paralelo.py) que se encontra no arquivo [log_execucao.txt](log_execucao.txt). Para esclarecer, a operação de \(A^2\) se refere ao caso 1.
>
> Os tempos gerados na saída podem variar levemente de execução em execução. Além disso, vale ressaltar que [produto_matricial_paralelo.py](produto_matricial_paralelo.py) foi executado em um notebook lenovo com intel core i7 e com 12 processadores.

> Resultado de \(A^2\)
>
> |       |  Alice   |  Bob   |  Carol   |  David   |  Paul   |
> |-------|----------|--------|----------|----------|---------|
> | Alice |    0     |    1   |    1     |    0     |    2    |
> | Bob   |    2     |    0   |    1     |    1     |    0    |
> | Carol |    0     |    2   |    0     |    1     |    1    |
> | David |    1     |    0   |    2     |    0     |    1    |
> | Paul  |    1     |    1   |    0     |    2     |    0    |

1. **Demonstração da matriz resultante**: Demonstre as duas pessoas com mais amigos em comum.
2. **Pessoa mais influente do grupo**: Identifique quem é.

> Resposta para os dois itens acima: Todos têm a mesma quantidade de amigos, portanto todos também são igualmente influentes.

3. **Tempos de execução de cada thread**: Calcule e demonstre o tempo que cada thread utilizou para as multiplicações. ✔️ [log_execucao.txt](log_execucao.txt)

4. **Discussão sobre o tempo total**:
   - Qual o tempo utilizado para calcular a matriz resultante?
   > Considerando o menor tempo gasto por execução com uma quantidade *x* de processadores como **O** tempo, esse foi de 0.1203 segundos.
   - Qual o tempo gasto para identificar as pessoas com mais amigos em comum e a pessoa mais influente?
   > Todos têm a mesma quantidade de amigos, portanto todos também são igualmente influentes.
   - Discuta as diferenças de tempo encontradas.
   > No caso da multiplicação paralelelizada, a execução demonstrou que não vale a pena paralelizar essa operação para uma matriz pequena como uma 5x5, contudo, isso não é verdade para uma matriz grande o suficiente, como uma 300x300.
---

