def copia_matriz(A):
    C = []
    for linha in A:
        copia = linha.copy()
        C.append(copia)
    return C

def dfs(grafo, deondevem, s, t):
    #Todos os vertices iniciam como não visitados
    visitados = [False] * len(grafo[0])

    #fila vazia
    fila = []

    #marque o nó fonte como visitado
    fila.append(s)
    visitados[s] = True

    #loop DFS
    while fila:
        #sai o primeiro da fila
        u = fila.pop(0)

        #encontra todos os vertices adjacentes a u
        #se um dos vertices adjacentes ainda nao foi visitado
        #marque ele como visitado e adicione na fila
        for indice, peso in enumerate(grafo[u]):
            if(visitados[indice] == False and peso > 0):
                visitados[indice] = True
                fila.append(indice)
                deondevem[indice] = u

    if(visitados[t]):
        return (True, visitados)
    else:
        return (False, visitados)

#deondevem nos dá um caminho aumentador da fonte ao sorvedouro
#vamos procurar a menor restrição desse caminho, esse será o fluxo do caminho ou sua capacidade grafo (delta)
#começando do sorvedouro

def path_flow(grafo, deondevem, s, t):
    chegada = t
    delta = float("Inf")
    while(chegada != s):
        saida = deondevem[chegada]
        delta = min(delta, grafo[saida][chegada])
        chegada = saida
    return delta

def envia_fluxo(grafo, deondevem, fluxo_caminho, s, t):
    chegada = t
    while(chegada != s):
        saida = deondevem[chegada]
        grafo[saida][chegada] -= fluxo_caminho
        grafo[chegada][saida] += fluxo_caminho
        chegada = saida
    return grafo

#Ford Fulkerson
def ff(grafo, s, t):
    #guarda o caminho encontrado pelo DFS
    deondevem = [-1] * len(grafo)

    #começa com fluxo -
    fluxo_maximo = 0

    #enquanto houver caminho aumementador no grado grafo
    while( dfs(grafo, deondevem, s, t)[0] ):

        fluxo_caminho = path_flow(grafo, deondevem, s, t)

        #adiciona o fluxo do caminho aumentador encontrado ao fluxo maximo
        fluxo_maximo += fluxo_caminho

        #envia delta unidades de fluxo pelo grafo
        grafo = envia_fluxo(grafo, deondevem, fluxo_caminho, s, t)

    return fluxo_maximo

def main():
    dim = []
    dim = input().split(" ")
    n = int(dim[0]) #numero de vertices
    m = int(dim[1]) #numero de arestas

    grafo = []

    for x in range(n):
        grafo.append([0] * (n))

    for i in range(m):
        arestas = input().split(" ")
        u = int( arestas[0] )
        v = int( arestas[1] )
        w = int( arestas[2] )
        grafo[u][v] = w
        grafo[v][u] = w

    t = n-1
    fluxo_minimo = float("Inf")
    caminho = [-1] * n
    for x in range(n-1):
        residual = copia_matriz(grafo)
        fluxo = ff(residual, x, t)
        if(fluxo < fluxo_minimo):
            visitados = [False] * n
            visitados = dfs(residual, caminho, x, t)[1]
            fluxo_minimo = fluxo

    #Quantidade de vertices em S
    print(sum(visitados))

    #Indice dos vertices em S
    s = []
    for n in range(len(visitados)):
        if(visitados[n]):
            #s.append( str(n) )
            print(n, end=" ")
    print(' '.join(s))

    #Peso do corte
    print(fluxo_minimo)

if __name__ == "__main__":
    main()
