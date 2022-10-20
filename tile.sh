gdal_translate -of mbtiles -co TILE_FORMAT=PNG8 -co ZLEVEL=9 -co BLOCKSIZE=512 NE1_HR_LC.tif ne1.mbtiles
gdaladdo -r cubic -oo TILE_FORMAT=PNG8 -oo ZLEVEL=9 ne1.mbtiles 2 4 8 16 32

gdal_translate -of mbtiles -co TILE_FORMAT=PNG8 -co ZLEVEL=9 -co BLOCKSIZE=512 NE1_HR_LC_SR.tif ne1-sr.mbtiles
gdaladdo -r cubic -oo TILE_FORMAT=PNG8 -oo ZLEVEL=9 ne1-sr.mbtiles 2 4 8 16 32

gdal_translate -of mbtiles -co TILE_FORMAT=PNG8 -co ZLEVEL=9 -co BLOCKSIZE=512 NE2_HR_LC.tif ne2.mbtiles
gdaladdo -r cubic -oo TILE_FORMAT=PNG8 -oo ZLEVEL=9 ne2.mbtiles 2 4 8 16 32

gdal_translate -of mbtiles -co TILE_FORMAT=PNG8 -co ZLEVEL=9 -co BLOCKSIZE=512 NE2_HR_LC_SR.tif ne2-sr.mbtiles
gdaladdo -r cubic -oo TILE_FORMAT=PNG8 -oo ZLEVEL=9 ne2-sr.mbtiles 2 4 8 16 32
