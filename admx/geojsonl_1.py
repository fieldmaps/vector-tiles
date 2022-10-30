import gzip
import shutil
import subprocess
from multiprocessing import Pool
from zipfile import ZipFile
from admx.utils import logging, cwd

logger = logging.getLogger(__name__)
outputs = cwd / '../tmpx'


def get_inputs(l):
    inputs_0 = cwd / '../../adm0-generator/outputs/osm/intl'
    inputs_x = cwd / '../../admin-boundaries/outputs/edge-matched/humanitarian/intl'
    return inputs_0 if l == 0 else inputs_x


def unzip(src):
    with ZipFile(src, 'r') as z:
        z.extractall(outputs)


def compress_file(output, compressed):
    compressed.unlink(missing_ok=True)
    with open(output, 'rb') as f_in:
        with gzip.open(compressed, 'wb', compresslevel=1) as f_out:
            shutil.copyfileobj(f_in, f_out)
            output.unlink()


def export(l):
    unzip(get_inputs(l) / f'adm{l}_polygons.gpkg.zip')
    input = outputs / f'adm{l}_polygons.gpkg'
    output = outputs / f'adm{l}_polygons.geojsonl'
    output.unlink(missing_ok=True)
    compressed = outputs / f'adm{l}_polygons.geojsonl.gz'
    area = cwd / f'../../population-statistics/data/area_{l}.xlsx'
    pop = (
        cwd / f'../../population-statistics/outputs/population/humanitarian/intl/cod/adm{l}_join.xlsx')
    sql = ' '.join([
        f"SELECT a.*, b.*, c.*",
        f"FROM adm{l}_polygons a",
        f"LEFT JOIN '{area}'.area_{l} b ON a.adm{l}_id = b.adm{l}_id",
        f"LEFT JOIN '{pop}'.adm{l}_join c ON a.adm{l}_id = c.adm{l}_id",
    ])
    subprocess.run([
        'ogr2ogr',
        '-mapFieldType', 'Date=String',
        '-f', 'GeoJSONSeq',
        '-dialect', 'INDIRECT_SQLITE',
        '-sql', sql,
        output,
        input,
    ])
    input.unlink(missing_ok=True)
    compress_file(output, compressed)
    output.unlink(missing_ok=True)
    logger.info(f'adm{l}_polygons')


def main():
    outputs.mkdir(parents=True, exist_ok=True)
    results = []
    pool = Pool()
    for l in range(4, 5):
        result = pool.apply_async(export, args=[l])
        results.append(result)
    pool.close()
    pool.join()
    for result in results:
        result.get()
    logger.info('finished')


def cleanup():
    shutil.rmtree(outputs, ignore_errors=True)
