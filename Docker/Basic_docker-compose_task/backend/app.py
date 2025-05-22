from flask import Flask
from flask_cors import CORS  # import CORS
import mysql.connector
import time

app = Flask(__name__)
CORS(app)  # enable CORS for all routes

def get_connection():
    for _ in range(10):
        try:
            conn = mysql.connector.connect(
                host='db',
                user='testuser',
                password='testpass',
                database='testdb'
            )
            return conn
        except mysql.connector.Error as err:
            print(f"Waiting for database... {err}")
            time.sleep(2)
    raise Exception("Database not reachable after retries")

@app.route('/')
def hello():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT message FROM greetings LIMIT 1")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else "No message found"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
