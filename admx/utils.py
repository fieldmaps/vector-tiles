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
