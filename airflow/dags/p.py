from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from callables.health import scrape_health
from callables.entertainment import scrape_entertainment
from callables.politics import scrape_politics
from callables.fashion import scrape_fashion
from callables.technology import scrape_technology
from callables.sports import scrape_sports
from callables.dbt import trigger_dbt
from airflow import DAG
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 3, 19),
    'retries': 1,
}

assignment_dag = DAG(
    'assignment_dag',
    default_args=default_args,
    description='Final Project dag',
    schedule='0 9 * * *',  # Cron expression for 9 AM daily
    catchup=False  # Optionally, disable catchup if not needed
)

scrape_health_task = PythonOperator(
    task_id='scrape_health',
    python_callable=scrape_health,
    dag=assignment_dag,
)
scrape_entertainment_task = PythonOperator(
    task_id="scrape_entertainment",
    python_callable=scrape_entertainment,
    dag=assignment_dag,
)
scrape_politics_task = PythonOperator(
    task_id="scrape_politics",
    python_callable=scrape_politics,
    dag=assignment_dag,
)

scrape_fashion_task = PythonOperator(
    task_id="scrape_fashion",
    python_callable=scrape_fashion,
    dag=assignment_dag,
)

scrape_technology_task = PythonOperator(
    task_id="scrape_technology",
    python_callable=scrape_technology,
    dag=assignment_dag,
)


scrape_sports_task = PythonOperator(
    task_id="scrape_sports",
    python_callable=scrape_sports,
    dag=assignment_dag,
)



dbt_trigger_task = PythonOperator(
        task_id='get_dbt_status',
        python_callable=trigger_dbt,  # Use the dbt_status() function
    )



# Task dependencies
scrape_entertainment_task >> scrape_fashion_task >> scrape_health_task >> scrape_politics_task >> scrape_sports_task  >> scrape_technology_task >> dbt_trigger_task



