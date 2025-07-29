from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.dummy import DummyOperator
import json
from datetime import datetime

def addition_5(**kwargs):
    y = [1 , 3 , 4, 7, 10]
    kwargs['ti'].xcom_push(key='table20', value=json.dumps(y))
    return y


def choose_the_branch(**kwargs):
    x = kwargs['ti'].xcom_pull(task_ids = 'addition5' , key='table20')
    x = json.loads(x)
    returnmytask1 = False
    for number in x:
        if number > 9:
            returnmytask1 = True
    if returnmytask1:
        return 'task_1'
    else:
        return 'task_2'


with DAG(
    dag_id = 'branch_task',
    start_date = datetime(2025,1,1),
    schedule_interval = '0 20 * * 1',
    catchup = False
) as dag:
    
    start = DummyOperator(
        task_id = 'start_my_task'
    )
    
    my_addition = PythonOperator(
        task_id='addition5',
        python_callable=addition_5,
        provide_context = True
    )

    my_branch = BranchPythonOperator(
        task_id='branch_task',
        python_callable=choose_the_branch,
        provide_context = True
    )
    
    task1 = BashOperator(
        task_id = 'task_1',
        bash_command = 'echo task1 OK'
    )

    task2 = BashOperator(
        task_id = 'task_2',
        bash_command = 'echo task2 OK'
    )

    task3 = BashOperator(
        task_id = 'task_3',
        bash_command = 'echo task3 OK',
        trigger_rule='none_failed_min_one_success'
    )

    end = DummyOperator(
        task_id = 'end_my_task'
    )

    start >> my_addition >> my_branch >> [task1, task2] >> task3 >> end