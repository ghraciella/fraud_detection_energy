
"""
script : storage.py 
purpose: 


    - storage on cloud (AWS or GCP)
    


"""


# Importing necessary libraries and modules 

import subprocess

try:

    import os
    import boto3
    from dotenv import dotenv_values, load_dotenv

    import psycopg2
    import sqlalchemy
    from sqlalchemy import create_engine


except ImportError as error:
    print(f"Installation of the required dependencies necessary! {error}")

    subprocess.check_call(["pip", "install", "python-dotenv"])


    print(f"Successful installation of the required dependencies necessary")


import warnings
warnings.filterwarnings('ignore')


# custom imports
from config import (
                get_aws_config,
                get_rds_config,
                get_pgrds_config,
                )



def configure_aws_session():

    """
    configure access to aws using credentials


    :param: 
    :return: object session object

    Description:
    
    """

    aws_credentials = get_aws_config()

    session = boto3.Session(
        aws_access_key_id = aws_credentials['aws_access_key_id'],
        aws_secret_access_key = aws_credentials['aws_secret_access_key'],
        region_name = aws_credentials['aws_region']
        )
    
    return session







def create_aws_data_lake(session, data_files_path, bucket_name= 'fraud_detection_datasets'):

    """
    data lake creation and file storage 


    :param: 
    :return: object - connection engine object

    Description:

    data lake creation : amazon S3
        - initialize S3 client
        - create S3 bucket for data lake
        - get data from data sources or data file
        - upload and store data in s3
    """
    
    s3 = session.client('s3')
    s3.create_bucket(Bucket=bucket_name)

    for path in data_files_path:
        file_name = path.split('/')[-1]
        file_exists = False

        objects = s3.list_objects_v2(Bucket=bucket_name)

        if 'Contents' in objects:
            file_exists = any(obj['Key'] == file_name for obj in objects.get('Contents', []))
        print(f'{file_name} already exists: {file_exists}')

        if not file_exists:
                s3.upload_file(path, bucket_name, file_name)



def create_data_warehouse():

    """
    data warehouse creation: aws rds (relational ) postgresql instance

    :param: 
    :return: 

    Description:
        - get rds configurations
        - initialize rds client
        - create rds instance
    
    """

    rds_config = get_rds_config()
    rds = boto3.client('rds', region_name='us-east-1')

    try: 
    
        response = rds.describe_db_instances(DBInstanceIdentifier=rds_config['db_instance_name'])
        if 'DBInstances' in response and len(response['DBInstances']) > 0:

            # # postgresql RDS: connection parameters
            # db_instance = response['DBInstances'][0]
            # dbname = db_instance['DBName']
            # username = db_instance['MasterUsername']
            # endpoint = db_instance['Endpoint']['Address']
            # port =  db_instance['Endpoint']['Port']
            
            # db_config =  {
            #     'db_instance': db_instance,
            #     'dbname': dbname,
            #     'username': username,
            #     'endpoint': endpoint,
            #     'port': port,
            #     }
            print("RDS instance exist, response returned")

    except rds.exceptions.DBInstanceNotFoundFault:

        print("RDS instance does not exist. Creating a new PostgreSQL RDS instance...")
        response = rds.create_db_instance(
                        DBInstanceIdentifier=rds_config['db_instance_name'],
                        MasterUsername=rds_config['master_username'],
                        MasterUserPassword=rds_config['master_password'],
                        DBName=rds_config['db_name'],
                        AllocatedStorage=int(rds_config['allocated_storage']),
                        DBInstanceClass=rds_config['instance_class'],
                        Engine=rds_config['engine'],
                        EngineVersion=rds_config['engine_version'],
                    )

        #waiter = rds.get_waiter('db_instance_available')
        #waiter.wait(DBInstanceIdentifier=rds_config['db_instance_name'])

    return  response #db_config



    
    pass

def create_db_tables(config, sql_queries, schema_name='fraud_data_schema', driver= 'psycopg2',*args, **kwargs):

    """
    psycopg2 driver (PSQL adapter) - function to create a connection to the PostgreSQL RDS


    :param: 
    :return: 

    Description:
    

    - create tables in the postgresql database in aws
    
    """

    pg_config = get_pgrds_config()

    #conn_engine = psycopg2.connect(**config)

    # try:
    #     conn_engine = psycopg2.connect(
    #         dbname=pg_config['pg_db_name'],
    #         user=pg_config['pg_username'],
    #         host=pg_config['pg_host'],
    #         port=pg_config['pg_port'],
    #         password=pg_config['pg_password']
    #     )
    #     print("Connection Sucessful!")
    # except (Exception, psycopg2.Error) as error:
    #     print(error)

    # cursor = conn_engine.cursor(name='streaming_cursor', cursor_factory=psycopg2.extras.DictCursor)

    # for query in sql_queries:
    #     cursor.execute(query)

    # conn_engine.commit()
    # cursor.close()
    # conn_engine.close()

    # print(f"done!")

    if driver == 'psycopg2':
        db_url = pg_config["pg_db_url"]
    else:
        db_url = f'''postgresql://{pg_config['pg_username']}:{pg_config['pg_password']}@{pg_config['pg_host']}:{pg_config['pg_port']}/{pg_config['pg_db_name']}'''

    grant_access = f'''GRANT CONNECT ON DATABASE {pg_config['pg_db_name']} TO {pg_config['pg_username']};'''
    grant_access_query =f'''GRANT CREATE, USAGE ON SCHEMA {schema_name} TO {pg_config['pg_username']};'''


    try:
        engine = create_engine(db_url)
        print("Connection Sucessful!")


        with engine.connect() as conn_engine:
            conn_engine.execute(grant_access_query)
            print("Access granted succesfully!")

            for query in sql_queries:
                conn_engine.execute(query)
        print("Queries executed succesfully!")

    except (Exception, sqlalchemy.exc.SQLAlchemyError) as error:
        print(error)
    finally:
        if engine:
            engine.dispose()
        print("Connection engine closed successfully")







def load_data_db_tables(session, config, data_files_path, bucket_name= 'fraud_detection_datasets'):

    """
    load data from the data lake (s3 bucket) into the PostgreSQL RDS tables


    :param: 
    :return: 

    Description:
    

    - create tables in the postgresql database in aws
    
    """

    s3 = session.client('s3')

    #conn_engine = psycopg2.connect(**config)

    pg_config = get_pgrds_config()

    try:
        conn_engine = psycopg2.connect(
            dbname=pg_config['pg_db_name'],
            user=pg_config['pg_username'],
            host=pg_config['pg_host'],
            port=pg_config['pg_port'],
            password=pg_config['pg_password']
        )
        print("Connection Sucessful!")
    except (Exception, psycopg2.Error) as error:
        print(error)


    cursor = conn_engine.cursor(name='streaming_cursor', cursor_factory=psycopg2.extras.DictCursor)

    for path in data_files_path:
        file_name = path.split('/')[-1]
        file_exists = False

        objects = s3.list_objects_v2(Bucket=bucket_name)

        if 'Contents' in objects:
            file_exists = any(obj['Key'] == file_name for obj in objects.get('Contents', []))

            if file_exists:
                load_db_query = f'''
                        COPY {file_name.split('.')[0]} 
                        FROM 's3://{bucket_name}/{file_name}' 
                        CSV HEADER;
                        '''
                cursor.execute(load_db_query)
                conn_engine.commit()

        cursor.close()
        conn_engine.close()    

    print(f"done!")




