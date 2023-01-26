import pandas as pd
from time import time
from sqlalchemy import create_engine
import argparse


def main(params):

    pg_user=params.user
    pg_password=params.password
    pg_host=params.host
    pg_port=params.port
    pg_db=params.db
    pg_table = params.table
    csv_path = params.csv_path
    zone_csv_path = params.zone_csv_path
    
    engine = create_engine(f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}")
    con = engine.connect()


    
    zones_df = pd.read_csv(zone_csv_path)
    zones_df.to_sql(con=con, name="zones", if_exists="append")
    print("Zones ingested")


    df_iter = pd.read_csv(csv_path, iterator=True, chunksize=100000)
    df = next(df_iter)



    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    df.head(0).to_sql(con=con, name=pg_table, if_exists="replace")

    df.to_sql(con=con, name=pg_table, if_exists="append")

    try:
        while True:
            t_start = time()
            df = next(df_iter)

            df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
            df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
            df.to_sql(con=con, name=pg_table, if_exists="append")

            end_time = time()
            print("New records added {}".format(end_time-t_start))
    except StopIteration:
        print("All records ingested")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Ingesting data in to pgdatabase')
    parser.add_argument('--user', help="Database user") 
    parser.add_argument('--password', help="Database password") 
    parser.add_argument('--host', help="Database host") 
    parser.add_argument('--port', help="Database port") 
    parser.add_argument('--db', help="Database name") 
    parser.add_argument('--table', help="Database table") 
    parser.add_argument('--csv_path', help="CSV Path") 
    parser.add_argument('--zone_csv_path', help="Zone CSV Path") 

    params = parser.parse_args()
    main(params)