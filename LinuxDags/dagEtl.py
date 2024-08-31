from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from azureEtl import run_etl  # Importa función ETL

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1,
}

dag = DAG(
    'subiendo_silver',
    default_args=default_args,
    description='ETL DAG para Clickstream Data hacia capa Silver',
    schedule_interval='@daily',
)

etl_task = PythonOperator(
    task_id='run_etl',
    python_callable=run_etl,
    dag=dag,
)

etl_task
