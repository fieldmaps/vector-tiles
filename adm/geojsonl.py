import json
import shutil
import subprocess
from multiprocessing import Pool

from .utils import cwd, logging

logger = logging.getLogger(__name__)

inputs_0 = cwd / "../../adm0-generator/outputs/adm0/osm/intl"
inputs = cwd / "../../admin-boundaries/outputs/edge-matched/humanitarian/intl"
area = cwd / "../../admin-boundaries/data/edge-matched/humanitarian/intl/area.xlsx"
outputs = cwd / "../tmp"


def export_adm0(geom):
    input = inputs_0 / f"adm0_{geom}.gpkg.zip"
    output = outputs / f"adm0_{geom}.geojsonl.gz"
    output.unlink(missing_ok=True)
    sql_if = "SELECT * FROM adm0_lines;"
    sql_else = " ".join(
        [
            "SELECT a.*, b.area_0_km AS area_km",
            f"FROM adm0_{geom} a",
            f"LEFT JOIN '{area}'.area b ON a.adm0_id = b.adm0_id;",
        ]
    )
    sql = sql_if if geom == "lines" else sql_else
    subprocess.run(
        [
            "ogr2ogr",
            *["-mapFieldType", "Date=String"],
            *["-f", "GeoJSONSeq"],
            *["-dialect", "INDIRECT_SQLITE"],
            *["-sql", sql],
            "/vsigzip/" + str(output),
            "/vsizip/" + str(input),
        ]
    )
    logger.info(f"adm0_{geom}")


def export(geom, lvl, layer, a_min, a_max):
    input = inputs / f"adm{lvl}_{geom}.gpkg.zip"
    output = outputs / f"adm{lvl}_{geom}_{layer}.geojsonl.gz"
    output.unlink(missing_ok=True)
    sql = " ".join(
        [
            f"SELECT a.*, b.area_{lvl}_km AS area_km",
            f"FROM adm{lvl}_{geom} a",
            f"LEFT JOIN '{area}'.area b ON a.adm0_id = b.adm0_id",
            f"WHERE a.adm{lvl-1}_id IS NOT NULL AND area_km <= {a_max} AND area_km > {a_min};",
        ]
    )
    subprocess.run(
        [
            "ogr2ogr",
            *["-mapFieldType", "Date=String"],
            *["-f", "GeoJSONSeq"],
            *["-dialect", "INDIRECT_SQLITE"],
            *["-sql", sql],
            "/vsigzip/" + str(output),
            "/vsizip/" + str(input),
        ]
    )
    logger.info(f"adm{lvl}_{geom}_{layer}")


def get_zooms(layer):
    a_min = 0
    a_max = 1e8
    if "filter" in layer:
        if layer["filter"][0] == "all":
            a_max = layer["filter"][1][2]
            a_min = layer["filter"][2][2]
        if layer["filter"][0] == ">":
            a_min = layer["filter"][2]
        if layer["filter"][0] == "<=":
            a_max = layer["filter"][2]
    return layer["id"], int(a_min), int(a_max)


def get_layers(geom, lvl):
    with open(cwd / f"../../vector-styles/src/layers/adm{lvl}-{geom}.json") as f:
        data = json.load(f)
    return map(get_zooms, data)


def main():
    outputs.mkdir(parents=True, exist_ok=True)
    results = []
    pool = Pool()
    for geom in ["points", "lines"]:
        export_adm0(geom)
        for lvl in range(1, 3):
            for layer, a_min, a_max in get_layers(geom, lvl):
                args = [geom, lvl, layer, a_min, a_max]
                result = pool.apply_async(export, args=args)
                results.append(result)
    pool.close()
    pool.join()
    for result in results:
        result.get()
    logger.info("finished")


def cleanup():
    shutil.rmtree(outputs, ignore_errors=True)
