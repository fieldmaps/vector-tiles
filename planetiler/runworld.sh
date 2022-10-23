java -Xmx116g \
  -XX:MaxHeapFreeRatio=40 \
  -jar planetiler.jar \
  --exclude-layers=boundary \
  --area=planet --bounds=planet --download \
  --download-threads=10 --download-chunk-size-mb=1000 \
  --fetch-wikidata \
  --mbtiles=planet.mbtiles \
  --nodemap-type=array --storage=ram \
  --force 2>&1 | tee logs.txt
