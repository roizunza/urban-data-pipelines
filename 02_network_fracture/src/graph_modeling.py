import geopandas as gpd
import rasterio
import os
import pandas as pd
import numpy as np

class GraphTopographyEngine:
    """
    Motor para inyectar altimetria en redes espaciales, calcular friccion topografica
    y umbrales de inundacion.
    """
    def __init__(self, processed_dir="data/processed", raw_dir="data/raw"):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.processed_dir = os.path.join(base_dir, processed_dir)
        self.raw_dir = os.path.join(base_dir, raw_dir)

    def load_base_data(self, nodes_file="kamakura_nodes.geojson", edges_file="kamakura_edges.geojson", dem_file="kamakura_srtm.tif"):
        nodes_path = os.path.join(self.processed_dir, nodes_file)
        edges_path = os.path.join(self.processed_dir, edges_file)
        self.dem_path = os.path.join(self.raw_dir, dem_file)
        
        self.nodes = gpd.read_file(nodes_path)
        self.edges = gpd.read_file(edges_path)
        
    def inject_elevation(self):
        # Proyeccion temporal a WGS84 (EPSG:4326) para alinear con el DEM
        nodes_4326 = self.nodes.to_crs("EPSG:4326")
        coords = [(geom.x, geom.y) for geom in nodes_4326.geometry]
        
        with rasterio.open(self.dem_path) as src:
            elevations = []
            for val in src.sample(coords):
                z = val[0]
                # Limpiar valores anómalos del raster (nodata)
                elevations.append(z if z > -1000 else 0)
            self.nodes['elevation'] = elevations
            
        elev_dict = dict(zip(self.nodes['osmid'], self.nodes['elevation']))
        
        self.edges['elev_u'] = self.edges['u'].map(elev_dict)
        self.edges['elev_v'] = self.edges['v'].map(elev_dict)
        self.edges['min_elevation'] = self.edges[['elev_u', 'elev_v']].min(axis=1)

    def calculate_effort_factor(self):
        """
        Aplica la funcion de Tobler para calcular el tiempo de recorrido en segundos
        basado en la pendiente topografica.
        """
        dz = self.edges['elev_v'] - self.edges['elev_u']
        
        # Evitar divisiones por cero en calles sin longitud registrada
        dx = self.edges['length'].replace(0, 1)
        
        slope = dz / dx
        
        # Velocidad en km/h segun Tobler
        velocity_kmh = 6 * np.exp(-3.5 * np.abs(slope + 0.05))
        
        # Conversion a m/s (1 km/h = 1/3.6 m/s)
        velocity_ms = velocity_kmh / 3.6
        
        # Factor de esfuerzo = Tiempo requerido para cruzar la calle (segundos)
        self.edges['effort_time_s'] = self.edges['length'] / velocity_ms

    def calculate_flood_thresholds(self):
        def determine_threshold(z):
            if pd.isna(z) or z < 0: return 10
            if z < 10: return 10
            elif z < 20: return 20
            elif z < 30: return 30
            else: return 999 

        self.edges['inundation_threshold'] = self.edges['min_elevation'].apply(determine_threshold)

    def export_topological_graph(self, out_edges="kamakura_edges_3d.geojson", out_nodes="kamakura_nodes_3d.geojson"):
        edges_path = os.path.join(self.processed_dir, out_edges)
        nodes_path = os.path.join(self.processed_dir, out_nodes)
        
        self.edges.to_file(edges_path, driver="GeoJSON")
        self.nodes.to_file(nodes_path, driver="GeoJSON")
        
        return edges_path, nodes_path