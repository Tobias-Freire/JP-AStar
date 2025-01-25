import csv
import math
from collections import defaultdict
import heapq


def heuristic(node1, node2, nodes):
    """
    Compute the estimated cost (Haversine distance) between two nodes.
    """
    return haversine(
        nodes[node1]['latitude'], nodes[node1]['longitude'],
        nodes[node2]['latitude'], nodes[node2]['longitude']
    )

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the distance (in km) between two geographical points using the Haversine formula.
    """
    R = 6371  # Radius of the Earth in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def a_star(graph, nodes, start_id, goal_id):
    """
    A* algorithm implementation to find the shortest path between two geographical points.
    Returns the path as a list of (latitude, longitude) tuples.
    """
    # Priority queue to store (f_cost, node)
    open_set = []
    heapq.heappush(open_set, (0, start_id))

    # Cost tracking
    g_cost = {node: float('inf') for node in nodes}
    g_cost[start_id] = 0

    # Path tracking
    came_from = {}

    while open_set:
        current_f, current = heapq.heappop(open_set)

        # Goal check
        if current == goal_id:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append((nodes[current]['latitude'], nodes[current]['longitude']))
                current = came_from[current]
            path.append((nodes[start_id]['latitude'], nodes[start_id]['longitude']))
            return path[::-1], g_cost[goal_id]

        # Explore neighbors
        for neighbor, edge_cost in graph[current]:
            # Calculate tentative g_cost (actual path cost)
            tentative_g_cost = g_cost[current] + edge_cost

            # Check if this path is better than any previous one
            if tentative_g_cost < g_cost[neighbor]:
                # Update path tracking
                came_from[neighbor] = current
                g_cost[neighbor] = tentative_g_cost

                # Compute f_cost: actual path cost + heuristic estimate
                f_cost = tentative_g_cost + heuristic(neighbor, goal_id, nodes)

                # Add to open set
                heapq.heappush(open_set, (f_cost, neighbor))

    # No path found
    return None, float('inf')


def load_nodes(path: str) -> dict:
    """
    Load nodes from a CSV file. Returns a dictionary with node_id as the key
    and latitude/longitude as values.
    """
    nodes = {}
    with open(path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            nodes[row['node_id']] = {
                'latitude': float(row['latitude']),
                'longitude': float(row['longitude'])
            }
    return nodes


def load_edges(path: str) -> dict:
    """
    Load graph edges from a CSV file. Returns a defaultdict with adjacency lists.
    """
    graph = defaultdict(list)
    with open(path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            origin = row['from_node']
            destination = row['to_node']
            distance = float(row['distance'])
            graph[origin].append((destination, distance))
            graph[destination].append((origin, distance))  # Bidirectional graph
    return graph
