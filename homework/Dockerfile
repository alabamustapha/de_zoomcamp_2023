FROM python:3.9.1

WORKDIR /app
RUN pip install pandas sqlalchemy psycopg2
COPY green_tripdata_2019-01.csv.gz green_tripdata_2019-01.csv.gz
COPY taxi_zone_lookup.csv taxi_zone_lookup.csv
COPY ingesting.py ingesting.py

ENTRYPOINT ["python", "ingesting.py"]
