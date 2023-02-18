# Connector gen-2-market

## Execution

```
docker run --rm \     
  -v $PWD/sample-data/input:/data/input \
  -v $PWD/sample-data/output:/data/output \
  --env-file .env \
  gen2mkt:Dockerfile \
  /data/input/ParcelDemand.csv \
  /data/input/skimTijd_new_REF.mtx \
  /data/input/skimAfstand_new_REF.mtx \
  /data/input/Zones_v4.zip \
  /data/input/SEGS2020.csv \
  /data/input/parcelNodes_v2.zip \
  /data/output/
  ```