import json
import subprocess

from .utils import MAX_ZOOM, cwd, logging

logger = logging.getLogger(__name__)

inputs = cwd / "../tmp"
outputs = inputs


def adm_points(lvl, name, z_min, z_max):
    subprocess.run(
        [
            "tippecanoe",
            "--quiet",
            f"--layer=adm{lvl}_points",
            f"--minimum-zoom={z_min}",
            f"--maximum-zoom={z_max}",
            "--drop-rate=1",
            "--read-parallel",
            "--no-tile-size-limit",
            "--force",
            f"--include=adm{lvl}_name",
            "--include=status_cd",
            "--include=area_km",
            f"--output={outputs}/{name}.mbtiles",
            f"{inputs}/{name}.geojsonl.gz",
        ], check=False,
    )
    logger.info(name)


def adm_lines(lvl, name, z_min, z_max):
    subprocess.run(
        [
            "tippecanoe",
            "--quiet",
            f"--layer=adm{lvl}_lines",
            f"--minimum-zoom={z_min}",
            f"--maximum-zoom={z_max}",
            "--simplify-only-low-zooms",
            "--no-simplification-of-shared-nodes",
            "--read-parallel",
            "--no-tile-size-limit",
            "--force",
            "--include=rank",
            "--include=area_km",
            f"--output={outputs}/{name}.mbtiles",
            f"{inputs}/{name}.geojsonl.gz",
        ], check=False,
    )
    logger.info(name)


def get_zooms(layer):
    z_min = 0
    z_max = MAX_ZOOM
    if "minzoom" in layer:
        z_min = layer["minzoom"]
    if "maxzoom" in layer and layer["maxzoom"] < MAX_ZOOM:
        z_max = layer["maxzoom"]
    return layer["id"], z_min, z_max


def get_layers(geom, lvl):
    with open(cwd / f"../../vector-styles/src/layers/adm{lvl}-{geom}.json") as f:
        data = json.load(f)
    return map(get_zooms, data)


def main():
    outputs.mkdir(parents=True, exist_ok=True)
    for geom in ["points", "lines"]:
        func = adm_lines if geom == "lines" else adm_points
        func(0, f"adm0_{geom}", 0, MAX_ZOOM)
        for lvl in range(1, 3):
            for layer, z_min, z_max in get_layers(geom, lvl):
                func(lvl, f"adm{lvl}_{geom}_{layer}", z_min, z_max)
    logger.info("finished")
