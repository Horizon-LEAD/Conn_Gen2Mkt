# Connector gen-2-market

## Usage 

```
$ gen2mkt -h
usage: gen2mkt [-h] [-v] [--flog] [-e ENV] [--gui] PARCELS SKIMTIME SKIMDISTANCE ZONES SEGS PARCELNODES OUTDIR

gen2mkt connector

positional arguments:
  PARCELS            The path of the parcel demand file (csv)
  SKIMTIME           The path of the time skim matrix (mtx)
  SKIMDISTANCE       The path of the distance skim matrix (mtx)
  ZONES              The path of the area shape file (shp)
  SEGS               The path of the socioeconomics data file (csv)
  PARCELNODES        The path of the parcel nodes file (shp)
  OUTDIR             The output directory

optional arguments:
  -h, --help         show this help message and exit
  -v, --verbosity    Increase output verbosity (default: 0)
  --flog             Stores logs to file (default: False)
  -e ENV, --env ENV  Defines the path of the environment file (default: None)
  --gui              Displays the graphical user interface (default: False)
```

## Execution


```
gen2mkt -vvv --env .env \
    sample-data/input/ParcelDemand.csv \
    sample-data/input/skimTijd_new_REF.mtx \
    sample-data/input/skimAfstand_new_REF.mtx \
    sample-data/input/Zones_v4.zip \
    sample-data/input/SEGS2020.csv \
    sample-data/input/parcelNodes_v2.zip \
    sample-data/output/
```


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