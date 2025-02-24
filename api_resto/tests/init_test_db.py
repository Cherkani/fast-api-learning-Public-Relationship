import mysql.connector
from .test_config import TestConfig

def init_test_db():
    # Connect to MySQL server
    conn = mysql.connector.connect(
        host=TestConfig.db_host,
        user=TestConfig.db_user,
        password=TestConfig.db_password
    )
    cursor = conn.cursor()

    # Create test database if it doesn't exist
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {TestConfig.db_name}")
    
    # Close connection
    cursor.close()
    conn.close()

if __name__ == "__main__":
    init_test_db()
