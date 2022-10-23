import time
import subprocess
from multiprocessing import Pool
from admin.utils import logging, cwd, MAX_ZOOM

logger = logging.getLogger(__name__)

inputs = cwd / '../tmp'
outputs = cwd / '../tmp'


def adm_points(l):
    subprocess.run([
        'tippecanoe',
        '--quiet',
        f'--layer=adm{l}_points',
        f'--maximum-zoom={MAX_ZOOM}',
        '--drop-rate=1',
        '--read-parallel',
        '--no-tile-size-limit',
        '--force',
        f'--include=adm{l}_name',
        '--include=area',
        f'--output={outputs}/adm{l}_points.mbtiles',
        f'{inputs}/adm{l}_points.geojsonl.gz',
    ])
    logger.info(f'adm{l}_points')


def adm_lines(l):
    subprocess.run([
        'tippecanoe',
        '--quiet',
        f'--layer=adm{l}_lines',
        f'--maximum-zoom={MAX_ZOOM}',
        '--simplify-only-low-zooms',
        '--no-simplification-of-shared-nodes',
        '--read-parallel',
        '--no-tile-size-limit',
        '--force',
        '--include=rank' if l == 0 else '--include=area',
        f'--output={outputs}/adm{l}_lines.mbtiles',
        f'{inputs}/adm{l}_lines.geojsonl.gz',
    ])
    logger.info(f'adm{l}_lines')


def main():
    outputs.mkdir(parents=True, exist_ok=True)
    results = []
    pool = Pool()
    for l in range(0, 5):
        for func in [adm_points, adm_lines]:
            result = pool.apply_async(func, args=[l])
            results.append(result)
    pool.close()
    pool.join()
    for result in results:
        result.get()
    logger.info('finished')
