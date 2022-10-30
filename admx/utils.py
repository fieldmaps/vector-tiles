import gzip
import shutil
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
cwd = Path(__file__).parent

DATABASE = 'vector_tiles'
MAX_ZOOM = 11

cols_meta = ['pop_src', 'pop_src1', 'pop_lvl', 'pop_year']
grps = ['t', 'f', 'm']
dests = ['00_04', '05_09', '10_14', '15_19', '20_24', '25_29', '30_34',
         '35_39', '40_44', '45_49', '50_54', '55_59', '60_plus']
special = ['t_15_24', 'f_15_49']


def get_pop_cols():
    cols = ['t', 'f', 'm']
    for grp in grps:
        for dest in dests:
            cols.append(f'{grp}_{dest}')
    cols = cols + special
    return cols


def compress_file(output, compressed):
    compressed.unlink(missing_ok=True)
    with open(output, 'rb') as f_in:
        with gzip.open(compressed, 'wb', compresslevel=1) as f_out:
            shutil.copyfileobj(f_in, f_out)
            output.unlink()


def get_inputs(l):
    inputs_0 = cwd / '../../adm0-generator/outputs/osm/intl'
    inputs_x = cwd / '../../admin-boundaries/outputs/edge-matched/humanitarian/intl'
    return inputs_0 if l == 0 else inputs_x
