"""
script : data_processing.py 
purpose: 


"""


# Importing necessary libraries and modules 

import subprocess

try:

    import numpy as np
    import pandas as pd

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
from sql_functions import (
       get_data_postgres_db,
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


