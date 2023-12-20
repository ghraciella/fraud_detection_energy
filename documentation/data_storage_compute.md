# Data Storage: 

* Using cloud services for data storage and compute
    - depending on which service: AWS or GCP



* Manual Setup Process: Accessing Google Cloud Platfrom and Modules
* Manual Setup Process: Data Warehouse and Data Lakes Creation via  Google Cloud UI
* Python Support for Google Cloud Storage Module 
* Terraform: Data Warehouse and Data Lakes Creation
* Manual Setup Process: Accessing AWS and services
* ...

<br/>

___





## Manual Setup Process: Accessing Google Cloud Platfrom and Modules

* `google-cloud` package: It is a large collection of modules used to interact with services on the Google Cloud Platform (GCP).

    ```bash
    # Installation

    pip install -U google-cloud

    ```
    
    - download the google cloud sdk for command line usage 

* `setup service account to get application credentials`: to do this, connect to GCS with credentials (Service Account or IAM)

    ```markdown
    # service account setup

    * within <project folder> on GCP console --> navigation menu ≡ --> IAM and Admin  --> service accounts --> create service account  --> <create the service account>.

    ```


* `gcs_credentials.json` file: get and store google cloud credentials (gcs credentials as json file) in working directory (could take the name of your project folder). 

    ```markdown
    # get and store credential from gcp console

    * service account --> <the ⋮ of service account created> --> manage keys --> add key --> create new key --> json --> create --> download json <to /your/credentials/folder> --> close.

    ```

* `specify service account permissions`: specify permissions and resources the service account can access

    ```markdown
    # specify service account permissions

    * IAM and Admin --> IAM --> edit <created service account> principal --> add roles --> save changes. 

    ```

* `roles that can be added`:  

    ```markdown
    # roles that could be added to service account

    * BigQuery:  access and control to resources, datasets, job submissions and details
        - bigquery admin
        - bigquery data owner
        - bigquery data editor
        - bigquery user
        - bigquery job user
    * Cloud Storage: access to resources and creation of objects in buckets
        - storage admin
        - storage object admin
        - storage object creator
        - storage object viewer    
    * AI Platform: resources, ai models creation and management, jobs
        - ml admin
        - ml developer
    * Compute Engine:
        - compute admin
        - compute instance admin
        - compute viewer

    .... etc etc

    ```


<br/>

___

## Manual Setup Process: Data Warehouse and Data Lakes Creation via  Google Cloud UI


* `Data Lake`:  storage repo for big data - raw in native form (structure, semi-structured, and unstructure) using <schema on read> to map structure dynamically when data is needed.

    ```markdown
    # datalakes: create GCS storage bucket

    * cloud storage --> create --> <specify bucket name> --> choose <bucket options> as needed --> create <data lake bucket>.
        - <bucket name> should be globally unique.

    * recommended options
        - location type: region
        - storage class: standard
        - activate enforce public access prevention
        - access control: uniform
        - protection tools`: none        

    ```


* `Data Warehouse`:  

    ```markdown
    # data warehouse: create google database and table

    * bigquery --> <the ⋮ of project name> --> create dataset --> <specify dataset name> --> create <dataset>.
        - <dataset name> should be globally unique.

    * <the ⋮ of created dataset> --> create table --> select data source --> <empty table> --> <specify table name> --> define schema --> create <table>.

    * load data   

    ```


<br/>

___




## Terraform: Data Warehouse and Data Lakes Creation

* create bucket and warehouse easily
* reproducibility error reduction in production

* ... TBA


<br>

---
---

## Manual Setup Process: Accessing AWS and services

* `boto3` : It is the offical AWS sdk for python.

    ```bash
    # Installation

    pip install boto3
    ```

* `setup account to get credentials`: to do this, connect to [AWS management console](https://aws.amazon.com/).

    ```markdown
    # service account setup

    * on AWS console --> IAM (Identity and Access Management) service --> create IAM user
    * to create IAM user --> IAM dashboard --> <users> --> click <create user> --> set username --> (optional) check <provide user access> box, <programmatic access> --> set permisions for user --> complete.
    * if you choose <specify a user in identity center> --> takes you to IAM identity center console --> enable identity center --> IAM dashboard --> <users> --> click <add user> --> set user details (username, email to send pasweord set up instructions etc) --> add user to group --> review and add user --> complete.

    ```



* `aws_credentials.csv` file: get and store aws credentials (access keys). Use access keys to send programmatic calls to AWS from the AWS CLI, AWS Tools for PowerShell, AWS SDKs, or direct AWS API calls. You can have a maximum of two access keys (active or inactive) at a time

    ```markdown
    # get and store credential from aws console

    * IAM --> users --> choose IAM user --> security credentials --> acess keys --> create <access key> --> choose use case --> store user's <access key id> and <secret access key> --> csv with credentials -->  download csv <to /your/credentials/folder> --> close.

    ```

* `aws cli`: aws command line interface (cli) to interact with aws services on terminal

    * configuration: using the credentials to configure the aws cli in terminal

    ```markdown
    # configuration 

    brew install awscli

    aws --version

    aws configure

    # prommpt
    - enter access key id, secrete access key, default region and default output format

    AWS Access Key ID [****************]:
    AWS Secret Access Key [****************]:
    Default region name [eu-central-1]:
    Default output format [None]:

    # list buckets
    aws s3 ls

    ```




<br/>

___



