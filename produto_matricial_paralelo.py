import multiprocessing as mp
import timeit
import time
from casos import casos

matriz = list[list]

def calcular_elemento(A: matriz, B: matriz, i: int, j: int) -> int:
    '''Função para calcular um único elemento da matriz resultante'''
    return sum(A[i][k] * B[k][j] for k in range(len(A[0])))

def calcular_lote(A: matriz, B: matriz, elementos: list[tuple[int, int]]) -> tuple[list[tuple[int, int, int]], int]:
    '''Função para calcular um lote de elementos em um único processo'''
    inicio = time.time_ns()  # Início da contagem do tempo de processo em nanossegundos
    resultados = [(i, j, calcular_elemento(A, B, i, j)) for i, j in elementos]
    duracao = time.time_ns() - inicio  # Duração total do processo
    return resultados, duracao

def produto_matricial_paralelo(A: matriz, B: matriz, processadores: int = mp.cpu_count()) -> tuple[matriz, list[int]]:
    '''Distribui os cálculos entre os processadores e retorna tempos de execução de cada processo'''
    m: int = len(A)
    p: int = len(B[0])

    # Lista de todos os elementos a serem calculados (índices i, j)
    elementos = [(i, j) for i in range(m) for j in range(p)]

    # Dividir elementos entre os processos
    divisao_elementos = [elementos[i::processadores] for i in range(processadores)]

    with mp.Pool(processes=processadores) as pool:
        # Paraleliza o cálculo de cada lote e registra o tempo de cada processo
        resultados = pool.starmap(calcular_lote, [(A, B, lote) for lote in divisao_elementos])

    # Transformando a lista de resultados em uma matriz de dimensões mxp e extraindo tempos de cada processo
    resultado_matriz = [[0] * p for _ in range(m)]
    tempos_processos = []
    
    for lote_resultado, duracao in resultados:
        tempos_processos.append(duracao)
        for i, j, valor in lote_resultado:
            resultado_matriz[i][j] = valor

    return resultado_matriz, tempos_processos

def testar_caso(A: matriz, B: matriz, vezes: int = 1) -> tuple[matriz, list[float], list[list[int]]]:
    """Executa o produto matricial paralelo e retorna a matriz resultante, tempos de execução e tempos de cada processo"""
    
    # Função interna para testar o produto matricial com o número de processadores
    def teste_produto(): return produto_matricial_paralelo(A, B, processadores=num_processadores)
    
    matriz_resultante = None
    tempos = []
    tempos_processos = []
    
    # Testar multiplicação paralela com diferentes números de processadores
    for num_processadores in range(1, mp.cpu_count() + 1):
        
        # Executar uma vez para capturar tempos de execução de cada processo e matriz resultante
        matriz, tempos_processos_individuais = teste_produto()
        
        # Armazenar apenas uma vez os tempos dos processos
        tempos_processos.append(tempos_processos_individuais)
        
        # Medir tempo médio de execução usando timeit
        tempo_execucao = timeit.timeit(teste_produto, number=vezes)
        
        # Pega a média dos tempos
        tempo_execucao /= vezes
        
        # Executa a função de produto matricial para obter a matriz resultante na primeira vez
        if matriz_resultante is None:
            matriz_resultante = matriz
            
        tempos.append(tempo_execucao)
            
    return matriz_resultante, tempos, tempos_processos

def exibir_resultados_caso(A: matriz, B: matriz, vezes: int = 1) -> None:
    """Executa um caso de teste e exibe os resultados, incluindo a matriz resultante e tempos"""
    print("Executando o produto matricial...")
    
    # Testar o caso e capturar os resultados
    matriz_resultante, tempos, tempos_processos = testar_caso(A, B, vezes=vezes)
    
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

    # Exibir tempos de execução de cada processo
    print("\nTempos individuais de execução de processos (em nanossegundos):\n")
    for i, tempos_processo in enumerate(tempos_processos, start=1):
        print(f"Com {i} processador(es): média de {sum(tempos_processo) / len(tempos_processo):.0f} ns\n\n    {[f'{t} ns' for t in tempos_processo]}\n")

def main() -> None:
    """Função principal que itera sobre os casos de teste e exibe os resultados"""
    for i, (A, B) in enumerate(casos):
        print(f"\n===== Caso {i+1} =====")
        exibir_resultados_caso(A, B, vezes=5)
    
if __name__ == '__main__':
    main()