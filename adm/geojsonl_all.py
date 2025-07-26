import shutil
import subprocess
from multiprocessing import Pool

from .utils import cwd, logging

logger = logging.getLogger(__name__)

inputs = cwd / "../../admin-boundaries/outputs/edge-matched/humanitarian/intl"
area = cwd / "../../population-statistics/data/area.xlsx"
outputs = cwd / "../tmp"


def export(geom, lvl):
    input = inputs / f"adm4_{geom}.gpkg.zip"
    output = outputs / f"adm{lvl}_{geom}.geojsonl.gz"
    output.unlink(missing_ok=True)
    sql_if = "SELECT * FROM adm0_lines;"
    sql_else = " ".join(
        [
            f"SELECT a.*, b.area_{lvl}_km AS area_km",
            f"FROM adm{lvl}_{geom} a",
            f"LEFT JOIN '{area}'.area b ON a.adm0_id = b.adm0_id;",
        ],
    )
    sql = sql_if if geom == "lines" and lvl == 0 else sql_else
    subprocess.run(
        [
            "ogr2ogr",
            *["-mapFieldType", "Date=String"],
            *["-f", "GeoJSONSeq"],
            *["-dialect", "INDIRECT_SQLITE"],
            *["-sql", sql],
            "/vsigzip/" + str(output),
            "/vsizip/" + str(input),
        ], check=False,
    )
    logger.info(f"adm{lvl}_{geom}")


def main():
    outputs.mkdir(parents=True, exist_ok=True)
    results = []
    pool = Pool()
    for geom in ["points", "lines"]:
        for lvl in range(3):
            result = pool.apply_async(export, args=[geom, lvl])
            results.append(result)
    pool.close()
    pool.join()
    for result in results:
        result.get()
    logger.info("finished")


def cleanup():
    shutil.rmtree(outputs, ignore_errors=True)
