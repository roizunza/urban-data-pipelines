import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.accessibility import AccessibilityEngine

def main():
    print("Iniciando Fase 3: Simulacion de Fractura y Nodos aislados...")
    
    engine = AccessibilityEngine()
    
    try:
        print("1. Cargando Grafo 3D e Infraestructura (Oficial y Latente)...")
        engine.load_scenario_data()
        
        print("2. Procesando escenarios de inundacion y esfuerzo de evacuacion...")
        engine.simulate_tsunami_scenarios(water_levels=[0, 10, 20, 30])
        
        print("3. Exportando nodos simulados...")
        out_path = engine.export_results()
        
        print(f"\n[Exito] Simulacion completada. Resultados en:\n -> {out_path}")
        
    except Exception as e:
        print(f"\n[Error] Ocurrio un problema en la simulacion: {e}")

if __name__ == "__main__":
    main()