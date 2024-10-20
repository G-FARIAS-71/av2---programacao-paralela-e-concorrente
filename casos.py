import random

"""
O propósito desse módulo é meramente armazenar os casos de teste para um módulo de produto matricial com programação paralela

Os casos são apresentados em uma tupla na qual, para efetuar um produto matricial de A*B, o primeiro elemento faz o papel do A e o segundo, do B
"""

matriz = list[list[int]]

caso = tuple[matriz, matriz]

# CASO 1

A: matriz = [
    [0, 1, 0, 1, 0],
    [0, 0, 1, 0, 1],
    [1, 0, 0, 1, 0],
    [0, 1, 0, 0, 1],
    [1, 0, 1, 0, 0],
]

caso1: caso = (A, A)

# CASO 2

m = 300
n = 300

A = [[random.randint(0,1) if i != j else 0 for i in range(m)] for j in range(n)] 

caso2: caso = (A,A)

# FIM DOS CASOS

casos: tuple[caso,...] = caso1, caso2

def main() -> None:
    for i, caso in enumerate(casos):
        print(f'caso{i+1} = {caso}', end='\n\n')
    
if __name__ == '__main__':
    main()