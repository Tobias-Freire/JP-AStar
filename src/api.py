from fastapi import FastAPI, HTTPException
from src.AStar import load_nodes, load_edges, a_star
import os
import osmnx as ox

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NODES_FILE = os.path.join(BASE_DIR, "../data/joao_pessoa_nodes.csv")
EDGES_FILE = os.path.join(BASE_DIR, "../data/joao_pessoa_edges.csv")


@app.get("/")
def home():
    return {"message": "Bem-vindo à API de cálculo de rota! Use o endpoint /findPath para encontrar um caminho."}


@app.get("/findPath")
def find_path(start_loc: str, end_loc: str):
    # Address geocoding
    start_localization = ox.geocode(start_loc)
    end_localization = ox.geocode(end_loc)

    # Obtain the graph of the net around the locations
    start_graph = ox.graph_from_point(start_localization, dist=100, network_type='all')
    end_graph = ox.graph_from_point(end_localization, dist=100, network_type='all')

    # Obtain the nearest nodes to the locations
    start_node_id = f'JP_{ox.distance.nearest_nodes(start_graph, X=start_localization[1], Y=start_localization[0])}'
    end_node_id = f'JP_{ox.distance.nearest_nodes(end_graph, X=end_localization[1], Y=end_localization[0])}'

    # Load data
    try:
        nodes = load_nodes(NODES_FILE)
        edges = load_edges(EDGES_FILE)
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar os arquivos: {str(e)}")

    # Verify if the nodes exist
    if start_node_id not in nodes or end_node_id not in nodes:
        raise HTTPException(status_code=404, detail="Um ou ambos os nós fornecidos não existem nos dados carregados.")

    # Execute A* algorithm
    path, cost = a_star(edges, nodes, start_node_id, end_node_id)

    if path:
        return {"locations": [start_loc, end_loc], "locations_nodes_id": {start_localization, end_localization},"path": path, "cost": cost}
    else:
        raise HTTPException(status_code=404, detail="Não foi encontrado um caminho entre os nós fornecidos.")
