"""
script : data_processing.py 
purpose: 


"""


# Importing necessary libraries and modules 

import subprocess

try:

    import numpy as np
    import pandas as pd

    # databases - sql
    import psycopg2
    import sqlalchemy
    from dotenv import dotenv_values, load_dotenv
    from sqlalchemy import create_engine

    # data - api
    import requests

    # object serialisation
    import pickle
    import joblib

    # pipeline
    from sklearn.pipeline import Pipeline
    from sklearn.pipeline import make_pipeline

except ImportError as error:
    print(f"Installation of the required dependencies necessary! {error}")

    subprocess.check_call(["pip", "install", "numpy"])
    subprocess.check_call(["pip", "install", "pandas"])
    subprocess.check_call(["pip", "install", "pickle"])
    subprocess.check_call(["pip", "install", "joblib"])
    subprocess.check_call(["pip", "install", "requests"])


    print(f"Successful installation of the required dependencies necessary")


import warnings
warnings.filterwarnings('ignore')


# custom imports
#from sql_functions import (
#        get_data_postgres_db,
#        )

from config import (
                get_sql_config,
                )


def get_data_structured_file(data_path, *args, **kwargs):
    """
    function to map and read data based on their file formats
    tabular and structured data file formats

    :param data_path: str - query statement, valid instructions to database
    :return: object - data

    Description:

    supported file formats: 
        'csv' - csv, 'parquet' - parquet, 
        'xlsx' or 'xls' -  excel, 'json' - json
        
    """

    read_functions = {
        'csv': pd.read_csv,
        'xlsx': pd.read_excel,
        'json': pd.read_json,
        'parquet': pd.read_parquet,
        'xls': pd.read_excel,
        
    }

    get_file_extension = data_path.split('.')[-1].lower()

    if get_file_extension not in read_functions:
        raise ValueError(f"Unsupported file format: {get_file_extension}")

    try:
        read_function = read_functions[get_file_extension]
        data = read_function(data_path)
        return data
    except Exception as error:
        print(f"Error reading file: {error}")
        return None


def get_conn_engine_alchemy(config, driver=None, *args, **kwargs):

    """
    SQLAlchemy - function to create a connection to the dialect; PostgreSQL server

    :param driver: str - if alchemy, default (None) driver or psycopg2   
    :return: object - connection engine object

    Description:

    drivers : 'psycopg2', 'None'-(auto/default choice), 'pg800' - (not supported yet)
    dialects: 'postgresql', others not supported yet ('mysql', 'oracle', sqlite, 'mssql')

    - call the function imported get_sql_config() which gets the credentials
    - use the configurations gotten to create the database connection string (db_url)
        - with no specific driver (automatic choice based on environment configurations and installed packages) 
        - or with psycopg2 driver (PostgreSQL adapter)
    - return engine
        
    """

    config_data = config()

    if driver == 'psycopg2':
        db_url = f'''postgresql+psycopg2://{config_data['user']}:{config_data['password']}@{config_data['host']}:{config_data['port']}/{config_data['database']}'''

    else:
        db_url = f'''postgresql://{config_data['user']}:{config_data['password']}@{config_data['host']}:{config_data['port']}/{config_data['database']}'''


    try:
        engine = create_engine(db_url)
        print("Connection Sucessful!")
    except (Exception, sqlalchemy.exc.SQLAlchemyError) as error:
        print(error)

    return engine


def get_conn_engine_psycopg(config, *args, **kwargs):

    """
    psycopg2 driver (PSQL adapter) - function to create a connection to the PostgreSQL server


    :param: 
    :return: object - connection engine object

    Description:
    

    - call the function imported get_sql_config() which gets the credentials
    - use the configurations gotten to create the database connection 
    - return engine / connection object
    
    """

    config_data = config()

    try:
        engine = psycopg2.connect(
            user=config_data['user'],
            password=config_data['password'],
            host=config_data['host'],
            database=config_data['database']
        )
        print("Connection Sucessful!")
    except (Exception, psycopg2.Error) as error:
        print(error)

    return engine



def get_data_postgres_db(sql_query, chunk_size=15000, plain=True, driver=None, *args, **kwargs):
    ''' 
    Get data using connection engine to connect to the PostgreSQL database server, 


    :param sql_query: str - query statement, valid instructions to database
    :param chunk_size: int - numeric value for chunks of streaming data 
    :param plain: bool - make connecttion to db without alchemy or not
    :param driver: str - if alchemy, default (None) driver or psycopg2   
    :return: object - data

    Description:

    if plain set to True, the psycopg2 is used to connect to the db without alchemy:
        - execute sql queries with a curser for the connection
        - call execute() method on cursor
        - fetch data
            - all: use of fetchall() to fetch all rows from executed query
            - stream data in chunks: use of fetchmany() to fetch rows from executed query
        - close cursor and connection
        - return data as a pandas dataframe

    else :
        - use SQLAlchemy
        - takes query and connection engine
        - read query using pandas method read_sql_query()
        - return data as a pandas dataframe

    '''

    if plain == True:

        #con = conn_engine
        conn_engine = get_conn_engine_psycopg()
        #cursor = con.cursor()
        cursor = conn_engine.cursor(name='streaming_cursor', cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute(sql_query)
        #data = cursor.fetchall()

        while True:
            data = cursor.fetchmany(size=chunk_size)
            if not data:
                break

        cursor.close()
        conn_engine.close()
        data = pd.DataFrame(data)

    else:
        conn_engine = get_conn_engine_alchemy(driver=driver)
        data = pd.read_sql_query(sql=sql_query, con=conn_engine)

    return data 



def get_data_serialized_file(data_path, *args, **kwargs):
    """
    function to map and read data based on their file formats
    
    :param data_path: str - query statement, valid instructions to database
    :return: object - data

    Description:

    supported file formats: 
        'pkl' - pickle, 'joblib' - joblib
        'npy' - numpy, 'txt' - text
        
    """


    get_file_extension = data_path.split('.')[-1].lower()

    try:
        if get_file_extension == 'pkl':
            with open(data_path, 'rb') as f:
                data = pickle.load(f)

        elif get_file_extension == 'joblib':
            with open(data_path, 'rb') as f:
                data = joblib.load(f)

        elif get_file_extension == 'npy':
            data = np.load(data_path, allow_pickle=True)

        else:
            raise ValueError(f"Unsupported file format: {get_file_extension}")
        
        return data
    except Exception as error:
        print(f"Error reading file: {error}")
        return None



def get_data_apis(url, *args, **kwargs):
    ''' 
    Get data from API

    :param url: str - url 
    :return: object - data


    Description:

    '''

    response = requests.get(url)
    data = response.json()

    return data 




def load_data(data_path, source='flat', *args, **kwargs):

    """
    Load data from source file or location

    :param data_path: str - path to source file or location
    :param source: str - path to source file or location

        'flat':  get data from structured source (e.g csv, parquet, json, xlsx, etc)
        'serial':  get data from serialized/ embedded files (e.g joblib, pkl, npy)
        'db':  get data from database source 
        'api': get data from api source

    :return: object - data

    Description:

    """
        
    get_data_method = {
        'flat': get_data_structured_file(data_path),   
        'serial': get_data_serialized_file(data_path),
        'db': get_data_postgres_db(data_path),
        'api': get_data_apis(data_path),
    }
    
    if source in get_data_method:
        data = get_data_method[source]()
    else:
        raise ValueError('''Invalid source to get data. Valid Sources are: 
                        'flat':  get data from structured source (e.g csv, parquet, json, xlsx, etc)
                        'serial':  get data from serialized/ embedded files (e.g joblib, pkl, npy)
                        'db':  get data from database source 
                        'api': get data from api source
                        ''')
    return data












if __name__ == '__main__':

    data_path = 'data/processed/datafile.csv'
    data = load_data(data_path, source='flat')
    print(f"There are {data.shape[0]} observations and {data.shape[1]} feature variables")


