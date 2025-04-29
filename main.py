
import time #para calcular en ms
import math #cuentas de mayor complejidad
import heapq #para manejar colas de prioridad
from collections import deque #para ayudar a manejar colas

# Laberintos como lista de listas
MAZES = {
    "maze1": [
        list("###############"),
        list("#E  # # #     #"),
        list("### ###       #"),
        list("##  # # ###   #"),
        list("# #           #"),
        list("# # #         #"),
        list("# # ## # #    #"),
        list("## #          #"),
        list("# ##         S#"),
        list("###############")
    ],
    "maze2": [
        list("####################"),
        list("#E    #  ##   # # ##"),
        list("## #  # # #    # ###"),
        list("#    #     #   #####"),
        list("#      # ##     #  #"),
        list("### #    ###  # #  #"),
        list("#   #  ### #       #"),
        list("#     ##        #  #"),
        list("#  #  #    ###     #"),
        list("# #    # # # ##    #"),
        list("#   #     ##    #  #"),
        list("#   #    #         #"),
        list("#  ##  #   ## #   ##"),
        list("#   ## #  # # #   ##"),
        list("# #   # #          #"),
        list("# #  #      #  #   #"),
        list("#    #       # #   #"),
        list("##  ##  ## ## #   ##"),
        list("## ##     #        #"),
        list("#  ###   # #      ##"),
        list("#    #  #   ##   # #"),
        list("####      # #      #"),
        list("#  # #  #  ## ## ###"),
        list("####   # #  #    #S#"),
        list("####################")
    ],
    "maze3": [
        list("##########"),
        list("#E    # ##"),
        list("# #  #  ##"),
        list("# #   ## #"),
        list("#     ## #"),
        list("#   ##   #"),
        list("#  #    ##"),
        list("#    #   #"),
        list("###  ###S#"),
        list("##########")
    ]
}

# FUNCIONES AUXILIARES

# Para determinar la posicion de un determinado elemento("#", "E", "S", " ", ".")
def encontrar_posicion(lab, simbolo):
    for y, fila in enumerate(lab):
        for x, sim in enumerate(fila):
            if sim == simbolo: # si el elemento que queremos buscar coincide, devuelve su posicion
                return (x, y)
    return None

# para separar caminos posibles de caminos sin final
def es_transitable(lab, pos):
    x, y = pos
    return 0 <= y < len(lab) and 0 <= x < len(lab[0]) and lab[y][x] != '#' # "len(lab)" refiere a la lognitud. en este caso a la cantidad de caracteres, para asegurar que tanto filas como columnas se generen bien colocadas

# funcion para generar las posibles posiciones
def vecinos(lab, pos):
    x, y = pos
    for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]: # arriba, derecha, abajo, izquierda
        nuevo = (x + dx, y + dy) # siguiente posicion
        if es_transitable(lab, nuevo):
            yield nuevo  # usamos yield para no perder la información actual (ya que esta función a diferencia de return, al devolver el valor de "nuevo" pausa la funcion en vez de terminarla


# funcion auxiliar a reconstruir_solucion
def encontrar(nodo, visitados):
    for i, v in enumerate(visitados):
        if v["nodo"] == nodo:
            return i
    return None

# funcion sacada del pseudocodigo del pdf de la actividad
def reconstruir_solucion(meta, visitados, lab):
    solucion = []
    actual = meta
    while actual is not None:
        index = encontrar(actual, visitados)
        if index is None:
            break
        solucion.append(actual)
        actual = visitados[index]["padre"]
    solucion.reverse()
    inicio = encontrar_posicion(lab, 'E')
    return solucion if solucion and solucion[0] == inicio else []

# funcion para mostrar el laberinto correctamente
def imprimir_laberinto(lab):
    for fila in lab:
        print(''.join(fila))

# funcion para señalar las casillas pisadas
def marcar_camino(lab, camino):
    lab_copia = [fila.copy() for fila in lab] #genero una copia para rellenarlo con el camino
    for x, y in camino:
        if lab_copia[y][x] not in ('E', 'S'): #si no se trata de entrada o salida marco casilla
            lab_copia[y][x] = '.'
    return lab_copia

#ALGORITMOS DE BUSQUEDA NO INFORMADA

#sacado del pseudocodigo de moodle
def bfs(lab):
    t0 = time.perf_counter_ns()
    inicio = encontrar_posicion(lab, 'E')
    objetivo = encontrar_posicion(lab, 'S')

    cola = deque([inicio])
    visitados = [{"nodo": inicio, "padre": None}]
    explorados = set([inicio])
    nodos_expandidos = 0
    max_frontera = 1

    while cola:
        max_frontera = max(max_frontera, len(cola))
        actual = cola.popleft()
        nodos_expandidos += 1

        if actual == objetivo:
            t1 = time.perf_counter_ns()
            return reconstruir_solucion(objetivo, visitados, lab), nodos_expandidos, max_frontera, t1 - t0

        for vecino in vecinos(lab, actual):
            if vecino not in explorados:
                explorados.add(vecino)
                visitados.append({"nodo": vecino, "padre": actual})
                cola.append(vecino)

    return None, nodos_expandidos, max_frontera, time.perf_counter_ns() - t0

#sacado del pseudocodigo de moodle
def dfs(lab):
    t0 = time.perf_counter_ns()
    inicio = encontrar_posicion(lab, 'E')
    objetivo = encontrar_posicion(lab, 'S')

    pila = [inicio]
    visitados = [{"nodo": inicio, "padre": None}]
    explorados = set([inicio])
    nodos_expandidos = 0
    max_frontera = 1

    while pila:
        max_frontera = max(max_frontera, len(pila))
        actual = pila.pop()
        nodos_expandidos += 1

        if actual == objetivo:
            t1 = time.perf_counter_ns()
            return reconstruir_solucion(objetivo, visitados, lab), nodos_expandidos, max_frontera, t1 - t0

        for vecino in vecinos(lab, actual):
            if vecino not in explorados:
                explorados.add(vecino)
                visitados.append({"nodo": vecino, "padre": actual})
                pila.append(vecino)

    return None, nodos_expandidos, max_frontera, time.perf_counter_ns() - t0

# ALGORITMOS DE BUSQUEDA INFORMADA

#sacado del pseudocodigo de moodle
def gbf(lab, heur):
    t0 = time.perf_counter_ns()
    inicio = encontrar_posicion(lab, 'E')
    objetivo = encontrar_posicion(lab, 'S')

    abiertos = []
    heapq.heappush(abiertos, (heur(inicio, objetivo), inicio))
    visitados = [{"nodo": inicio, "padre": None}]
    cerrados = set([inicio])
    nodos_expandidos = 0
    max_frontera = 1

    while abiertos:
        max_frontera = max(max_frontera, len(abiertos))
        _, actual = heapq.heappop(abiertos)
        nodos_expandidos += 1

        if actual == objetivo:
            t1 = time.perf_counter_ns()
            return reconstruir_solucion(objetivo, visitados, lab), nodos_expandidos, max_frontera, t1 - t0

        for hijo in vecinos(lab, actual):
            if hijo not in cerrados:
                visitados.append({"nodo": hijo, "padre": actual})
                heapq.heappush(abiertos, (heur(hijo, objetivo), hijo))
                cerrados.add(hijo)

    return None, nodos_expandidos, max_frontera, time.perf_counter_ns() - t0


#sacado del pseudocodigo de moodle
def A_ESTRELLA(lab, heuristica):
    inicio = encontrar_posicion(lab, 'E')
    objetivo = encontrar_posicion(lab, 'S')

    Est_abiertos = []
    heapq.heappush(Est_abiertos, (0, inicio))
    g_score = {inicio: 0}
    padres = {inicio: None}
    nodos_expandidos = 0
    max_frontera = 1
    Est_cerrados = set()

    t0 = time.perf_counter_ns()

    while Est_abiertos:
        max_frontera = max(max_frontera, len(Est_abiertos))
        f_actual, actual = heapq.heappop(Est_abiertos)

        if actual in Est_cerrados:
            continue
        Est_cerrados.add(actual)
        nodos_expandidos += 1

        if actual == objetivo:
            t1 = time.perf_counter_ns()
            camino = reconstruir_solucion(objetivo, [{"nodo": k, "padre": v} for k, v in padres.items()], lab)
            return camino, nodos_expandidos, max_frontera, t1 - t0

        for hijo in vecinos(lab, actual):
            tentative_g = g_score[actual] + 1
            if hijo in Est_cerrados and tentative_g >= g_score.get(hijo, float('inf')):
                continue

            if tentative_g < g_score.get(hijo, float('inf')):
                g_score[hijo] = tentative_g
                padres[hijo] = actual
                f = tentative_g + heuristica(hijo, objetivo)
                heapq.heappush(Est_abiertos, (f, hijo))

    return None, nodos_expandidos, max_frontera, time.perf_counter_ns() - t0

# HEURISTICAS

#sacado del pseudocodigo de moodle
def heuristica_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


#sacado del pseudocodigo de moodle
def heuristica_euclidea(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

#consiste en la suma de las heuristicas anteriores dividida entre 2
def heuristica_propuesta(a, b):
    return (heuristica_manhattan(a, b) + heuristica_euclidea(a, b)) / 2

# MAIN
def main():
    # diccionario de algoritmos
    algoritmos = {
        'BUSQUEDA ANCHURA': (bfs, 'COLA'), #al final de cada funcion del diccionario ponemos el tipo de ED que usa
        'BUSQUEDA PROFUNDIDAD': (dfs, 'PILA'),
        'GREEDY MANHATTAN': (lambda lab: gbf(lab, heuristica_manhattan), 'COLA DE PRIORIDAD'), #usamos "lambda lab:" en todos para generar una funcion temporal de lab para cada heuristica en los algoritmos informados
        'GREEDY EUCLIDEA': (lambda lab: gbf(lab, heuristica_euclidea), 'COLA DE PRIORIDAD'),
        'GREEDY PROPUESTA': (lambda lab: gbf(lab, heuristica_propuesta), 'COLA DE PRIORIDAD'),
        'A* MANHATTAN': (lambda lab: A_ESTRELLA(lab, heuristica_manhattan), 'LISTA'),
        'A* EUCLIDEA': (lambda lab: A_ESTRELLA(lab, heuristica_euclidea), 'LISTA'),
        'A* PROPUESTA': (lambda lab: A_ESTRELLA(lab, heuristica_propuesta), 'LISTA'),
    }

    for nombre, grid in MAZES.items(): # usamos ".items()" para acceder al diccionario MAZES donde están almacenados los laberintos (listas de listas)
        lab = [fila.copy() for fila in grid]
        print(f"== LABERINTO: {nombre} ==")

        print("Laberinto original:")
        imprimir_laberinto(grid)

        for nom_alg, (func, estructura) in algoritmos.items(): # aqui ".items()" tiene la misma función pero accede al diccionario algoritmos
            lab_copia = [fila.copy() for fila in grid]
            try:
                camino, nodos, maxf, tiempo_ns = func(lab_copia)
                if camino:
                    print(f"\n--- {nom_alg} ---")
                    print(f"Camino recorrido (x,y): {camino}")
                    print(f"Nodos expandidos: {nodos}")
                    print(f"Tiempo: {tiempo_ns/1e6:.2f} ms") # para transformas a milisegundos
                    print(f"Máximo en frontera: {maxf}")
                    print(f"Profundidad: {len(camino)-1}")

                    lab_resuelto = marcar_camino(lab_copia, camino)
                    print("\nLaberinto resuelto:")
                    imprimir_laberinto(lab_resuelto)
                else:
                    print(f"\n--- {nom_alg} ---")
                    print("No se encontró camino.")
            except Exception as e:
                print(f"\n--- {nom_alg} ---")
                print(f"Error: {str(e)}") #imprime el tipo de error, esto es de chatgpt pero lo puse por si al transcribir los pseudocodigos me daba un error raro, poder resolverlo rápido

if __name__ == "__main__":
    main()
