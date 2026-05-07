import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.graph_modeling import GraphTopographyEngine

def main():
    print("Iniciando Fase 2: Modelado Topografico y Friccion...")
    
    engine = GraphTopographyEngine()
    
    try:
        print("1. Cargando datos base...")
        engine.load_base_data()
        
        print("2. Muestreando DEM con correccion de proyeccion WGS84...")
        engine.inject_elevation()
        
        print("3. Calculando Factor de Esfuerzo (Tobler's Hiking Function)...")
        engine.calculate_effort_factor()
        
        print("4. Calculando umbrales de colapso por tsunami...")
        engine.calculate_flood_thresholds()
        
        print("5. Exportando red unificada 3D...")
        edges_out, nodes_out = engine.export_topological_graph()
        
        print(f"\n[Exito] Red recalibrada generada:\n -> {edges_out}\n -> {nodes_out}")
        
    except Exception as e:
        print(f"\n[Error] Ocurrio un problema en el modelado: {e}")

if __name__ == "__main__":
    main()