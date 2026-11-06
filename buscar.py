from location_points import location
import math
import heapq

# dicionário: grafo[id] -> ponto
grafo = {p["id"]: p for p in location}


def distancia(id_a, id_b):
    """Distância em metros em linha reta (Haversine) entre dois pontos.
    Serve como heurística h(n)."""
    p1 = grafo[id_a]
    p2 = grafo[id_b]

    R = 6371000  # raio da Terra em metros
    lat1, lon1 = math.radians(p1["latitude"]), math.radians(p1["longitude"])
    lat2, lon2 = math.radians(p2["latitude"]), math.radians(p2["longitude"])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def a_estrela(inicio, destino):
    """Retorna (caminho, custo_total) ou (None, inf) se não houver caminho."""
    contador = 0  # desempate na fila de prioridade
    fila = [(distancia(inicio, destino), contador, inicio)]

    g = {inicio: 0}   # custo real do início até cada nó
    veio_de = {}      # para reconstruir o caminho
    fechados = set()

    while fila:
        _, _, atual = heapq.heappop(fila)

        if atual == destino:
            caminho = [atual]
            while atual in veio_de:
                atual = veio_de[atual]
                caminho.append(atual)
            return caminho[::-1], g[destino]

        if atual in fechados:
            continue
        fechados.add(atual)

        ponto = grafo[atual]
        for vizinho, custo_aresta in zip(ponto["destinos"], ponto["distancias"]):
            if vizinho in fechados:
                continue

            novo_g = g[atual] + custo_aresta
            if novo_g < g.get(vizinho, math.inf):
                g[vizinho] = novo_g
                veio_de[vizinho] = atual
                f = novo_g + distancia(vizinho, destino)
                contador += 1
                heapq.heappush(fila, (f, contador, vizinho))

    return None, math.inf


if __name__ == "__main__":
    inicio, destino = 1, 9
    caminho, custo = a_estrela(inicio, destino)
    print("Caminho:", " -> ".join(grafo[i]["nome"] for i in caminho))
    print("Custo (m):", custo)