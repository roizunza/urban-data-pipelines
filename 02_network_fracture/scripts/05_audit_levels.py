import os
import geopandas as gpd

def validate_hypothesis_levels():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    nodes_path = os.path.join(base_dir, "data", "processed", "kamakura_nodes_simulated.geojson")
    temples_path = os.path.join(base_dir, "data", "processed", "kamakura_temples_wgs84.geojson")

    print("Cargando y procesando matriz espacial...")
    nodes_gdf = gpd.read_file(nodes_path)
    temples_gdf = gpd.read_file(temples_path)

    # Unificar proyeccion a UTM para mediciones precisas en metros
    if nodes_gdf.crs is None or nodes_gdf.crs.to_epsg() != 32654:
        nodes_gdf.set_crs(epsg=32654, inplace=True, allow_override=True)
    
    temples_proj = temples_gdf.to_crs(epsg=32654)

    # Heredar la elevacion del nodo mas cercano a cada templo
    temples_with_elev = gpd.sjoin_nearest(
        temples_proj, 
        nodes_gdf[['elevation', 'geometry']], 
        how='left', 
        distance_col='dist_to_node'
    )
    
    # Limpiar duplicados en caso de empates en distancia
    temples_with_elev = temples_with_elev[~temples_with_elev.index.duplicated(keep='first')]

    total_nodes = len(nodes_gdf)
    total_temples = len(temples_gdf)

    print("\n==================================================")
    print("      AUDITORIA DE RESILIENCIA POR NIVELES")
    print("==================================================")
    print(f"Total de infraestructura vial (nodos): {total_nodes}")
    print(f"Total de templos emergentes mapeados: {total_temples}")

    niveles = [10, 20, 30]

    for nivel in niveles:
        print(f"\n[ ESCENARIO: TSUNAMI DE {nivel} METROS ]")
        
        # Filtros de supervivencia
        templos_sobrevivientes = len(temples_with_elev[temples_with_elev['elevation'] > nivel])
        nodos_huerfanos = len(nodes_gdf[nodes_gdf[f'orphan_off_{nivel}m'] == True])
        nodos_rescatados = len(nodes_gdf[nodes_gdf[f'saved_by_temple_{nivel}m'] == True])
        
        print(f"Templos operativos (por encima del agua): {templos_sobrevivientes}")
        print(f"Calles vulnerables (aisladas de refugios oficiales): {nodos_huerfanos}")
        print(f"Calles rescatadas por templos operativos: {nodos_rescatados}")
        
        if nodos_huerfanos > 0:
            tasa_rescate = (nodos_rescatados / nodos_huerfanos) * 100
            print(f"Eficiencia de red emergente: {tasa_rescate:.2f}% de rescate.")
            
    print("\n==================================================\n")

if __name__ == "__main__":
    validate_hypothesis_levels()