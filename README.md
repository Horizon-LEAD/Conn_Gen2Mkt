# Connector gen-2-market

## Execution

```
python ParcelGen2ParcelMkt.py \
    test Input Output \
    Params_ParcelGen.txt \
    ParcelDemand_Test.csv \
    skimTijd_new_REF.mtx \
    skimAfstand_new_REF.mtx \
    Zones_v4.shp \
    SEGS2020.csv \
    parcelNodes_v2.shp
```

```
python -m src.gen2mkt.__main__ -vvv --env .env \
    sample-data/input/ParcelDemand_Test.csv \
    sample-data/input/skimTijd_new_REF.mtx \
    sample-data/input/skimAfstand_new_REF.mtx \
    sample-data/input/Zones_v4.zip \
    sample-data/input/SEGS2020.csv \
    sample-data/input/parcelNodes_v2.zip
```