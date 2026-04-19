import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="@adityA12",
        database="gym_churn_db"
    )
