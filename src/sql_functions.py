
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

    # aws sdk python
    import boto3

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




# custom imports




grant_access_query ='''GRANT CREATE, USAGE ON SCHEMA schema_name TO username;'''


sql_create_client_table = '''
        CREATE TABLE IF NOT EXISTS client_data (
            district  TEXT,
            client_id INT,
            client_catg  TEXT,
            region TEXT,
            creation_date DATE,
            target DECIMAL,
        );
        '''



sql_create_invoice_table = '''
        CREATE TABLE IF NOT EXISTS invoice_data (
            client_id INT,
            invoice_date DATE,
            tarif_type TEXT,
            counter_number INT,
            counter_statue TEXT,
            counter_code TEXT,
            reading_remarque TEXT,
            counter_coefficient DECIMAL,
            consommation_level_1 DECIMAL,
            consommation_level_2 DECIMAL,
            consommation_level_3 DECIMAL,
            consommation_level_4 DECIMAL,
            old_index DECIMAL,
            new_index DECIMAL,
            months_number INT,
            counter_type TEXT
        );
        '''














