import subprocess
from admx.utils import logging, cwd, MAX_ZOOM

logger = logging.getLogger(__name__)

inputs = cwd / '../tmpx'
outputs = cwd / '../dist/data'


def adm_polygons(l):
    subprocess.run([
        'tippecanoe',
        f'--layer=adm{l}_polygons',
        f'--maximum-zoom={MAX_ZOOM}',
        '--simplify-only-low-zooms',
        '--detect-shared-borders',
        '--read-parallel',
        '--no-tile-size-limit',
        '--force',
        f'--output={outputs}/adm{l}_polygons.mbtiles',
        f'{inputs}/adm{l}_polygons.geojsonl.gz',
    ])
    logger.info(f'adm{l}_polygons')


def main():
    outputs.mkdir(parents=True, exist_ok=True)
    for l in range(0, 5):
        adm_polygons(l)
    logger.info('finished')
