"""
script : tests.py 
purpose: 


"""


# Importing necessary libraries and modules 

import subprocess

try:

    import os
    import pandas as pd
    import numpy as np
    import unittest
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
from dataloader import (
                load_data,
                )

from dataprocessor import (
                read_combine_dataframe,
                data_wrangling,
                read_dataset,
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




def test_data_loading():
    """
    :param : 
    :return: 

    Description:
    Dataloading test
        - read and combine data fn test
        - check it is not empty 
        - verify it is a dataframe

    """   
    
    data = read_combine_dataframe(data)
    assert data is not None
    assert isinstance(data, pd.DataFrame)



def test_data_wrangling():
    """
    :param : 
    :return: 

    Description:
    data preprocessing - wrangling test
        - read_ data
        - data wrangling fn 
        - check it is not empty 
        - verify it is a dataframe

    """    

    data = read_combine_dataframe(data)
    data = data_wrangling(data)
    assert data is not None
    assert isinstance(data, pd.DataFrame)


def test_feature_engineering():
    """
    :param : 
    :return: 

    Description:
    Feature engineering test
        - read_ data
        - create new features
        - check it is not empty 
        - verify it is a dataframe

    """

    data = read_combine_dataframe(data)
    data = create_new_feautures(data)
    assert data is not None
    assert isinstance(data, pd.DataFrame)




def test_ml_modelling():
    """
    :param : 
    :return: 

    Description:
    ml modellingtest
        - read_ data
        - create new features
        - check it is not empty 
        - verify it is a dataframe

    """   

    data = read_combine_dataframe(data)
    #model = 
    #assert model is not None
    pass 




@profile
def test_main():
    """
    :param : 
    :return: 

    Description:
    main test fn 
        - test_data_loading
        - test_data_wrangling
        - test_feature_engineering 
        - test_ml_modelling
    """   

    test_data_loading()
    test_feature_engineering()
    test_data_wrangling()
    test_ml_modelling
    
    print(f'''done!''')




if __name__ == '__main__':

    test_main()