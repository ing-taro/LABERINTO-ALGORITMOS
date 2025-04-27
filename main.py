import time
import math
from collections import deque

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

# Funciones auxiliares
def encontrar_posicion(laberinto, simbolo):
    for y, fila in enumerate(laberinto):
        for x, ch in enumerate(fila):
            if ch == simbolo:
                return (x, y)
    return None

def es_transitable(laberinto, pos):
    x, y = pos
    return 0 <= y < len(laberinto) and 0 <= x < len(laberinto[0]) and laberinto[y][x] != '#'

def vecinos(laberinto, pos):
    x, y = pos
    for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
        nuevo = (x + dx, y + dy)
        if es_transitable(laberinto, nuevo):
            yield nuevo

def reconstruir_camino(padres, inicio, objetivo):
    camino = []
    nodo = objetivo
    while nodo != inicio:
        camino.append(nodo)
        nodo = padres.get(nodo)
        if nodo is None:
            return []
    camino.append(inicio)
    camino.reverse()
    return camino

def imprimir_laberinto(laberinto):
    for fila in laberinto:
        print(''.join(fila))

def marcar_camino(laberinto, camino):
    # Marca el camino en una copia del laberinto con '.'
    lab = [fila.copy() for fila in laberinto]
    for x, y in camino:
        if lab[y][x] not in ('E', 'S'):
            lab[y][x] = '.'
    return lab

# Algoritmos de búsqueda sin clase
def bfs(lab):
    t0 = time.perf_counter_ns()
    inicio = encontrar_posicion(lab, 'E')
    objetivo = encontrar_posicion(lab, 'S')
    frontera = deque([inicio])
    visitados = {inicio}
    padres = {}
    max_frontera = 1
    nodos_expandidos = 0
    while frontera:
        max_frontera = max(max_frontera, len(frontera))
        nodo = frontera.popleft()
        nodos_expandidos += 1
        if nodo == objetivo:
            t1 = time.perf_counter_ns()
            return reconstruir_camino(padres, inicio, objetivo), nodos_expandidos, max_frontera, t1 - t0
        for v in vecinos(lab, nodo):
            if v not in visitados:
                visitados.add(v)
                padres[v] = nodo
                frontera.append(v)
    return None, nodos_expandidos, max_frontera, time.perf_counter_ns() - t0

def dfs(lab):
    t0 = time.perf_counter_ns()
    inicio = encontrar_posicion(lab, 'E')
    objetivo = encontrar_posicion(lab, 'S')
    frontera = [inicio]
    visitados = {inicio}
    padres = {}
    max_frontera = 1
    nodos_expandidos = 0
    while frontera:
        max_frontera = max(max_frontera, len(frontera))
        nodo = frontera.pop()
        nodos_expandidos += 1
        if nodo == objetivo:
            t1 = time.perf_counter_ns()
            return reconstruir_camino(padres, inicio, objetivo), nodos_expandidos, max_frontera, t1 - t0
        for v in vecinos(lab, nodo):
            if v not in visitados:
                visitados.add(v)
                padres[v] = nodo
                frontera.append(v)
    return None, nodos_expandidos, max_frontera, time.perf_counter_ns() - t0

# Heurísticas
def heuristica_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def heuristica_euclid(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def heuristica_propuesta(a, b):
    return (heuristica_manhattan(a, b) + heuristica_euclid(a, b)) / 2

def greedy_best_first_sin_heap(lab, heur):
    t0 = time.perf_counter_ns()
    inicio = encontrar_posicion(lab, 'E')
    objetivo = encontrar_posicion(lab, 'S')
    abierto = [(heur(inicio, objetivo), inicio)]
    visitados = {inicio}
    padres = {}
    max_frontera = 1
    nodos_expandidos = 0
    while abierto:
        max_frontera = max(max_frontera, len(abierto))
        h_val, nodo = min(abierto, key=lambda x: x[0])
        abierto.remove((h_val, nodo))
        nodos_expandidos += 1
        if nodo == objetivo:
            t1 = time.perf_counter_ns()
            return reconstruir_camino(padres, inicio, objetivo), nodos_expandidos, max_frontera, t1 - t0
        for v in vecinos(lab, nodo):
            if v not in visitados:
                visitados.add(v)
                padres[v] = nodo
                abierto.append((heur(v, objetivo), v))
    return None, nodos_expandidos, max_frontera, time.perf_counter_ns() - t0

def a_star_sin_heap(lab, heur):
    t0 = time.perf_counter_ns()
    inicio = encontrar_posicion(lab, 'E')
    objetivo = encontrar_posicion(lab, 'S')
    abierto = [(heur(inicio, objetivo), 0, inicio)]
    g_score = {inicio: 0}
    padres = {}
    max_frontera = 1
    nodos_expandidos = 0
    while abierto:
        max_frontera = max(max_frontera, len(abierto))
        f, g, nodo = min(abierto, key=lambda x: x[0])
        abierto.remove((f, g, nodo))
        nodos_expandidos += 1
        if nodo == objetivo:
            t1 = time.perf_counter_ns()
            return reconstruir_camino(padres, inicio, objetivo), nodos_expandidos, max_frontera, t1 - t0
        for v in vecinos(lab, nodo):
            tentative_g = g + 1
            if tentative_g < g_score.get(v, float('inf')):
                padres[v] = nodo
                g_score[v] = tentative_g
                abierto.append((tentative_g + heur(v, objetivo), tentative_g, v))
    return None, nodos_expandidos, max_frontera, time.perf_counter_ns() - t0


def main():
    # Tu código de la función main aquí
    algoritmos = {
        'BFS': bfs,
        'DFS': dfs,
        'Greedy-MH': lambda lab: greedy_best_first_sin_heap(lab, heuristica_manhattan),
        'A*-MH': lambda lab: a_star_sin_heap(lab, heuristica_manhattan),
        'A*-EU': lambda lab: a_star_sin_heap(lab, heuristica_euclid),
        'A*-PROP': lambda lab: a_star_sin_heap(lab, heuristica_propuesta),
    }

    print("Iniciando resolución de laberintos...")

    for nombre, grid in MAZES.items():
        print(f"\n==============================")
        print(f"== LABERINTO: {nombre.upper()} ==")
        print(f"==============================\n")

        print("Laberinto original:")
        imprimir_laberinto(grid)

        for nom_alg, func in algoritmos.items():
            print(f"\n--- Resultado con {nom_alg} ---")
            lab_copia = [fila.copy() for fila in grid]
            try:
                camino, nodos, maxf, tiempo_ns = func(lab_copia)
                if camino:
                    lab_resuelto = marcar_camino(grid, camino)
                    imprimir_laberinto(lab_resuelto)
                    print(f"\n✔ Camino encontrado ({len(camino)} pasos)")
                else:
                    print("✘ No se encontró camino.")
                    continue
                print(f"Nodos expandidos:    {nodos}")
                print(f"Máxima frontera:     {maxf}")
                print(f"Tiempo de ejecución: {tiempo_ns} ns")
            except Exception as e:
                print(f"Error al ejecutar {nom_alg}: {str(e)}")
                continue


if __name__ == "__main__":
    main()
