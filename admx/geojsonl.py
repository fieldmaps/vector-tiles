import shutil
import subprocess
import pandas as pd
from multiprocessing import Pool
from psycopg import connect
from psycopg.sql import SQL, Identifier
from admx.utils import logging, cwd, DATABASE, cols_meta, get_pop_cols

logger = logging.getLogger(__name__)
outputs = cwd / '../tmpx'

query_1 = """
    DROP VIEW IF EXISTS {view_out};
    CREATE VIEW {view_out} AS
    SELECT a.*, b.area, {pop_cols}
    FROM {table_in} a
    LEFT JOIN {area} b ON {join_1} = {join_2}
    LEFT JOIN {pop} c ON {join_1} = {join_3};
"""

query_2 = """
    DROP VIEW IF EXISTS {view_out};
    DROP TABLE IF EXISTS {table_out1};
    DROP TABLE IF EXISTS {table_out2};
    DROP TABLE IF EXISTS {table_out3};
"""


def get_inputs(l):
    inputs_0 = cwd / '../../adm0-generator/outputs/osm/intl'
    inputs_x = cwd / '../../admin-boundaries/outputs/edge-matched/humanitarian/intl'
    return inputs_0 if l == 0 else inputs_x


def run_funcs(l):
    import_data(l)
    merge(l)
    export(l)
    clean(l)


def import_data(l):
    area = cwd / f'../../population-statistics/data/area_{l}.parquet'
    pop = (
        cwd / f'../../population-statistics/outputs/population/humanitarian/intl/cod/adm{l}_join.parquet')
    for src, dest in [(area, f'adm{l}_area'), (pop, f'adm{l}_pop')]:
        df = pd.read_parquet(src)
        df.to_sql(dest, f'postgresql:///{DATABASE}',
                  if_exists='replace', index=False, method='multi')
    input = get_inputs(l) / f'adm{l}_polygons.gpkg.zip'
    subprocess.run([
        'ogr2ogr',
        '-overwrite',
        '-makevalid',
        '-dim', 'XY',
        '-t_srs', 'EPSG:4326',
        '-lco', 'FID=fid',
        '-lco', 'GEOMETRY_NAME=geom',
        '-nln', f'adm{l}_polygons',
        '-f', 'PostgreSQL', f'PG:dbname={DATABASE}',
        '/vsizip/' + str(input),
    ])
    logger.info(f'adm{l}_import')


def merge(l):
    pop_cols = list(map(lambda x: Identifier(x), cols_meta + get_pop_cols()))
    conn = connect(f'dbname={DATABASE}', autocommit=True)
    conn.execute(SQL(query_1).format(
        table_in=Identifier(f'adm{l}_polygons'),
        area=Identifier(f'adm{l}_area'),
        pop=Identifier(f'adm{l}_pop'),
        pop_cols=SQL(',').join(pop_cols),
        join_1=Identifier('a', f'adm{l}_id'),
        join_2=Identifier('b', f'adm{l}_id'),
        join_3=Identifier('c', f'adm{l}_id'),
        view_out=Identifier(f'adm{l}_join'),
    ))
    conn.close()
    logger.info(f'adm{l}_merge')


def export(l):
    output = outputs / f'adm{l}_polygons.geojsonl.gz'
    output.unlink(missing_ok=True)
    subprocess.run([
        'ogr2ogr',
        '-mapFieldType', 'Date=String',
        '-f', 'GeoJSONSeq',
        '/vsigzip/' + str(output),
        f'PG:dbname={DATABASE}', f'adm{l}_join',
    ])
    logger.info(f'adm{l}_export')


def clean(l):
    conn = connect(f'dbname={DATABASE}', autocommit=True)
    conn.execute(SQL(query_2).format(
        view_out=Identifier(f'adm{l}_join'),
        table_out1=Identifier(f'adm{l}_polygons'),
        table_out2=Identifier(f'adm{l}_area'),
        table_out3=Identifier(f'adm{l}_pop'),
    ))
    conn.close()
    logger.info(f'adm{l}_clean')


def main():
    outputs.mkdir(parents=True, exist_ok=True)
    results = []
    pool = Pool()
    for l in range(0, 5):
        result = pool.apply_async(run_funcs, args=[l])
        results.append(result)
    pool.close()
    pool.join()
    for result in results:
        result.get()
    logger.info('finished')


def cleanup():
    shutil.rmtree(outputs, ignore_errors=True)
