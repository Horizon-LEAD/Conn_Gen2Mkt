# Connector gen-2-market

## Installation

The `requirements.txt` and `Pipenv` files are provided for the setup of an environment where the module can be installed. The package includes a `setup.py` file and it can be therefore installed with a `pip install .` when we are at the same working directory as the `setup.py` file. For testing purposes, one can also install the package in editable mode `pip install -e .`.

After the install is completed, an executable `gen2mkt` will be available to the user.

Furthermore, a `Dockerfile` is provided so that the user can package the parcel generation model. To build the image the following command must be issued from the project's root directory:

```
docker build -t gen2mkt:latest .
```

## Usage 

```
gen2mkt -h                                                                                                                                  19.9s  2023-02-20 19:26:49
usage: gen2mkt [-h] [-v] [--flog] [-e ENV] [--gui] PARCELS ZONES SEGS PARCELNODES OUTDIR

gen2mkt connector

positional arguments:
  PARCELS            The path of the parcel demand file (csv)
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
  gen2mkt:latest \
  /data/input/ParcelDemand.csv \
  /data/input/Zones_v4.zip \
  /data/input/SEGS2020.csv \
  /data/input/parcelNodes_v2.zip \
  /data/output/
```