"""
    Script utilized to generate the CSV files for the João Pessoa city network nodes and edges.
    The generated files are used in the A* algorithm implementation.
"""

import osmnx as ox
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Set the place name
place_name = "João Pessoa, Paraíba, Brasil"

# Download the street network
G = ox.graph_from_place(place_name, network_type='allMangabeira')

# Extract nodes and edges
nodes_df, edges_df = ox.graph_to_gdfs(G)

# City geographic bounds for strict filtering
city_bounds = {
    'min_lat': -7.2, 
    'max_lat': -6.9, 
    'min_lon': -34.9, 
    'max_lon': -34.7
}

# Create a GeoDataFrame with points
geometry = [Point(xy) for xy in zip(nodes_df['x'], nodes_df['y'])]
nodes_gdf = gpd.GeoDataFrame(nodes_df, geometry=geometry, crs='EPSG:4326')

# Get the bounding box of João Pessoa
city_gdf = ox.geocode_to_gdf(place_name)
city_boundary = city_gdf.geometry.iloc[0]

# Filter nodes within city boundary and coordinates
nodes_in_city = nodes_gdf[
    nodes_gdf.geometry.within(city_boundary) & 
    (nodes_gdf['y'] >= city_bounds['min_lat']) & 
    (nodes_gdf['y'] <= city_bounds['max_lat']) & 
    (nodes_gdf['x'] >= city_bounds['min_lon']) & 
    (nodes_gdf['x'] <= city_bounds['max_lon'])
]

# Prepare nodes CSV
nodes_csv = nodes_in_city.reset_index()[['osmid', 'x', 'y']].rename(columns={
    'osmid': 'node_id', 
    'x': 'longitude', 
    'y': 'latitude'
})
nodes_csv['node_id'] = nodes_csv['node_id'].astype(str)
nodes_csv['node_id'] = 'JP_' + nodes_csv['node_id']  # Add João Pessoa prefix

# Prepare edges CSV (filtering edges with nodes in the city)
valid_nodes = set(nodes_csv['node_id'])
edges_csv = pd.DataFrame({
    'from_node': 'JP_' + edges_df.index.get_level_values(0).astype(str),
    'to_node': 'JP_' + edges_df.index.get_level_values(1).astype(str),
    'distance': edges_df['length'].values
})
edges_csv = edges_csv[
    edges_csv['from_node'].isin(valid_nodes) & 
    edges_csv['to_node'].isin(valid_nodes)
]

# Save to CSV files
nodes_csv.to_csv('joao_pessoa_nodes.csv', index=False)
edges_csv.to_csv('joao_pessoa_edges.csv', index=False)

print("CSV files generated successfully:")
print("- joao_pessoa_nodes.csv")
print("- joao_pessoa_edges.csv")
print(f"Total nodes in João Pessoa: {len(nodes_csv)}")
print(f"Total edges in João Pessoa: {len(edges_csv)}")