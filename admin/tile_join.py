import subprocess
from admin.utils import logging, cwd

logger = logging.getLogger(__name__)

inputs = (cwd / '../tmp').glob('*.mbtiles')
output = cwd / '../dist/data'
file = output / 'admin.mbtiles'


def main():
    file.unlink(missing_ok=True)
    output.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        'tile-join',
        f'--name=admin',
        '--no-tile-size-limit',
        '--force',
        f'--output={file}',
        *inputs,
    ])
    logger.info('finished')
