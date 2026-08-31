# Guide: Creating Balboa Comarca Locator Maps

This guide explains how to generate SVG locator maps for Balboan comarcas, highlighting one comarca in red within the full country context.

## Prerequisites

- Python 3 with `fiona`, `shapely`, `pyproj` installed (system python3, NOT the wiki venv)
- GIS data in `/Users/shubhamnaik/Developer/adonia-gis/`:
  - `Adonia Countries.gdb` — geodatabase with `adonia_countries` layer (CRS ESRI:54030)
  - Province shapefiles: `Balboa.shp`, `Tramuntana.shp`, `Jala.shp`, `Migjorn.shp`, `Nurra.shp` (all EPSG:4326)

## Output

SVG files saved to `articles/Countries/Balboa/Maps/`, named `<Comarca Name> in Balboa.svg`.

## Color Scheme

| Element | Color | Notes |
|---|---|---|
| Water background | `#C7E7FB` | Ocean/sea |
| Neighbor countries | `#DFDFDF` | Fill for Tapuya, sinchew, Amiera, Areza |
| Balboa land | `#FDFBEA` | Fill for all Balboan land |
| Political borders | `#656565` | Country, province, and comarca borders |
| Coastlines | `#1278AB` | Land-water boundaries (drawn on top to overwrite political border color) |
| Highlighted comarca | `#C12838` | Fill for the target comarca |

## SVG Structure (drawing order, bottom to top)

1. Water background rect
2. Neighbors group — Tapuya, sinchew, Amiera (fill `#DFDFDF`, stroke `#656565` 0.3)
3. Balboa land — union of all province comarcas (fill `#FDFBEA`, stroke `#656565` 0.3)
4. Comarca borders — all 106 comarcas across 5 provinces (fill none, stroke `#656565` 0.2)
5. Areza enclave — international city within Balboa (fill `#DFDFDF`, stroke `#656565` 0.3)
6. Focus comarca — highlighted target (fill `#C12838`, stroke `#656565` 0.3)
7. Coastline — boundary of total land union, drawn LAST (fill none, stroke `#1278AB` 0.3)

The coastline is drawn last so it overwrites the `#656565` political border color on all shorelines, leaving only interior political borders visible as grey.

## Key Implementation Details

- **Country geometries** are in CRS ESRI:54030 and must be reprojected to EPSG:4326 (WGS84) using `pyproj.Transformer.from_crs('ESRI:54030', 'EPSG:4326', always_xy=True)`.
- **Balboa land fill** is derived from the union of all province shapefile comarcas (NOT the Countries geodatabase), ensuring island comarcas have land background. The geodatabase may not include all small islands.
- **Total land union** (for coastline extraction) = Balboa + Tapuya + sinchew + Amiera + Areza. The `.boundary` of this union gives all land-water edges.
- **Zero-area comarcas** (degenerate geometries with area < 0.0001 sq degrees) are filtered out. These appear as "Unknown" entries in Jala province shapefiles.
- **Full country geometries** are drawn unclipped — the SVG viewBox handles cropping. Do NOT clip geometries to the map bounds.
- **Map bounds** use 8% padding around Balboa's bounding box.
- **SVG dimensions**: 400 x 600 pixels, viewBox `0 0 400 600`.
- **Projection**: Simple affine transform mapping lon/lat to SVG x/y with y-axis flipped. Scale is uniform (min of x/y scale), centered with offsets.

## How to Create a New Comarca Locator Map

1. Copy the generation script (see below)
2. Change the `target_name` variable to the comarca you want to highlight
3. Change the `output_path` to match the naming convention
4. Run with `python3`
5. Open the SVG in Chrome to review: `open -a "Google Chrome" <path>`
6. Commit and upload to the wiki

### Finding the Target Comarca

The script searches for the target by name substring. Comarca names are stored in the `Comarca`, `NAME`, or `Name` property field of each province shapefile. To list all comarca names:

```python
import fiona
gis_dir = '/Users/shubhamnaik/Developer/adonia-gis'
for fname in ['Balboa.shp', 'Tramuntana.shp', 'Jala.shp', 'Migjorn.shp', 'Nurra.shp']:
    with fiona.open(f'{gis_dir}/{fname}') as src:
        for f in src:
            name = f['properties'].get('Comarca') or f['properties'].get('NAME') or f['properties'].get('Name')
            print(f"{fname.replace('.shp','')}: {name} (id={f['properties'].get('id')})")
```

### Province Shapefile Comarca Counts

| Province | Count | Notes |
|---|---|---|
| Jala | 35 (22 after removing 13 zero-area) | Includes many island comarcas |
| Tramuntana | 27 | |
| Nurra | 25 | |
| Migjorn | 19 | |
| Balboa (Estret) | 13 | |
| **Total** | 106 | After filtering zero-area |

## Generation Script Template

```python
import fiona
from shapely.geometry import shape
from shapely.ops import unary_union
from shapely.ops import transform
import pyproj

gis_dir = '/Users/shubhamnaik/Developer/adonia-gis'

# ─── Config ────────────────────────────────────────────────────────────────────
TARGET_NAME = "La Serra de Llevant"  # Change this
OUTPUT_PATH = f'articles/Countries/Balboa/Maps/{TARGET_NAME} in Balboa.svg'

# ─── Load country geometries ────────────────────────────────────────────────────
transformer_to_wgs84 = pyproj.Transformer.from_crs('ESRI:54030', 'EPSG:4326', always_xy=True)

with fiona.open(f'{gis_dir}/Adonia Countries.gdb', layer='adonia_countries') as src:
    by_country = {}
    for f in src:
        c = f['properties'].get('Country', '')
        if not c or c == '0':
            continue
        try:
            geom = shape(f['geometry'])
            geom_wgs84 = transform(transformer_to_wgs84.transform, geom)
            by_country.setdefault(c, []).append(geom_wgs84)
        except:
            pass

tapuya_union = unary_union(by_country['Tapuya'])
sinchew_union = unary_union(by_country['sinchew'])
amiera_union = unary_union(by_country['Amiera'])
areza_union = unary_union(by_country['Areza'])

# ─── Load comarcas (filter zero-area) ──────────────────────────────────────────
all_comarcas = []
target_geom = None

for fname in ['Balboa.shp', 'Tramuntana.shp', 'Jala.shp', 'Migjorn.shp', 'Nurra.shp']:
    with fiona.open(f'{gis_dir}/{fname}') as src:
        for f in src:
            geom = shape(f['geometry'])
            if geom.area < 0.0001:
                continue
            props = f['properties']
            name = props.get('Comarca') or props.get('NAME') or props.get('Name') or 'Unknown'
            all_comarcas.append({'geometry': geom, 'name': name})
            if TARGET_NAME.lower() in str(name).lower():
                target_geom = geom

if target_geom is None:
    raise ValueError(f"Comarca '{TARGET_NAME}' not found")

# ─── Build unions ──────────────────────────────────────────────────────────────
balboa_land_union = unary_union([c['geometry'] for c in all_comarcas])
total_land_union = unary_union([
    balboa_land_union, tapuya_union, sinchew_union, amiera_union, areza_union
])

minx, miny, maxx, maxy = balboa_land_union.bounds
pad_x = (maxx - minx) * 0.08
pad_y = (maxy - miny) * 0.08
map_minx, map_miny = minx - pad_x, miny - pad_y
map_maxx, map_maxy = maxx + pad_x, maxy + pad_y

# ─── Project to SVG coordinates ────────────────────────────────────────────────
svg_width, svg_height = 400, 600
map_width, map_height = map_maxx - map_minx, map_maxy - map_miny
scale = min(svg_width / map_width, svg_height / map_height)
offset_x = (svg_width - map_width * scale) / 2
offset_y = (svg_height - map_height * scale) / 2

def project_geom(geom):
    def tx(x, y, z=None):
        return (offset_x + (x - map_minx) * scale, svg_height - offset_y - (y - map_miny) * scale)
    return transform(tx, geom)

def polygon_to_path(geom):
    coords = geom.exterior.coords
    path = f"M{coords[0][0]:.2f},{coords[0][1]:.2f}"
    for x, y in coords[1:]:
        path += f" L{x:.2f},{y:.2f}"
    path += " Z"
    for interior in geom.interiors:
        coords = interior.coords
        path += f" M{coords[0][0]:.2f},{coords[0][1]:.2f}"
        for x, y in coords[1:]:
            path += f" L{x:.2f},{y:.2f}"
        path += " Z"
    return path

def linestring_to_path(geom):
    coords = list(geom.coords)
    path = f"M{coords[0][0]:.2f},{coords[0][1]:.2f}"
    for x, y in coords[1:]:
        path += f" L{x:.2f},{y:.2f}"
    return path

def geom_to_path(geom):
    if geom.geom_type == 'Polygon':
        return polygon_to_path(geom)
    elif geom.geom_type == 'MultiPolygon':
        return " ".join(polygon_to_path(p) for p in geom.geoms)
    elif geom.geom_type == 'LineString':
        return linestring_to_path(geom)
    elif geom.geom_type == 'MultiLineString':
        return " ".join(linestring_to_path(ls) for ls in geom.geoms)
    elif geom.geom_type == 'GeometryCollection':
        return " ".join(geom_to_path(g) for g in geom.geoms if geom_to_path(g))
    return ""

# ─── Project all geometries ────────────────────────────────────────────────────
neighbor_paths = [geom_to_path(project_geom(u)) for u in [tapuya_union, sinchew_union, amiera_union]]
neighbor_paths = [p for p in neighbor_paths if p]

balboa_path = geom_to_path(project_geom(balboa_land_union))
comarca_paths = [geom_to_path(project_geom(c['geometry'])) for c in all_comarcas]
comarca_paths = [p for p in comarca_paths if p]
areza_path = geom_to_path(project_geom(areza_union))
target_path = geom_to_path(project_geom(target_geom))
coastline_path = geom_to_path(project_geom(total_land_union).boundary)

# ─── Colors ────────────────────────────────────────────────────────────────────
WATER, NEIGHBOR_FILL, BALBOA_FILL = "#C7E7FB", "#DFDFDF", "#FDFBEA"
BORDER, COASTLINE = "#656565", "#1278AB"
FOCUS_FILL, FOCUS_STROKE = "#C12838", "#656565"

# ─── Build SVG ──────────────────────────────────────────────────────────────────
svg = [f'<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">',
    f'  <rect x="0" y="0" width="{svg_width}" height="{svg_height}" fill="{WATER}"/>']

svg.append('  <g id="neighbors">')
for p in neighbor_paths:
    svg.append(f'    <path d="{p}" fill="{NEIGHBOR_FILL}" stroke="{BORDER}" stroke-width="0.3"/>')
svg.append('  </g>')

svg.append('  <g id="balboa">')
svg.append(f'    <path d="{balboa_path}" fill="{BALBOA_FILL}" stroke="{BORDER}" stroke-width="0.3"/>')
svg.append('  </g>')

svg.append('  <g id="comarcas">')
for p in comarca_paths:
    svg.append(f'    <path d="{p}" fill="none" stroke="{BORDER}" stroke-width="0.2"/>')
svg.append('  </g>')

if areza_path:
    svg.append('  <g id="areza">')
    svg.append(f'    <path d="{areza_path}" fill="{NEIGHBOR_FILL}" stroke="{BORDER}" stroke-width="0.3"/>')
    svg.append('  </g>')

svg.append('  <g id="focus">')
svg.append(f'    <path d="{target_path}" fill="{FOCUS_FILL}" stroke="{FOCUS_STROKE}" stroke-width="0.3"/>')
svg.append('  </g>')

if coastline_path:
    svg.append('  <g id="coastline">')
    svg.append(f'    <path d="{coastline_path}" fill="none" stroke="{COASTLINE}" stroke-width="0.3"/>')
    svg.append('  </g>')

svg.append('</svg>')
svg_content = "\n".join(svg)

with open(OUTPUT_PATH, 'w') as f:
    f.write(svg_content)
print(f"Written: {OUTPUT_PATH} ({len(svg_content):,} bytes)")
```

## Uploading to the Wiki

After committing the SVG, upload it to the TALOD Miraheze wiki:

```bash
cd /Users/shubhamnaik/Developer/wiki
uv run python upload_image.py "articles/Countries/Balboa/Maps/<filename>.svg" --description "Locator map of <comarca> comarca in <province> province, Balboa"
```

Then reference it in the comarca article's infobox via the `image_map` field.
