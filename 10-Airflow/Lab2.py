from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime

with DAG(
    dag_id='student_management_dag',
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,  
    catchup=False,
) as dag:

    create_students_table = PostgresOperator(
        task_id='create_students_table',
        postgres_conn_id='postgres_conn',
        sql="""
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            name TEXT,
            age INTEGER,
            city TEXT
        );
        """
    )

    insert_students = PostgresOperator(
        task_id='insert_students',
        postgres_conn_id='postgres_conn',
        sql="""
        INSERT INTO students (name, age, city) VALUES
            ('Ahmed', 24, 'Cairo'),
            ('Sara', 22, 'Giza'),
            ('Youssef', 27, 'Alexandria'),
            ('Mariam', 29, 'Mansoura'),
            ('Tarek', 25, 'Tanta');
        """
    )

    delete_older_students = PostgresOperator(
        task_id='delete_older_students',
        postgres_conn_id='postgres_conn',
        sql="""
        DELETE FROM students
        WHERE age > 26;
        """
    )

    create_students_table >> insert_students >> delete_older_students
