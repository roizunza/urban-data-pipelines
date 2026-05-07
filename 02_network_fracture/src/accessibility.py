import os
import geopandas as gpd
import networkx as nx
import osmnx as ox
import pandas as pd
import numpy as np

class AccessibilityEngine:
    """
    Motor algoritmico para simular la degradacion de la red (tsunami) 
    y calcular el esfuerzo de evacuacion a refugios usando Dijkstra.
    """
    def __init__(self, processed_dir="data/processed"):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.processed_dir = os.path.join(base_dir, processed_dir)
        self.nodes = None
        self.edges = None
        self.official_nodes = []
        self.emergent_nodes = []

    def load_scenario_data(self):
        """
        Carga los datos topologicos y los puntos de interes (POIs).
        """
        self.nodes = gpd.read_file(os.path.join(self.processed_dir, "kamakura_nodes_3d.geojson"))
        self.edges = gpd.read_file(os.path.join(self.processed_dir, "kamakura_edges_3d.geojson"))
        official_gdf = gpd.read_file(os.path.join(self.processed_dir, "kamakura_official_shelters.geojson"))
        emergent_gdf = gpd.read_file(os.path.join(self.processed_dir, "kamakura_emergent_temples.geojson"))

        self.G_base = nx.MultiDiGraph()
        
        # Inyeccion del CRS: Le pasamos la proyeccion espacial (UTM) al grafo
        self.G_base.graph['crs'] = self.nodes.crs
        
        for _, row in self.nodes.iterrows():
            self.G_base.add_node(row['osmid'], x=row['x'], y=row['y'])
            
        for _, row in self.edges.iterrows():
            self.G_base.add_edge(
                row['u'], row['v'], key=row.get('key', 0),
                effort_time_s=row['effort_time_s'],
                inundation_threshold=row['inundation_threshold']
            )

        self.official_nodes = ox.distance.nearest_nodes(
            self.G_base, X=official_gdf.geometry.centroid.x, Y=official_gdf.geometry.centroid.y
        )
        self.emergent_nodes = ox.distance.nearest_nodes(
            self.G_base, X=emergent_gdf.geometry.centroid.x, Y=emergent_gdf.geometry.centroid.y
        )

    def _calculate_evacuation_times(self, graph, target_nodes):
        """
        Calcula el shortest path desde todos los nodos hacia el target mas cercano.
        Filtra los refugios que hayan quedado sumergidos en el escenario actual.
        """
        G_rev = graph.reverse()
        
        # El parche logico: solo buscar rutas hacia refugios que sobrevivieron a la inundacion
        valid_targets = [n for n in target_nodes if n in G_rev.nodes]
        
        # Si el tsunami fue tan masivo que inundo TODOS los refugios, no hay rutas
        if not valid_targets:
            return {} 
            
        try:
            times = nx.multi_source_dijkstra_path_length(G_rev, valid_targets, weight='effort_time_s')
            return times
        except Exception:
            return {}

    def simulate_tsunami_scenarios(self, water_levels=[0, 10, 20, 30]):
        """
        Itera sobre las cotas de inundacion, elimina aristas sumergidas y 
        calcula la accesibilidad para infraestructura oficial y latente.
        """
        for level in water_levels:
            print(f"   -> Simulando tsunami a {level} metros...")
            
            valid_edges = [
                (u, v, k) for u, v, k, data in self.G_base.edges(keys=True, data=True)
                if data['inundation_threshold'] > level
            ]
            
            G_scenario = self.G_base.edge_subgraph(valid_edges).copy()
            
            times_official = self._calculate_evacuation_times(G_scenario, self.official_nodes)
            times_emergent = self._calculate_evacuation_times(G_scenario, self.emergent_nodes)
            
            col_off = f'time_off_{level}m'
            col_emg = f'time_emg_{level}m'
            
            self.nodes[col_off] = self.nodes['osmid'].map(times_official)
            self.nodes[col_emg] = self.nodes['osmid'].map(times_emergent)
            
            self.nodes[f'orphan_off_{level}m'] = self.nodes[col_off].isna()
            
            self.nodes[f'saved_by_temple_{level}m'] = self.nodes[f'orphan_off_{level}m'] & ~self.nodes[col_emg].isna()

    def export_results(self, out_file="kamakura_nodes_simulated.geojson"):
        """
        Exporta los nodos con los atributos de simulacion integrados.
        """
        out_path = os.path.join(self.processed_dir, out_file)
        self.nodes.to_file(out_path, driver="GeoJSON")
        return out_path