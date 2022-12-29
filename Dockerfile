FROM python:3.8.12-slim-bullseye

RUN apt-get update && \
   apt-get install -y --no-install-recommends \
       liblapack-dev libatlas-base-dev && \
   rm -rf /var/lib/apt/lists/*

WORKDIR /srv/parcel-generation

COPY setup.py requirements.txt README.md /srv/parcel-generation/
COPY src /srv/parcel-generation/src

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /srv/parcel-generation/requirements.txt && \
    pip install --no-cache-dir /srv/parcel-generation/

ENTRYPOINT [ "gen2mark", "-vv" ]
