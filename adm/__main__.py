from . import geojsonl, geojsonl_all, tile_join, tiles, tiles_all
from .utils import logging

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("starting")
    geojsonl.main()
    if False:
        geojsonl_all.main()
    tiles.main()
    if False:
        tiles_all.main()
    tile_join.main()
    geojsonl.cleanup()
