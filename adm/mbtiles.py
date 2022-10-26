import json
import subprocess
from adm.utils import logging, cwd, MAX_ZOOM

logger = logging.getLogger(__name__)

inputs = cwd / '../tmp'
outputs = inputs


def adm_points(l, name, z_min, z_max):
    subprocess.run([
        'tippecanoe',
        '--quiet',
        f'--layer=adm{l}_points',
        f'--minimum-zoom={z_min}',
        f'--maximum-zoom={z_max}',
        '--drop-rate=1',
        '--read-parallel',
        '--no-tile-size-limit',
        '--force',
        f'--include=adm{l}_name',
        '--include=status_cd',
        '--include=area',
        f'--output={outputs}/{name}.mbtiles',
        f'{inputs}/{name}.geojsonl.gz',
    ])
    logger.info(name)


def adm_lines(l, name, z_min, z_max):
    subprocess.run([
        'tippecanoe',
        '--quiet',
        f'--layer=adm{l}_lines',
        f'--minimum-zoom={z_min}',
        f'--maximum-zoom={z_max}',
        '--simplify-only-low-zooms',
        '--no-simplification-of-shared-nodes',
        '--read-parallel',
        '--no-tile-size-limit',
        '--force',
        '--include=rank',
        '--include=area',
        f'--output={outputs}/{name}.mbtiles',
        f'{inputs}/{name}.geojsonl.gz',
    ])
    logger.info(name)


def get_zooms(layer):
    z_min = 0
    z_max = MAX_ZOOM
    if 'minzoom' in layer:
        z_min = layer['minzoom']
    if 'maxzoom' in layer and layer['maxzoom'] < MAX_ZOOM:
        z_max = layer['maxzoom']
    return layer['id'], z_min, z_max


def get_layers(geom, l):
    with open(cwd / f'../src/layers/adm{l}-{geom}.json') as f:
        data = json.load(f)
    return map(get_zooms, data)


def main():
    outputs.mkdir(parents=True, exist_ok=True)
    for geom in ['points', 'lines']:
        func = adm_lines if geom == 'lines' else adm_points
        func(0, f'adm0_{geom}', 0, MAX_ZOOM)
        for l in range(1, 3):
            for layer, z_min, z_max in get_layers(geom, l):
                func(l, f'adm{l}_{geom}_{layer}', z_min, z_max)
    logger.info('finished')
