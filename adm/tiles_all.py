import subprocess

from .utils import MAX_ZOOM, cwd, logging

logger = logging.getLogger(__name__)

inputs = cwd / "../tmp"
outputs = inputs


def adm_points(lvl):
    subprocess.run(
        [
            "tippecanoe",
            f"--layer=adm{lvl}_points",
            f"--maximum-zoom={MAX_ZOOM}",
            "--drop-rate=1",
            "--read-parallel",
            "--no-tile-size-limit",
            "--force",
            f"--include=adm{lvl}_name",
            "--include=status_cd",
            "--include=area",
            f"--output={outputs}/adm{lvl}_points.pmtiles",
            f"{inputs}/adm{lvl}_points.geojsonl.gz",
        ]
    )
    logger.info(f"adm{lvl}_points")


def adm_lines(lvl):
    subprocess.run(
        [
            "tippecanoe",
            f"--layer=adm{lvl}_lines",
            f"--maximum-zoom={MAX_ZOOM}",
            "--simplify-only-low-zooms",
            "--no-simplification-of-shared-nodes",
            "--read-parallel",
            "--no-tile-size-limit",
            "--force",
            "--include=rank",
            "--include=area",
            f"--output={outputs}/adm{lvl}_lines.pmtiles",
            f"{inputs}/adm{lvl}_lines.geojsonl.gz",
        ]
    )
    logger.info(f"adm{lvl}_lines")


def main():
    outputs.mkdir(parents=True, exist_ok=True)
    for lvl in range(0, 3):
        adm_points(lvl)
        adm_lines(lvl)
    logger.info("finished")
