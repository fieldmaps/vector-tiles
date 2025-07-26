import subprocess

from .utils import MAX_ZOOM, cwd, logging

logger = logging.getLogger(__name__)

inputs = cwd / "../tmpx"
outputs = cwd / "../dist/data"


def adm_polygons(l):
    subprocess.run(
        [
            "tippecanoe",
            "--layer=admx",
            '--attribution=<a href="https://fieldmaps.io/data/" target="_blank">&copy; FieldMaps</a>',
            f"--maximum-zoom={MAX_ZOOM}",
            "--simplify-only-low-zooms",
            "--no-simplification-of-shared-nodes",
            "--read-parallel",
            "--no-tile-size-limit",
            "--force",
            f"--output={outputs}/adm{l}.pmtiles",
            f"{inputs}/adm{l}_polygons.geojsonl.gz",
        ], check=False,
    )
    logger.info(f"adm{l}_polygons")


def main():
    outputs.mkdir(parents=True, exist_ok=True)
    for l in range(5):
        adm_polygons(l)
    logger.info("finished")
