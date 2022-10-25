import subprocess
from adm.utils import logging, cwd, MAX_ZOOM

logger = logging.getLogger(__name__)

inputs = cwd / '../tmp'
outputs = inputs


def adm_points(l):
    subprocess.run([
        'tippecanoe',
        f'--layer=adm{l}_points',
        f'--maximum-zoom={MAX_ZOOM}',
        '--drop-rate=1',
        '--read-parallel',
        '--no-tile-size-limit',
        '--force',
        f'--include=adm{l}_name',
        '--include=status_cd',
        '--include=area',
        f'--output={outputs}/adm{l}_points.mbtiles',
        f'{inputs}/adm{l}_points.geojsonl.gz',
    ])
    logger.info(f'adm{l}_points')


def adm_lines(l):
    subprocess.run([
        'tippecanoe',
        f'--layer=adm{l}_lines',
        f'--maximum-zoom={MAX_ZOOM}',
        '--simplify-only-low-zooms',
        '--no-simplification-of-shared-nodes',
        '--read-parallel',
        '--no-tile-size-limit',
        '--force',
        '--include=rank',
        '--include=area',
        f'--output={outputs}/adm{l}_lines.mbtiles',
        f'{inputs}/adm{l}_lines.geojsonl.gz',
    ])
    logger.info(f'adm{l}_lines')


def main():
    outputs.mkdir(parents=True, exist_ok=True)
    for l in range(0, 3):
        adm_points(l)
        adm_lines(l)
    logger.info('finished')
