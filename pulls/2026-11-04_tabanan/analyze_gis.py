# -*- coding: utf-8 -*-
import geopandas as gpd
from shapely.ops import unary_union

base = r'B:\02_GIT CONNECTED\map\countries\Almuria'
import os
print(os.listdir(base))
tdir = os.path.join(base, 'Almuria \u2014 Pakiak')
print(os.listdir(tdir))
