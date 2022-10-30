import json
import subprocess
import shutil
from multiprocessing import Pool
from adm.utils import logging, cwd

logger = logging.getLogger(__name__)

inputs = cwd / '../../admin-boundaries/outputs/edge-matched/humanitarian/intl'
area = cwd / '../../population-statistics/data/area.xlsx'
outputs = cwd / '../tmp'


def export_adm0(geom):
    input = inputs / f'adm4_{geom}.gpkg.zip'
    output = outputs / f'adm0_{geom}.geojsonl.gz'
    output.unlink(missing_ok=True)
    sql_if = "SELECT * FROM adm0_lines"
    sql_else = ' '.join([
        f"SELECT a.*, b.area_0 AS area",
        f"FROM adm0_{geom} a",
        f"LEFT JOIN '{area}'.area b ON a.adm0_id = b.adm0_id",
    ])
    sql = sql_if if geom == 'lines' else sql_else
    subprocess.run([
        'ogr2ogr',
        '-mapFieldType', 'Date=String',
        '-f', 'GeoJSONSeq',
        '-dialect', 'INDIRECT_SQLITE',
        '-sql', sql,
        '/vsigzip/' + str(output),
        '/vsizip/' + str(input),
    ])
    logger.info(f'adm0_{geom}')


def export(geom, l, layer, a_min, a_max):
    input = inputs / f'adm4_{geom}.gpkg.zip'
    output = outputs / f'adm{l}_{geom}_{layer}.geojsonl.gz'
    output.unlink(missing_ok=True)
    sql = ' '.join([
        f"SELECT a.*, b.area_{l} AS area",
        f"FROM adm{l}_{geom} a",
        f"LEFT JOIN '{area}'.area b ON a.adm0_id = b.adm0_id",
        f"WHERE area <= {a_max} AND area > {a_min}",
    ])
    subprocess.run([
        'ogr2ogr',
        '-mapFieldType', 'Date=String',
        '-f', 'GeoJSONSeq',
        '-dialect', 'INDIRECT_SQLITE',
        '-sql', sql,
        '/vsigzip/' + str(output),
        '/vsizip/' + str(input),
    ])
    logger.info(f'adm{l}_{geom}_{layer}')


def get_zooms(layer):
    a_min = 0
    a_max = 1e14
    if 'filter' in layer:
        if layer['filter'][0] == 'all':
            a_max = layer['filter'][1][2]
            a_min = layer['filter'][2][2]
        if layer['filter'][0] == '>':
            a_min = layer['filter'][2]
        if layer['filter'][0] == '<=':
            a_max = layer['filter'][2]
    return layer['id'], a_min, a_max


def get_layers(geom, l):
    with open(cwd / f'../src/layers/adm{l}-{geom}.json') as f:
        data = json.load(f)
    return map(get_zooms, data)


def main():
    outputs.mkdir(parents=True, exist_ok=True)
    results = []
    pool = Pool()
    for geom in ['points', 'lines']:
        export_adm0(geom)
        for l in range(1, 3):
            for layer, a_min, a_max in get_layers(geom, l):
                args = [geom, l, layer, a_min, a_max]
                result = pool.apply_async(export, args=args)
                results.append(result)
    pool.close()
    pool.join()
    for result in results:
        result.get()
    logger.info('finished')


def cleanup():
    shutil.rmtree(outputs, ignore_errors=True)
