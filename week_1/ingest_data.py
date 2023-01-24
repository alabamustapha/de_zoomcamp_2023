
from sqlalchemy import create_engine
from time import time
import pandas as pd
import argparse
import os



def main(params):
    # get params
    pg_user = params.user
    pg_password = params.password
    pg_host = params.host
    pg_port = params.port
    pg_db = params.db
    pg_table_name = params.table_name
    csv_url = params.csv_url

    # connect to database engine
    engine = create_engine(f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}').connect()
    
    print(engine)
    
    # download csv from url
    # csv_name = "ny_taxi_data.csv"
    # to avoid downloading
    csv_name = "yellow_tripdata_2021-01.csv.gz"
    # download
    # sys.system(f"wget {csv_url} -O {csv_name}")
    # copy 
    # os.system(f"cp yellow_tripdata_2021-01.csv.gz {csv_name}")

    # read data in chunk
    df_iter = pd.read_csv(f"{csv_name}", iterator=True, chunksize=100000)
    df = next(df_iter)

    # create table if it does not exist
    df.head(0).to_sql(con=engine, name='yellow_taxi_data', if_exists="replace")

    # ingest first batch
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    df.to_sql(con=engine, name='yellow_taxi_data', if_exists="append")

    # loop and ingest each iter
    while True:
        t_start = time()
        df = next(df_iter)
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        
        df.to_sql(con=engine, name='yellow_taxi_data', if_exists="append")
        t_end = time()
        
        print("A chunk just finish in {%.3f}" % (t_end - t_start))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog = 'NY Taxi Trips 2021 Data Ingestion', 
        description = 'Download and ingest data for 2021 ny taxi trips'
        )
    
    parser.add_argument('--user', help='postgres database user')
    parser.add_argument('--password', help='postgres database password')
    parser.add_argument('--host', help='postgres database host')
    parser.add_argument('--port', help='postgres database port')
    parser.add_argument('--db', help='postgres database name')
    parser.add_argument('--table_name', help='postgres database table name')
    parser.add_argument('--csv_url', help='ny taxi 2021 csv url')

    args = parser.parse_args()
    main(args)