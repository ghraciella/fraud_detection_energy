"""
script : feature_engineering.py 
purpose: 


"""


# Importing necessary libraries and modules 

import subprocess

try:

    import os
    import pandas as pd
    import numpy as np
    import time
    from memory_profiler import profile

except ImportError as error:
    print(f"Installation of the required dependencies necessary! {error}")

    subprocess.check_call(["pip", "install", "numpy"])
    subprocess.check_call(["pip", "install", "pandas"])
    subprocess.check_call(["pip", "install", "memory_profiler"])


    print(f"Successful installation of the required dependencies necessary")


import warnings
warnings.filterwarnings('ignore')


# custom imports
#



def rename_columns(data:pd.DataFrame) -> pd.DataFrame:
    """
    :param data: object - data
    :return: object - data

    Description:
    making column names consistent and rename columns

    """

    # making column names consistent and rename columns
    conditions = {
                    ' ': '_', 
                    'disrict':'district',
                    'client_catg': 'client_category',
                    }
    columns = {col:col.lower().replace(old, new) for col in data.columns.tolist() for old, new in conditions.items()}

    data = data.rename(columns= columns)

    return data


def drop_column(data:pd.DataFrame, col_name: str | list[str]) -> pd.DataFrame:
    """
    :param data: object - data
    :param col_name: str | list[str] - column name(s)
    :return: object - data

    Description:
    drop unwanted columns

    """

    data = data.drop([col_name], axis=1)
    return data


def cast_schema_types(data, params):

    """
    :param data: dataframe object - data
    :param params: dict object - dictionary containing key-value pairs for mapping
    :return: object - data

    Description:
    casts schema (column) types

    """

    for col_name, col_type in params.items():
        data = data[str(col_name)].astype(col_type)

    return data


@profile
def column_mapper(data, params, column_name='counter_statue'):

    """

    :param data: dataframe object - data
    :param params: dict object - dictionary containing key-value pairs for mapping
    :param column_name: str - name of columns to map values to
    :return: object - data

    Description:

    column mapper: 

        - check for pattern 
        - remove null values
        - bin/categories

    """

    data[column_name] = data[column_name].map(params)

    return data



def counter_statue_mapper(data):

    """
    :param data: object - data
    :return: object - data

    Description:
    clean up counter_statue column: 
        - turn strings 0-5 into int,
        - check percentage of values not 0-5,
        - check for pattern 
        - remove null values

    """

    # params = {
    #     0: 0, 1: 1, 2 : 2, 3: 3, 4: 4, 5: 5,
    #     '0': 0, '5': 5, '1': 1, '4': 4, 'A': np.nan,
    #     618: np.nan, 269375: np.nan, 46: np.nan, 
    #     420: np.nan, 769: np.nan, 
    # }
    params = {
        0: 0, 1: 1, 2 : 2, 3: 3, 4: 4, 5: 5,
        '0': 0, '5': 5, '1': 1, '4': 4, 'A': 7,
        618: np.nan, 269375: np.nan, 46: np.nan, 
        420: np.nan, 769: np.nan, 
    }

    data = column_mapper(data, params, column_name='tarif_type')

    return data


def tarrif_type_mapper(data):

    """
    :param data: object - data
    :return: object - data

    Description:

    bins tarrif_type column: 


    """

    params = {
        8: 0, 9: 0, 18: 0, 21:0, 24: 0, 
        27:0, 30: 0, 42: 0, 10: 10, 11: 11,
        12: 12, 13: 13, 14: 14, 15: 15,
        29: 29,  40: 40, 45: 45,
    }


    data = column_mapper(data, params, column_name='tarif_type')

    return data


def reading_remark_mapper(data):

    """
    :param data: object - data
    :return: object - data

    Description:

    bins column values reading remarks for meter/counter  


    """

    params = {
        5: 'anomalies',
        6: 'address_change',
        7: 'special',
        8: 'normal',
        9: 'estimated',
        203: 'replacement',
        207: 'different_size',
        413: 'maintenance',
    }

    data = column_mapper(data, params, column_name='reading_remarque')

    return data


def get_total_client_years(data:pd.DataFrame) -> pd.DataFrame:

    """
    :param data: object - data
    :return: object - data

    Description:
    Gets number of years as a client
        - member_years = invoice_date_year - creation_date_year

    """

    data['invoice_date'] = data['invoice_date'].dt.year.astype(int)
    data['creation_date'] = data['creation_date'].dt.year.astype(int)
    data['member_years'] = data['invoice_date'] - data['creation_date']

    return data




def get_index_change(data:pd.DataFrame) -> pd.DataFrame:

    """
    :param data: object - data
    :return: object - data

    Description:
    calculates and creates a new feauture for the change in index
        - index_change = new_index - old_index
    calculates and creates a new column for the index change per month
        - index_change_per_month = index_change / months_number (number of months)

    """

    data['index_change']= data['new_index'] - data['old_index']
    data['index_change_per_month']= data['index_change']/data['months_number']


    return data



def counter_quantity_per_client(data:pd.DataFrame) -> pd.DataFrame:

    """
    :param data: object - data
    :return: object - data

    Description:
    Get quantity of counter per client
        - grouby client id and counter number

    """

    data['counter_quantity'] = data.groupby('client_id')['counter_number'].count().reset_index()

    return data



def money_lost_per_fraudlent_client(data:pd.DataFrame) -> pd.DataFrame:

    """
    :param data: object - data
    :return: object - data

    Description:
    Creates column and calculate all fraudlent rate per client and also 
    creates column for money lost per fraudulent client when 
    total money lost declared as 200,000,000 tunisian dollars. 

    Assumption on cost of fraudlent activity per client based on their computed fraudulent rate,
    where total amount declared as lost for STEG = 200,000,000:
    * total number of clients in dataset = $135,493$
    * total fraudulent clients in dataset = $7566$
    * assumed fraudulent rtransactions per client :
        - calculated as such: fraudulent transactions per client = count of fraudulent transactions per client when target == 1 else fraudlent transactions = 0.
        - 
    * assumed loss per client:
        - calculated as such: assumed loss per client = fraud transactions per client multiplied by the total amount declared to be lost divided by sum of all fraud transactions
        - amount_lost_per_client = (fraudulent_transactions_per_client) * (total_amount_lost / sum of fraudulent transactions) 


    """


    total_money_lost = 200000000
    
    total_fraudulent_clients = len(data[data['target'] == 1].groupby('client_id'))
    assumed_loss_per_fraud_client = total_money_lost / total_fraudulent_clients
    print(f"Assumed loss per fraudulent client: {assumed_loss_per_fraud_client}")
    

    data['fraudulent_transactions'] = 0
    fraudulent_transactions = data[data['target'] == 1].groupby('client_id').size()
    valid_client_ids = data['client_id'].isin(fraudulent_transactions.index)
    data.loc[valid_client_ids, 'fraudulent_transactions'] = data.loc[valid_client_ids, 'client_id'].map(fraudulent_transactions)
    
    data['total_client_transactions'] = 0
    total_transactions = data.groupby('client_id').size()
    data['total_client_transactions'] = data['client_id'].map(total_transactions)

    data['amount_lost_per_client'] = 0
    data['amount_lost_per_client'] = data['fraudulent_transactions'] * (total_money_lost / data['fraudulent_transactions'].sum())

    return data





def create_new_feautures(data:pd.DataFrame) -> pd.DataFrame:

    """
    :param data: object - data
    :return: object - data

    Description:
    Function to create new column features for the energy data
        - get total number of years as a client
        - calculate and create a new feauture for the change in index
        - calculate and create a new column for the index change per month
        - create column for money lost per fraudulent 
            client when total money lost declared as 200,000,000 
    """

    data =  get_total_client_years(data)
    data =  get_index_change(data)

    data = money_lost_per_fraudlent_client(data)

    return data


        