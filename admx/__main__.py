from . import geojsonl, tiles
from .utils import logging

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("starting")
    geojsonl.main()
    tiles.main()
    geojsonl.cleanup()
