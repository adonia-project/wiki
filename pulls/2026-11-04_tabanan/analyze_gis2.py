# -*- coding: utf-8 -*-
import geopandas as gpd
from shapely.ops import unary_union
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DASH = '\u2014'
base = r'B:\02_GIT CONNECTED\map\countries\Almuria'
t = gpd.read_file(base + '\\Almuria ' + DASH + ' Pakiak\\Almuria ' + DASH + ' Pakiak.gpkg')
v = gpd.read_file(base + '\\Almuria ' + DASH + ' Volistraya\\Almuria ' + DASH + ' Volistraya.gpkg')
print('Tabanan:', t[['Country','Area_km2']].to_string())
print('Volistraya:', v[['Country','Area_km2']].to_string())

tg = unary_union(t.geometry.to_crs(6933))
vg = unary_union(v.geometry.to_crs(6933))
print('Tabanan eq area km2: %.0f' % (tg.area/1e6))
print('Volistraya eq area km2: %.0f' % (vg.area/1e6))

t4 = unary_union(t.to_crs(4326).geometry)
v4 = unary_union(v.to_crs(4326).geometry)
print('touches:', t4.touches(v4), '| intersects:', t4.intersects(v4))
inter = t4.intersection(v4)
print('border geom:', inter.geom_type, '| length (deg):', round(inter.length, 3))

geom = t.geometry.iloc[0]
parts = list(geom.geoms) if geom.geom_type == 'MultiPolygon' else [geom]
print('n parts:', len(parts))
for i, p in enumerate(sorted(parts, key=lambda x: -x.area)):
    c = p.centroid
    print('part %d: %,.0f km2  (%.2fE, %.2fN)' % (i, p.area/1e6, c.x, c.y) if False else 'part %d: %.0f km2  (%.2fE, %.2fN)' % (i, p.area/1e6, c.x, c.y))

# coastline in Robinson meters
trob = unary_union(t.geometry)
cl = sum(g.exterior.length for g in trob.geoms)/1000 if trob.geom_type == 'MultiPolygon' else trob.exterior.length/1000
print('coastline km: %.0f' % cl)
print('Tabanan bounds 4326:', t.to_crs(4326).total_bounds)
print('Volistraya bounds 4326:', v.to_crs(4326).total_bounds)
