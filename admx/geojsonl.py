import shutil
import subprocess
from multiprocessing import Pool

from psycopg import connect
from psycopg.sql import SQL, Identifier

from .utils import DATABASE, areas, compress_file, cwd, get_inputs, logging

logger = logging.getLogger(__name__)
outputs = cwd / "../tmpx"

query_1 = """
    DROP VIEW IF EXISTS {view_out};
    CREATE VIEW {view_out} AS
    SELECT a.*, b.area_km
    FROM {table_in} a
    LEFT JOIN {area} b ON {join_1} = {join_2};
"""

query_2 = """
    DROP VIEW IF EXISTS {view_out};
    DROP TABLE IF EXISTS {table_out1};
    DROP TABLE IF EXISTS {table_out2};
"""


def run_funcs(lvl):
    import_data(lvl)
    merge(lvl)
    export(lvl)
    clean(lvl)


def import_data(lvl):
    input_zip = get_inputs(lvl) / f"adm{lvl}_polygons.gpkg.zip"
    shutil.unpack_archive(input_zip, outputs)
    polygons = outputs / f"adm{lvl}_polygons.gpkg"
    area = areas / f"area_{lvl}.xlsx"
    inputs = [("area", area), ("polygons", polygons)]
    for name, input in inputs:
        subprocess.run(
            [
                "ogr2ogr",
                "-overwrite",
                *["-lco", "FID=fid"],
                *["-lco", "GEOMETRY_NAME=geom"],
                *["-nln", f"adm{lvl}_{name}"],
                *["-f", "PostgreSQL", f"PG:dbname={DATABASE}"],
                input,
            ], check=False,
        )
    polygons.unlink(missing_ok=True)
    logger.info(f"adm{lvl}_import")


def merge(lvl):
    conn = connect(f"dbname={DATABASE}", autocommit=True)
    conn.execute(
        SQL(query_1).format(
            table_in=Identifier(f"adm{lvl}_polygons"),
            area=Identifier(f"adm{lvl}_area"),
            join_1=Identifier("a", f"adm{lvl}_id"),
            join_2=Identifier("b", f"adm{lvl}_id"),
            view_out=Identifier(f"adm{lvl}_join"),
        ),
    )
    conn.close()
    logger.info(f"adm{lvl}_merge")


def export(lvl):
    output = outputs / f"adm{lvl}_polygons.geojsonl"
    output.unlink(missing_ok=True)
    compressed = outputs / f"adm{lvl}_polygons.geojsonl.gz"
    subprocess.run(
        [
            "ogr2ogr",
            *["-mapFieldType", "Date=String"],
            *["-f", "GeoJSONSeq"],
            output,
            *[f"PG:dbname={DATABASE}", f"adm{lvl}_join"],
        ], check=False,
    )
    compress_file(output, compressed)
    output.unlink(missing_ok=True)
    logger.info(f"adm{lvl}_export")


def clean(lvl):
    conn = connect(f"dbname={DATABASE}", autocommit=True)
    conn.execute(
        SQL(query_2).format(
            view_out=Identifier(f"adm{lvl}_join"),
            table_out1=Identifier(f"adm{lvl}_polygons"),
            table_out2=Identifier(f"adm{lvl}_area"),
        ),
    )
    conn.close()
    logger.info(f"adm{lvl}_clean")


def main():
    outputs.mkdir(parents=True, exist_ok=True)
    results = []
    pool = Pool()
    for l in range(5):
        result = pool.apply_async(run_funcs, args=[l])
        results.append(result)
    pool.close()
    pool.join()
    for result in results:
        result.get()
    logger.info("finished")


def cleanup():
    shutil.rmtree(outputs, ignore_errors=True)
