import subprocess
import shutil
from multiprocessing import Pool
from adm.utils import logging, cwd

logger = logging.getLogger(__name__)

inputs = cwd / '../../admin-boundaries/outputs/edge-matched/humanitarian/intl'
area = cwd / '../../population-statistics/data/area.csv'
outputs = cwd / '../tmp'


def export(geom, l):
    input = inputs / f'adm4_{geom}.gpkg.zip'
    output = outputs / f'adm{l}_{geom}.geojsonl.gz'
    output.unlink(missing_ok=True)
    sql_if = "SELECT * FROM adm0_lines"
    sql_else = ' '.join([
        f"SELECT g.*, CAST(c.area_{l} AS REAL) AS area",
        f"FROM adm{l}_{geom} g",
        f"LEFT JOIN '{area}'.area c ON g.adm0_id = c.adm0_id"
    ])
    sql = sql_if if geom == 'lines' and l == 0 else sql_else
    subprocess.run([
        'ogr2ogr',
        '-mapFieldType', 'Date=String',
        '-f', 'GeoJSONSeq',
        '-dialect', 'INDIRECT_SQLITE',
        '-sql', sql,
        '/vsigzip/' + str(output),
        '/vsizip/' + str(input),
    ])
    logger.info(f'adm{l}_{geom}')


def main():
    outputs.mkdir(parents=True, exist_ok=True)
    results = []
    pool = Pool()
    for geom in ['points', 'lines']:
        for l in range(0, 3):
            result = pool.apply_async(export, args=[geom, l])
            results.append(result)
    pool.close()
    pool.join()
    for result in results:
        result.get()
    logger.info('finished')


def cleanup():
    shutil.rmtree(outputs, ignore_errors=True)
