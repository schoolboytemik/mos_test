from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="etl_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["etl"],
) as dag:

    normalize = BashOperator(
        task_id="normalize",
        bash_command="""
        cd /opt/airflow &&
        python src/transform/normalize.py
        """
    )

    load_raw = BashOperator(
        task_id="load_raw",
        bash_command="""
        cd /opt/airflow &&
        python src/load_raw.py
        """
    )

    load_sor = BashOperator(
        task_id="load_sor",
        bash_command="""
        cd /opt/airflow &&
        python src/load_sor.py
        """
    )

    normalize >> load_raw >> load_sor