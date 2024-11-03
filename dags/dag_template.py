"""
DAG Template
"""

from datetime import datetime, timedelta
from airflow.decorators import dag, task


default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

@dag(
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['template'],
    default_args=default_args,
)
def dag_template():
    
    @task()
    def extract():
        return {"data": "example"}
    
    @task()
    def transform(input_data: dict):
        return {"processed_data": input_data["data"].upper()}
    
    @task()
    def load(transformed_data: dict):
        print(f"Loading data: {transformed_data}")
    
    # Define the task dependencies
    load(transform(extract()))


# Call the DAG function to register it with Airflow
dag_template()

