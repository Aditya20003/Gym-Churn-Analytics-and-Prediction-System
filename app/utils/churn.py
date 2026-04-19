from datetime import date
from app.utils.db import get_db_connection

def calculate_churn():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT member_id, last_visit FROM members")
    members = cursor.fetchall()

    today = date.today()

    cursor.execute("DELETE FROM churn_status")

    for member_id, last_visit in members:
        if last_visit is None:
            churned = 1
        else:
            days_inactive = (today - last_visit).days
            churned = 1 if days_inactive > 30 else 0

        cursor.execute(
            "INSERT INTO churn_status (member_id, churned) VALUES (%s, %s)",
            (member_id, churned)
        )

    conn.commit()
    conn.close()
