# -*- coding: utf-8 -*-
import os, io, sys
import geopandas as gpd
import pyogrio
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DASH = '\u2014'
base = r'B:\02_GIT CONNECTED\map\countries\Almuria'

jobs = [
    ('Almuria ' + DASH + ' Tabanan', 'Tabanan'),
    ('Almuria ' + DASH + ' Pakiak', 'Pakiak'),
]
for folder, country in jobs:
    d = os.path.join(base, folder)
    f = os.path.join(d, folder + '.gpkg')
    tmp = f + '.tmp'
    if os.path.exists(tmp):
        os.remove(tmp)
    # read whichever layer exists (take the first listed)
    layers = pyogrio.list_layers(f)
    lname = layers[0][0]
    g = gpd.read_file(f, layer=lname)
    g['Country'] = country
    # write fresh single-layer GPKG
    g.to_file(tmp, layer=folder, driver='GPKG')
    os.remove(f)
    os.rename(tmp, f)
    # verify
    print(folder, '->', pyogrio.list_layers(f).tolist())
    chk = gpd.read_file(f)
    print('  Country:', chk['Country'].iloc[0], '| Area_km2:', chk['Area_km2'].iloc[0], '| parts:', len(list(chk.geometry.iloc[0].geoms)))
