# Fraud Detection : Energy Finacial Data




## Requirements and Environment

Requirements:
- pyenv with Python: 3.11.3

Environment: 

For installing the virtual environment you can either use the Makefile and run `make setup` or install it manually with the following commands: 

```bash
# to setup venv and install requirements
make setup 
source .venv/bin/activate

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

## Limitations

Development libraries are part of the production environment, normally these would be separate as the production code should be as slim as possible.


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