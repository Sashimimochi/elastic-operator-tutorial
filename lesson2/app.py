import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

def get_db_connection():
    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_name = os.getenv("POSTGRES_DB")
    db_host = "postgres"

    try:
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

@app.route('/')
def get_current_time():
    ENV = os.getenv("ENV")
    conn = get_db_connection()
    if conn is None:
        return "Database connection failed", 500

    cur = conn.cursor()
    try:
        cur.execute("SELECT NOW()")
        current_time = cur.fetchone()[0]
        return jsonify({
          'current_time': str(current_time),
          'env': ENV
        })
    except Exception as e:
        return str(e), 500
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
