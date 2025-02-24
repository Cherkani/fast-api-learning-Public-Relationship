import mysql.connector
from .test_config import TestConfig

def init_test_db():
    conn = mysql.connector.connect(
        host=TestConfig.db_host,
        user=TestConfig.db_user,
        password=TestConfig.db_password
    )
    cursor = conn.cursor()

   
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {TestConfig.db_name}")
   
    cursor.close()
    conn.close()

if __name__ == "__main__":
    init_test_db()
