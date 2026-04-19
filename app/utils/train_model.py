import pandas as pd
from datetime import date
from pathlib import Path
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

from app.utils.db import get_db_connection


def load_training_data():
    conn = get_db_connection()

    query = """
    SELECT 
        m.member_id,
        m.age,
        m.membership_type,
        m.last_visit,
        COUNT(a.attendance_id) AS total_visits,
        c.churned
    FROM members m
    LEFT JOIN attendance a ON m.member_id = a.member_id
    JOIN churn_status c ON m.member_id = c.member_id
    GROUP BY m.member_id;
    """

    df = pd.read_sql(query, conn)
    conn.close()

    today = date.today()
    df["days_since_last_visit"] = df["last_visit"].apply(
        lambda x: (today - x).days if pd.notnull(x) else 999
    )

    df["membership_type"] = df["membership_type"].map({
        "monthly": 0,
        "quarterly": 1,
        "yearly": 2
    })

    df.drop(columns=["member_id", "last_visit"], inplace=True)

    return df


def train_churn_model():
    df = load_training_data()

    print("Label distribution:")
    print(df["churned"].value_counts())

    X = df.drop(columns=["churned"])
    y = df["churned"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    model = LogisticRegression()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    print(classification_report(y_test, preds))

    model_path = Path("models/churn_model.joblib")
    model_path.parent.mkdir(exist_ok=True)
    joblib.dump(model, model_path)

    print(f"Model saved at: {model_path.resolve()}")

    return model


if __name__ == "__main__":
    train_churn_model()
