from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="simple_k8s_dag",
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
    catchup=False,
    schedule=None,
    tags=["k8s", "example"],
) as dag:
    # 이 Task는 스케줄러에 의해 별도의 워커 Pod로 생성되어 실행됩니다.
    task_start = BashOperator(
        task_id="start_task",
        bash_command="echo 'Starting Kubernetes Executor task!'",
    )

    # 이 Task 또한 별도의 워커 Pod로 생성됩니다.
    task_running = BashOperator(
        task_id="running_task",
        bash_command="echo 'This task is running on a pod created by KubernetesExecutor'; sleep 5",
    )

    task_end = BashOperator(
        task_id="end_task",
        bash_command="echo 'Finished task successfully!'",
    )

    task_start >> task_running >> task_end
