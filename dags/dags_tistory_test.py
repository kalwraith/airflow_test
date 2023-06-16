from airflow import DAG
import pendulum
from datetime import timedelta
from operators.tistory_write_post_by_chatgpt_operator import TistoryWritePostByChatgptOperator

with DAG(
    dag_id='dags_tistory_test',
    start_date=pendulum.datetime(2023, 5, 1, tz='Asia/Seoul'),
    catchup=False,
    schedule=None,
    dagrun_timeout=timedelta(minutes=1),
) as dag:
    tistory = TistoryWritePostByChatgptOperator(
        task_id='tistory',
    )