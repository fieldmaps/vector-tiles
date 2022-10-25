import shutil
import subprocess
from multiprocessing import Pool
from admx.utils import logging, cwd

logger = logging.getLogger(__name__)
outputs = cwd / '../tmp_polygons'


def get_inputs(l):
    inputs_0 = cwd / '../../adm0-generator/outputs/osm/intl'
    inputs_x = cwd / '../../admin-boundaries/outputs/edge-matched/humanitarian/intl'
    return inputs_0 if l == 0 else inputs_x


def export(l):
    input = get_inputs(l) / f'adm{l}_polygons.gpkg.zip'
    output = outputs / f'adm{l}_polygons.geojsonl.gz'
    output.unlink(missing_ok=True)
    sql = ' '.join([f"SELECT g.*", f"FROM adm{l}_polygons g"])
    subprocess.run([
        'ogr2ogr',
        '-mapFieldType', 'Date=String',
        '-f', 'GeoJSONSeq',
        '-dialect', 'INDIRECT_SQLITE',
        '-sql', sql,
        '/vsigzip/' + str(output),
        '/vsizip/' + str(input),
    ])
    logger.info(f'adm{l}_polygons')


def main():
    outputs.mkdir(parents=True, exist_ok=True)
    results = []
    pool = Pool()
    for l in range(0, 3):
        result = pool.apply_async(export, args=[l])
        results.append(result)
    pool.close()
    pool.join()
    for result in results:
        result.get()
    logger.info('finished')


def cleanup():
    shutil.rmtree(outputs, ignore_errors=True)
