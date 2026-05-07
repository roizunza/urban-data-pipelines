import osmnx as ox
import geopandas as gpd
import os
import requests
from dotenv import load_dotenv

load_dotenv()

class KamakuraExtractor:
    def __init__(self, north, south, east, west, output_dir="data/processed", raw_dir="data/raw"):
        self.bbox = (north, south, east, west)
        self.output_dir = output_dir
        self.raw_dir = raw_dir
        self.crs_projected = "EPSG:32654"
        
        for directory in [self.output_dir, self.raw_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)

    def extract_pedestrian_network(self):
        G = ox.graph_from_bbox(
            bbox=self.bbox,
            network_type='walk',
            simplify=True
        )
        return ox.project_graph(G, to_crs=self.crs_projected)

    def extract_infrastructure(self, tags):
        gdf = ox.features_from_bbox(
            bbox=self.bbox,
            tags=tags
        )
        if not gdf.empty:
            gdf_proj = gdf.to_crs(self.crs_projected)
            return gdf_proj[gdf_proj.geometry.type.isin(['Polygon', 'MultiPolygon', 'Point'])]
        return gpd.GeoDataFrame()

    def download_dem_opentopography(self, filename="kamakura_srtm.tif"):
        api_key = os.getenv("OPENTOPOGRAPHY_API_KEY")
        if not api_key:
            raise ValueError("La API key no se encontro en el archivo .env local.")

        
        filepath = os.path.join(self.raw_dir, filename)
        west, south, east, north = self.bbox
        
        url = (
            f"https://portal.opentopography.org/API/globaldem?"
            f"demtype=SRTMGL1&south={south}&north={north}&west={west}&east={east}"
            f"&outputFormat=GTiff&API_Key={api_key}"
        )
        
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        else:
            raise Exception(f"Falla en la descarga. Status Code: {response.status_code}")
            
        return filepath
    
    def export_to_geojson(self, graph, official_gdf, emergent_gdf):
        """
        Exporta los datos a formato GeoJSON filtrando estrictamente las columnas 
        de la red vial segun la estructura solicitada.
        """
        # 1. Exportar la red vial (Nodos y Aristas)
        nodes, edges = ox.graph_to_gdfs(graph)
        
        # OSMnx guarda u, v, key como un MultiIndex. Los pasamos a columnas normales.
        edges = edges.reset_index()
        
        # Filtrado estricto de columnas. Agregamos 'length' porque es vital para grafos.
        columnas_deseadas = ['u', 'v', 'key', 'highway', 'lanes', 'maxspeed', 'length', 'geometry']
        
        # Validacion: si OSM no tiene 'lanes' o 'maxspeed' en esta zona, creamos la columna nula
        for col in columnas_deseadas:
            if col not in edges.columns:
                edges[col] = None
                
        edges_filtrado = edges[columnas_deseadas].copy()
        
        # Exportar Aristas
        edges_path = os.path.join(self.output_dir, "kamakura_edges.geojson")
        edges_filtrado.to_file(edges_path, driver="GeoJSON")
        
        # Exportar Nodos (Mantenemos coordenadas e ID)
        nodes_clean = nodes[['y', 'x', 'geometry']].reset_index()
        nodes_path = os.path.join(self.output_dir, "kamakura_nodes.geojson")
        nodes_clean.to_file(nodes_path, driver="GeoJSON")
        
        # 2. Exportar Infraestructura Oficial (Escuelas y Centros Comunitarios)
        if not official_gdf.empty:
            official_path = os.path.join(self.output_dir, "kamakura_official_shelters.geojson")
            # Filtramos metadata basura
            cols = [c for c in ['amenity', 'name', 'geometry'] if c in official_gdf.columns]
            official_gdf[cols].to_file(official_path, driver="GeoJSON")
            
        # 3. Exportar Templos (Infraestructura Latente)
        if not emergent_gdf.empty:
            emergent_path = os.path.join(self.output_dir, "kamakura_emergent_temples.geojson")
            cols = [c for c in ['amenity', 'religion', 'name', 'geometry'] if c in emergent_gdf.columns]
            emergent_gdf[cols].to_file(emergent_path, driver="GeoJSON")
            
        return edges_path, nodes_path