import subprocess

from .utils import cwd, logging

logger = logging.getLogger(__name__)

inputs = (cwd / "../tmp").glob("*.mbtiles")
output = cwd / "../dist/data"
file = output / "adm.pmtiles"


def main():
    file.unlink(missing_ok=True)
    output.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "tile-join",
            "--name=adm",
            '--attribution=<a href="https://fieldmaps.io/data/" target="_blank">&copy; FieldMaps</a>',
            "--no-tile-size-limit",
            "--force",
            f"--output={file}",
            *inputs,
        ]
    )
    logger.info("finished")
