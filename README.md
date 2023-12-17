# Fraud Detection : Energy Financial Data (Utility Transactions)

* __Company__ : `STEG - Société Tunisienne de L'Électricité et du Gaz`
* __Problem__ : The  company  suffered  tremendous  losses  in  the  order  of  `$200$  million Tunisian Dinars` due to fraudulent manipulations of meters by consumers.

* __Objective__ : 
    - Build  a  model  to  predict  clients  that  are  likely  committing  fraud  by manipulation of their gas or electricity meters. 
    - Our goal is to apply machine learning to correctly predict fraud (prevent financial  damage  for  the  company)  while  limiting  the  number  of  falsely accused clients (prevent reputation damage).

        ![objective stakeholder presentation](/images/base_objective.png)


<br>

* __Potential business value analysis__
    - based on assumption :  $26434$ Tunisian Dinars loss per fraudulent client 


        ![business value stakeholder presentation](/images/initial_business_value_analysis.png)


        ![frequency of fraudlent activities stakeholder presentation](/images/fraud_frequency_demo.png)

    
    - the fraud rate per client is also computed to estimate the total money each client defrauded the company of.
    - 

<br>


---

## Meet the Team

![team graphics designed on canva](/images/team_graphics.png)

<br>

---

## Requirements and Environment

Requirements:
- pyenv with Python: 3.11.3

Environment: 

For installing the virtual environment you can either use the Makefile and run `make setup`

```bash
# to setup venv and install requirements
make setup 
source .venv/bin/activate

```

or install it manually with the following commands: 

```bash
# to setup venv and install requirements
pyenv local 3.11.3
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

```

## Usage

In order to train the model and store test data in the data folder and the model in models run:

```bash
#activate env
source .venv/bin/activate

python example/train.py  
```

In order to test that predict works on a test set you created run:

```bash
python example/predict.py models/linear_regression_model.sav data/X_test.csv data/y_test.csv
```


## Project Structure

```bash

fraud_detection_energy_project/
├── data/
│   ├── raw/
│   └── processed/
│  
├── documentation/
│   ├── data_card.md
│   └── data_pipeline_modelling.md
│  
├── images/
│   
├── notebooks/
│   ├── stakeholder_presentation_fraud_detection.pdf
│   ├── energy_fraud_detection.pdf
│   └── ...
│   
├── presentation/
│   ├── stakeholder_presentation_fraud_detection.pdf
│   ├── energy_fraud_detection.pdf
│   └── ...
│  
├── src/
│   ├── data_processing.py
│   ├── models.py
│   ├── Dockerfile
│   ├── model_training.py
│   ├── model_evaluation.py
│   ├── model_test_predict.py
│   ├── model_deployment_monitoring.py
│   ├── Dockerfile
│   └── detect.py
│  
├── services/
│   ├── airflow/
│   │   ├── airflow_dags/
│   │   ├── airflow_configs/
│   │   ├── etl_workflow.py
│   │   ├── model_training_workflow.py
│   │   └── Dockerfile
│   ├── pyspark_scripts/
│   │   ├── data_preprocessing.py
│   │   ├── analysis.py
│   │   └── Dockerfile
│   └── db/ # postgres
│       ├── create_tables.sql
│       ├── queries.sql
│       └── Dockerfile
│  
├── Makefile
├── docker-compose.yml
├── requirements.txt
└── README.md


```



## Limitations

Development libraries are part of the production environment, normally these would be separate as the production code should be as slim as possible.

