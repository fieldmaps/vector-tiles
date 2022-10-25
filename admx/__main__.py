from admx import geojsonl, mbtiles
from admx.utils import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info('starting')
    geojsonl.main()
    mbtiles.main()
    geojsonl.cleanup()
