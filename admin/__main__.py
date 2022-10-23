from admin import geojsonl, mbtiles, tile_join
from admin.utils import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info('starting')
    geojsonl.main()
    mbtiles.main()
    tile_join.main()
    geojsonl.cleanup()
