
"""
script : config.py 
purpose: 


"""

# Importing necessary libraries and modules 

import subprocess

try:

    import os

    # env/configuration files
    from dotenv import load_dotenv, dotenv_values

    # experimentation, monitoring and tracking
    import mlflow


except ImportError as error:
    print(f"Installation of the required dependencies necessary! {error}")

    subprocess.check_call(["pip", "install", "python-dotenv"])
    subprocess.check_call(["pip", "install", "mlflow"])


    print(f"Successful installation of the required dependencies necessary")







def get_config(needed_keys):

    '''
    Function loads configuration details for services
        from .env file and returns a dictionary containing the data needed.

    :param : 
    :return: object - configuration dictionary

    Description:

    '''

    dotenv_dict = dotenv_values(".env")
    service_config = {key:dotenv_dict[key] for key in needed_keys if key in dotenv_dict}

    return service_config 



def get_sql_config():
    '''
    Function loads credentials from .env file and
        returns a dictionary containing the data needed for sqlalchemy.create_engine()

    :param : 
    :return: object - configuration dictionary

    Description:

    '''
    needed_keys = ['host', 'port', 'database','user','password', 'db_url']
    #needed_keys = ['host', 'port', 'database','password', 'db_url']

    dotenv_dict = dotenv_values(".env")
    sql_config = {key:dotenv_dict[key] for key in needed_keys if key in dotenv_dict}
    return sql_config


def get_kaggle_config():
    '''
    Function loads configuration details for kaggle api
        from .env file and returns a dictionary containing the data needed.


    :param : 
    :return: object - configuration dictionary

    Description:

    '''

    needed_keys = ['kaggle_username', 'kaggle_api_key']
    kaggle_config = get_config(needed_keys)

    return kaggle_config


def get_gsc_config():
    '''
    Function loads configuration details for google cloud BigQuery
        from .env file and returns a dictionary containing the data needed.

    :param : 
    :return: object - configuration dictionary

    Description:


    '''

    needed_keys = ['project_id', 'dataset_id', 'table_id']
    gsc_config = get_config(needed_keys)

    return gsc_config 


def get_aws_config():
    '''
    Function loads configuration details for AWS
        from .env file and returns a dictionary containing the data needed.

    :param : 
    :return: object - configuration dictionary

    Description:


    '''

    needed_keys = ['aws_access_key_id', 'aws_secret_access_key', 'aws_region']
    aws_config = get_config(needed_keys)

    return aws_config 


def get_rds_config():
    '''
    Function loads configuration details for AWS RDS instance
        from .env file and returns a dictionary containing the data needed.

    :param : 
    :return: object - configuration dictionary

    Description:


    '''

    needed_keys = ['db_instance_name', 'master_username', 'master_password', \
                    'db_name', 'allocated_storage', 'instance_class', 'engine', 'engine_version']
    rds_config = get_config(needed_keys)

    return rds_config 

def get_pgrds_config():
    '''
    Function loads configuration details for AWS RDS instance
        from .env file and returns a dictionary containing the data needed.

    :param : 
    :return: object - configuration dictionary

    Description:


    '''

    needed_keys = ['pg_username', 'pg_host', 'pg_port', 'pg_db_name', 'pg_password', 'pg_db_url']
    
    pg_rds_config = get_config(needed_keys)

    return pg_rds_config 



def get_mlflow_config():
    '''
    Function loads configuration details for mlflow
        from .env file and returns a dictionary containing the data needed.
    

    :param : 
    :return: object - configuration dictionary

    Description:

    '''

    needed_keys = ['MLFLOW_TRACKING_URI', 'MLFLOW_EXPERIMENT_NAME']
    mlflow_config = get_config(needed_keys)

    return mlflow_config



def load_mlflow_config():

    """
    function to load mlflow configurations from .env file

    :param : 
    :return: object - configuration dictionary

    Description:

    tracking_uri : 'MLFLOW_TRACKING_URI'
    experiment_name: 'MLFLOW_EXPERIMENT_NAME'

    """

    mlflow_config = mlflow_config()

    tracking_uri = mlflow_config['MLFLOW_TRACKING_URI']
    experiment_name = mlflow_config['MLFLOW_EXPERIMENT_NAME']
    
    return tracking_uri, experiment_name


def initialize_mlflow(tracking_uri, experiment_name):
    """
    function to start mlflow for tracking

    :param tracking_uri: 
    :param experiment_name: 

    :print: 

    Description:

    """

    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)

    print(f"MLflow initialization successful!")


