from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# -----------------------------------------------------------------------------------
# الدالة الأولى: طباعة تقرير الطالب
# -----------------------------------------------------------------------------------
def student_report(**kwargs):
    name = kwargs.get('name')
    scores = kwargs.get('scores', [])
    
    average = sum(scores) / len(scores) if scores else 0
    passed = average > 50

    print(f"Student: {name}")
    print(f"Scores: {scores}")
    print(f"Average: {average:.2f}")
    print(f"Passed: {'Yes' if passed else 'No'}")

# -----------------------------------------------------------------------------------
# الدالة الثانية: ترجع رقم وتخزنه في XCom
# -----------------------------------------------------------------------------------
def return_number(ti, number):
    ti.xcom_push(key='my_number', value=number)
    print(f"The Return Value: {number}")

# -----------------------------------------------------------------------------------
# الدالة الثالثة: تسحب الرقم من XCom وتحسب الناتج
# -----------------------------------------------------------------------------------
def calculate_result(ti):
    number = ti.xcom_pull(task_ids='return_number_task', key='my_number')
    result = number * number + 1
    print(f"The final result is: {result}")

# -----------------------------------------------------------------------------------
# تعريف الـ DAG الكامل
# -----------------------------------------------------------------------------------
with DAG(
    dag_id='student_and_xcom_dag',
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    # المهمة الأولى: تقرير الطالب
    report_task = PythonOperator(
        task_id='student_report_task',
        python_callable=student_report,
        op_kwargs={
            'name': 'Diea',
            'scores': [90, 90, 90]  # ممتاز، المتوسط = 90
        }
    )

    # المهمة الثانية: ترجع رقم وتخزنه في XCom
    t1 = PythonOperator(
        task_id='return_number_task',
        python_callable=return_number,
        op_kwargs={'number': 3}
    )

    # المهمة الثالثة: تسحب وتحسب الناتج
    t2 = PythonOperator(
        task_id='calculate_result_task',
        python_callable=calculate_result
    )

    # ترتيب المهام
    report_task >> t1 >> t2
