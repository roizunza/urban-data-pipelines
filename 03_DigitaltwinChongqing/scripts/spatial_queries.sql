
-- Radar Chart Data
-- Extrae los promedios de las variables de entrada comparando el Top 5% de rascacielos
-- (edificios mayores a 150m-50 niveles) contra el tejido base (menor a 6 niveles).
WITH rascacielos AS (
    SELECT 
        ROUND(AVG(poi_count_200m), 2) as avg_poi_rascacielos,
        ROUND(AVG(road_weight)::numeric, 4) as avg_road_rascacielos,
        ROUND(AVG(dist_transit_eq)::numeric, 2) as avg_dist_rascacielos
    FROM "chongqingZ_inferred_buildings"
    WHERE inferred_levels >= 50
),
base AS (
    SELECT 
        ROUND(AVG(poi_count_200m), 2) as avg_poi_base,
        ROUND(AVG(road_weight)::numeric, 4) as avg_road_base,
        ROUND(AVG(dist_transit_eq)::numeric, 2) as avg_dist_base
    FROM "chongqingZ_inferred_buildings"
    WHERE inferred_levels <= 6
),
maximos AS (
    SELECT 
        MAX(poi_count_200m) as max_poi,
        MAX(dist_transit_eq) as max_dist
    FROM "chongqingZ_inferred_buildings"
)
SELECT * FROM rascacielos CROSS JOIN base CROSS JOIN maximos;

-- ==============================================================================

-- Area Chart Data
-- Agrupa los 16,606 polígonos en rangos (bins) de 50m de distancia topográfica.
-- Permite visualizar el "Distance-Decay" sin saturar el DOM del frontend.
SELECT 
    (FLOOR(dist_transit_eq / 50) * 50) AS bin_distancia_m,
    ROUND(AVG(inferred_height_m)::numeric, 2) AS altura_promedio_m,
    MAX(inferred_height_m) AS altura_maxima_m,
    COUNT(*) AS volumen_parcelas
FROM "chongqingZ_inferred_buildings"
GROUP BY bin_distancia_m
ORDER BY bin_distancia_m;