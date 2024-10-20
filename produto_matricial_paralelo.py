import multiprocessing as mp
import timeit
from casos import casos

matriz = list[list]

def calcular_elemento(A: matriz, B: matriz, i: int, j: int) -> int:
    '''Função para calcular um único elemento da matriz resultante'''
    return sum(A[i][k] * B[k][j] for k in range(len(A[0])))

def produto_matricial_paralelo(A: matriz, B: matriz, processadores: int = mp.cpu_count()) -> matriz:
    '''Função para distribuir os cálculos entre os processadores'''
    # matriz mxn * matriz nxp = matriz mxp 
    m: int = len(A)
    p: int = len(B[0])

    # Lista de todos os elementos a serem calculados (índices i, j)
    elementos = [(i, j) for i in range(m) for j in range(p)]

    with mp.Pool(processes=processadores) as pool:
        # Paraleliza o cálculo de cada elemento da matriz resultante
        resultados = pool.starmap(calcular_elemento, [(A, B, i, j) for i, j in elementos])

    # Transformando a lista de resultados em uma matriz de dimensões mxp
    resultado_matriz = [[0] * p for _ in range(m)]
    for indice, (i, j) in enumerate(elementos):
        resultado_matriz[i][j] = resultados[indice]

    return resultado_matriz

def testar_caso(A: matriz, B: matriz, vezes: int = 1) -> tuple[matriz, list[float]]:
    """Executa o produto matricial paralelo e retorna a matriz resultante e tempos de execução"""
    matriz_resultante = None
    tempos = []
    
    # Testar multiplicação paralela com diferentes números de processadores
    for num_processadores in range(1, mp.cpu_count() + 1):
        
        # Função interna para testar o produto matricial com o número de processadores
        def teste_produto(): return produto_matricial_paralelo(A, B, processadores=num_processadores)
        
        # Medir o tempo usando timeit
        tempo_execucao = timeit.timeit(teste_produto, number=vezes)  # Executa várias vezes e mede o tempo
        
        tempo_execucao /= vezes # pega a média dos tempos
        
        # Executa a função de produto matricial para obter a matriz resultante na primeira vez
        if matriz_resultante is None:
            matriz_resultante = teste_produto()
            
        tempos.append(tempo_execucao)
            
    return matriz_resultante, tempos

def exibir_resultados_caso(A: matriz, B: matriz, vezes: int = 1) -> None:
    """Executa um caso de teste e exibe os resultados, incluindo a matriz resultante e tempos"""
    print("Executando o produto matricial...")
    
    # Testar o caso e capturar os resultados
    matriz_resultante, tempos = testar_caso(A, B, vezes=vezes)
    
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

def main() -> None:
    """Função principal que itera sobre os casos de teste e exibe os resultados"""
    for i, (A, B) in enumerate(casos):
        print(f"\n===== Caso {i+1} =====")
        exibir_resultados_caso(A, B, vezes=5)
    
if __name__ == '__main__':
    main()