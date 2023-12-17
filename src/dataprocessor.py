"""
script : dataprocessing.py 
purpose: 


"""


# Importing necessary libraries and modules 

import subprocess

try:

    import os
    import pandas as pd
    import numpy as np
    import missingno as msno 
    import seaborn as sns
    import matplotlib.pyplot as plt 
    import re

    import time
    from memory_profiler import profile

    # object serialization
    import joblib


    # split data - avoid data leakage
    from sklearn.model_selection import train_test_split, cross_val_score


    # cross validation, hyperparameter tuning
    from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, StratifiedKFold 

    # preprocessing: scaling, encoding
    from sklearn.preprocessing import MinMaxScaler, StandardScaler, OneHotEncoder, LabelEncoder
    from sklearn.compose import ColumnTransformer



except ImportError as error:
    print(f"Installation of the required dependencies necessary! {error}")

    subprocess.check_call(["pip", "install", "numpy"])
    subprocess.check_call(["pip", "install", "pandas"])
    subprocess.check_call(["pip", "install", "scikit-learn"])


    print(f"Successful installation of the required dependencies necessary")


import warnings
warnings.filterwarnings('ignore')


# custom imports
from dataloader import (
                load_data,
                )


from feature_engineering import (
                rename_columns,
                cast_schema_types,
                #column_mapper,
                counter_statue_mapper,
                create_new_feautures,
                #drop_column,
                #tariff_type_mapper,
                )







@profile
def read_combine_dataframe(datapath= None):

    """

    :param datapath: object - path to root data directory
    :return: object - data

    Description:

    read and merge the 2 data files
        - invoice.csv
        - clients.csv

    """

    if datapath:
        
        # "data/client_data.csv"
        client_path = os.path.normpath(os.path.join(datapath, 'client_data.csv'))
        # "data/invoice_data.csv"
        invoice_path = os.path.normpath(os.path.join(datapath, 'invoice_data.csv'))

        client_data = pd.read_csv(client_path)#, low_memory=True)#, engine="pyarrow")
        invoice_data = pd.read_csv(invoice_path)#, low_memory=True)#, engine="pyarrow")

    else:
        raise ValueError('''Either enter a source data path for the data files
                    
                        'datapath' : a data path used to load a csv data file
                    
                        ''')         
    
    data = pd.merge(client_data, invoice_data, on="client_id", how="left")

    return data


@profile
def read_dataset():
    '''
    :param: 
    :return: object - dataframe

    test funtion to compare memory usage and time with other
    
    '''
    client_data = pd.read_csv('../data/raw/client_data.csv')
    invoice_data = pd.read_csv('../data/raw/invoice_data.csv')
    data = pd.merge(client_data, invoice_data, on="client_id", how="left")
    return data

def missing_value_rate(data, column_name='counter_statue', col=True):

    """

    :param data: dataframe object - data
    :param column_name: str - name of columns to map values to
    :return: object - data

    Description:

    calculate percentage of missing values 
    """

    if col:
        print(f'''percentage of missing values in {column_name} : {round(data[column_name].isna().sum()/data.shape[0]*100,4)} %''')
    else:
        print(f'''percentage of missing values in data : {round(data.isna().sum()/data.shape[0]*100,4)} %''')







@profile
def data_wrangling(data):

    """

    :param data: object - data
    :return: object - data

    Description:

    data wrangling : cleaning, imputation, transformations and feature engineering
        - make column names consitent and rename columns
        - drop duplicates
        - removing punctuation and special characters
        - drop observations (rows) where 'ValueError' occurs
        - change target value to binary: 0 (not fraudulent client) and 1 (fraudulent client)
            - convert to int: from 0.0 -> 0  and 1.0 -> 1
        - 

    feature engineering
        - create column for number of years as a client
        - create column for index change
        - create column for index change per month
        - create column for money lost per fraudulent 
            client when total money lost declared as 200,000,000


    """


    # making column names consistent and rename
    data = rename_columns(data)

    # dropping duplicates and special characters
    data = data.drop_duplicates()
    data = data.applymap(lambda text: re.sub(r'[^A-Za-z0-9\s]+', ' ', text))

    # casting columns to specific types
    data = data.copy(deep=True)
    #data = data.convert_dtypes()

    data = cast_schema_types(data, params={'target': 'int'})

    # convert dates to datetime format
    data['invoice_date'] = pd.to_datetime(data['invoice_date'], format='%Y-%m-%d')
    data['creation_date'] = pd.to_datetime(data['creation_date'], format='%d/%m/%Y')

    # checking percentage of missing data
    print(f"numbers of rows : {data.shape[0]}")
    missing_value_rate(data, column_name=None, col=False)
    missing_value_rate(data, column_name='counter_statue', col=True)


    # check and drop rows with null values
    error_indices = get_invalid_indicies(data)
    data = data.drop(error_indices)
    print(data.isnull().T.any())


    ## feature engineering
    # create new features columns and drop columns
    data = create_new_feautures(data)
    #data = drop_column(data, col_name=['creation_date','invoice_date'])

    # delete client with 0 consommation and 0 months_number
    data = data.drop(index=3985967 , axis=0)

    # bin values in columns
    data = counter_statue_mapper(data)
    #data = tariff_type_mapper(data)


    return data




def get_invalid_indicies(data):
    """ 
    Get the indices which doesn't satisfy conditions and raises value error.

    :param data: object - data
    :custom_function: object - function to be checked
    :return: object - list of observation indices

    Description:


    
    """

    # error_indices = []
    # for idx, row in data.iterrows():
    #     try:
    #         custom_function(row)
    #     except ValueError:
    #         error_indices.append(idx)

    error_indices = [data[data.isnull().T.any()].index]
    print(f"Indices causing ValueError: {error_indices}")

    return error_indices








def save_data_embeddings(data, data_path, file_path, file_name='nextpulse_data_embedding', *args, **kwargs):

    """


    :param data: object - data
    :param data_path: str - path to data
    :param file_path: str - path/location to save embedded data file
    :param file_name: str - save file with the name
    :print: str - print statement of sucessful save

    Description:

    generate and save processed data as embedding : cleaning, imputation, transformations and feature engineering
        - using joblib
        - or pickle?


    """
    
    get_embeddings = load_data(data_path=data_path, source='flat')
    data_embeddings = get_embeddings.values
    joblib.dump(data_embeddings, file_path)

    print(f"The file {file_name} sucessefully saved to location: {file_path}")


def data_scaler_encoder(data, scaler = 'minmax', *args, **kwargs):

    """


    :param data: object - data
    :param scaler: str - scaling/encoding method 
    :return: object - scaled/encoded data

    Description:

    scaling the data
        - normalization : minmaxscaler
        - standardization : standardscaler
    
    """

    scalers = {
        'minmax': MinMaxScaler(),
        'standard': StandardScaler(),
        'label': LabelEncoder(),
        'onehot': OneHotEncoder() 
    }

    if scaler in scalers:
        scaler = scalers[scaler]
        return scaler.fit_transform(data)
    else:
        raise ValueError(f"The scaling - normalization technique: '{scaler}' is not supported.")



def data_preprocessor(data, data_type = 'num', scaler= 'onehot', *args, **kwargs):

    """"


    :param data: object - data
    :param data_type: str - data type i.e 'num' (numerical) or 'cat' (categorical) 
    :param scaler: str - scaling/encoding method
    :return: object - processed data

    Description:

    num: scaling our numerical data
    cat: encoding our numerical data
    
    """

    if not isinstance(data_type, str) and (data_type not in ('num', 'cat')):

        raise ValueError('''Incorrect entry for the data_type to be preprocessed. 
                        Provide valid input: 'cat' for categorical data and 'num' for numerical data ''')
    
    else:

        if data_type == 'num' and scaler in ('minmax', 'standard'):
            # for preprocessing / scaling our numerical data
            scaled_data = data_scaler_encoder(data, scaler=scaler)


        elif data_type == 'cat' and scaler in ('label', 'onehot'):
            # for preprocessing / encoding our numerical data
            scaled_data = data_scaler_encoder(data, scaler=scaler)
        
        else:
            raise ValueError('''Incorrect scaler for the data_type to be preprocessed.Provide valid 
                            input: categorical data ('label' or 'onehot') and for numerical data  ('minmax' or 'standard')''')
        


    return scaled_data


