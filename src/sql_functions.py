
"""
script : sql_functions.py 
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

    # pipeline
    from sklearn.pipeline import Pipeline
    from sklearn.pipeline import make_pipeline



except ImportError as error:
    print(f"Installation of the required dependencies necessary! {error}")

    subprocess.check_call(["pip", "install", "psycopg2-binary"])
    subprocess.check_call(["pip", "install", "python-dotenv"])



    print(f"Successful installation of the required dependencies necessary")


import warnings
warnings.filterwarnings('ignore')







def get_sql_config():
    '''
        Function loads credentials from .env file and
        returns a dictionary containing the data needed for sqlalchemy.create_engine()
    '''
    needed_keys = ['host', 'port', 'database','user','password', 'db_url']
    #needed_keys = ['host', 'port', 'database','password', 'db_url']

    dotenv_dict = dotenv_values(".env")
    sql_config = {key:dotenv_dict[key] for key in needed_keys if key in dotenv_dict}
    return sql_config





def get_conn_engine_alchemy(driver=None, *args, **kwargs):

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

    sql_config_data = get_sql_config()

    if driver == 'psycopg2':
        db_url = f'''postgresql+psycopg2://{sql_config_data['user']}:{sql_config_data['password']}@{sql_config_data['host']}:{sql_config_data['port']}/{sql_config_data['database']}'''

    else:
        db_url = f'''postgresql://{sql_config_data['user']}:{sql_config_data['password']}@{sql_config_data['host']}:{sql_config_data['port']}/{sql_config_data['database']}'''


    try:
        engine = create_engine(db_url)
        print("Connection Sucessful!")
    except (Exception, sqlalchemy.exc.SQLAlchemyError) as error:
        print(error)

    return engine


def get_conn_engine_psycopg(*args, **kwargs):

    """
    psycopg2 driver (PSQL adapter) - function to create a connection to the PostgreSQL server


    :param: 
    :return: object - connection engine object

    Description:
    

    - call the function imported get_sql_config() which gets the credentials
    - use the configurations gotten to create the database connection 
    - return engine / connection object
    
    """

    sql_config_data = get_sql_config()

    try:
        engine = psycopg2.connect(
            user=sql_config_data['user'],
            password=sql_config_data['password'],
            host=sql_config_data['host'],
            database=sql_config_data['database']
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






