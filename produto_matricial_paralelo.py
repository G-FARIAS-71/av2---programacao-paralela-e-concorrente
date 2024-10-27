import multiprocessing as mp
import timeit
import time
from casos import casos

matriz = list[list]

def calcular_elemento(A: matriz, B: matriz, i: int, j: int) -> tuple[int, int]:
    '''Função para calcular um único elemento da matriz resultante e medir o tempo de execução'''
    inicio = time.time_ns()  # Início da contagem em nanossegundos
    resultado = sum(A[i][k] * B[k][j] for k in range(len(A[0])))
    duracao = time.time_ns() - inicio  # Tempo total do cálculo em nanossegundos
    return resultado, duracao

def produto_matricial_paralelo(A: matriz, B: matriz, processadores: int = mp.cpu_count()) -> tuple[matriz, list[int]]:
    '''Função para distribuir os cálculos entre os processadores e retornar tempos de execução em nanossegundos'''
    # matriz mxn * matriz nxp = matriz mxp 
    m: int = len(A)
    p: int = len(B[0])

    # Lista de todos os elementos a serem calculados (índices i, j)
    elementos = [(i, j) for i in range(m) for j in range(p)]

    with mp.Pool(processes=processadores) as pool:
        # Paraleliza o cálculo de cada elemento da matriz resultante
        resultados = pool.starmap(calcular_elemento, [(A, B, i, j) for i, j in elementos])

    # Transformando a lista de resultados em uma matriz de dimensões mxp e extraindo tempos
    resultado_matriz = [[0] * p for _ in range(m)]
    tempos_individuais = []
    for indice, (i, j) in enumerate(elementos):
        resultado_matriz[i][j], duracao = resultados[indice]
        tempos_individuais.append(duracao)

    return resultado_matriz, tempos_individuais

def testar_caso(A: matriz, B: matriz, vezes: int = 1) -> tuple[matriz, list[float], list[list[int]]]:
    """Executa o produto matricial paralelo e retorna a matriz resultante, tempos de execução e tempos por elemento"""
    
    # Função interna para testar o produto matricial com o número de processadores
    def teste_produto(): return produto_matricial_paralelo(A, B, processadores=num_processadores)
    
    matriz_resultante = None
    tempos = []
    tempos_elementos = []
    
    # Testar multiplicação paralela com diferentes números de processadores
    for num_processadores in range(1, mp.cpu_count() + 1):
        
        matriz, tempos_individuais = teste_produto()
        
        tempos_elementos.append(tempos_individuais)
        
        tempo_execucao = timeit.timeit(teste_produto, number=vezes)  # Executa várias vezes e mede o tempo
        
        tempo_execucao /= vezes  # pega a média dos tempos
        
        # Executa a função de produto matricial para obter a matriz resultante na primeira vez
        if matriz_resultante is None:
            matriz_resultante = matriz
            
        tempos.append(tempo_execucao)
            
    return matriz_resultante, tempos, tempos_elementos

def exibir_resultados_caso(A: matriz, B: matriz, vezes: int = 1) -> None:
    """Executa um caso de teste e exibe os resultados, incluindo a matriz resultante e tempos"""
    print("Executando o produto matricial...")
    
    # Testar o caso e capturar os resultados
    matriz_resultante, tempos, tempos_elementos = testar_caso(A, B, vezes=vezes)
    
    # Exibir a matriz resultante (ou parte dela se for grande)
    print("Matriz resultante:")
    if len(matriz_resultante) <= 10 and len(matriz_resultante[0]) <= 10:
        for linha in matriz_resultante:
            print(linha)
    else:
        print(f"Matriz {len(matriz_resultante)}x{len(matriz_resultante[0])} (grande demais para exibir completamente)")

    # Exibir tempos de execução para diferentes números de processadores
    print("\nTempos de execução por número de processadores:")
    for i, tempo in enumerate(tempos, start=1):
        print(f"{i} processador(es): {tempo:.4f} segundos")

    # Exibir tempos individuais de cálculo para cada elemento (em nanossegundos)
    print("\nTempos individuais de cálculo de elementos (em nanossegundos):")
    for i, tempos_individuais in enumerate(tempos_elementos, start=1):
        print(f"Com {i} processador(es): {sum(tempos_individuais) / len(tempos_individuais):.0f} ms em média por elemento")

def main() -> None:
    """Função principal que itera sobre os casos de teste e exibe os resultados"""
    for i, (A, B) in enumerate(casos):
        print(f"\n===== Caso {i+1} =====")
        exibir_resultados_caso(A, B, vezes=5)
    
if __name__ == '__main__':
    main()