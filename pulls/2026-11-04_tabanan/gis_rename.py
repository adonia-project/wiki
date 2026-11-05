# -*- coding: utf-8 -*-
import os, shutil, io, sys
import geopandas as gpd
import pyogrio
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DASH = '\u2014'
base = r'B:\02_GIT CONNECTED\map\countries\Almuria'
north_old = os.path.join(base, 'Almuria ' + DASH + ' Pakiak')
south_old = os.path.join(base, 'Almuria ' + DASH + ' Volistraya')
north_new = os.path.join(base, 'Almuria ' + DASH + ' Tabanan')
south_new = os.path.join(base, 'Almuria ' + DASH + ' Pakiak')

# inspect current layer names
for d in [north_old, south_old]:
    f = [x for x in os.listdir(d) if x.endswith('.gpkg')][0]
    print(d.split('\\')[-1], '->', pyogrio.list_layers(os.path.join(d, f)).tolist())

# 1. North: rename folder + file + layer to Tabanan (Country field already Tabanan)
os.rename(north_old, north_new)
f_old = os.path.join(north_new, 'Almuria ' + DASH + ' Pakiak.gpkg')
f_new = os.path.join(north_new, 'Almuria ' + DASH + ' Tabanan.gpkg')
os.rename(f_old, f_new)
g = gpd.read_file(f_new)
g.to_file(f_new, layer='Almuria ' + DASH + ' Tabanan', driver='GPKG')
print('north done:', g[['Country','Area_km2']].to_string())

# 2. South: rename folder + file + layer to Pakiak, Country field -> Pakiak
os.rename(south_old, south_new)
f_old = os.path.join(south_new, 'Almuria ' + DASH + ' Volistraya.gpkg')
f_new = os.path.join(south_new, 'Almuria ' + DASH + ' Pakiak.gpkg')
os.rename(f_old, f_new)
g2 = gpd.read_file(f_new)
g2['Country'] = 'Pakiak'
g2.to_file(f_new, layer='Almuria ' + DASH + ' Pakiak', driver='GPKG')
print('south done:', g2[['Country','Area_km2']].to_string())

# verify
for d in [north_new, south_new]:
    print(d.split('\\')[-1], os.listdir(d))
    f = [x for x in os.listdir(d) if x.endswith('.gpkg')][0]
    print('  layers:', pyogrio.list_layers(os.path.join(d, f)).tolist())
    chk = gpd.read_file(os.path.join(d, f))
    print('  Country:', chk['Country'].iloc[0], '| Area:', chk['Area_km2'].iloc[0])
