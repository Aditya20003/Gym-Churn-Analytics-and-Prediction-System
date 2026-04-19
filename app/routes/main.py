from flask import Blueprint, render_template, request, redirect, url_for
from app.utils.db import get_db_connection

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM members")
    total_members = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM churn_status WHERE churned = 1")
    churned_members = cursor.fetchone()[0]

    conn.close()
    return render_template(
        "home.html",
        total_members=total_members,
        churned_members=churned_members
    )

@main_bp.route("/members")
def members():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members")
    data = cursor.fetchall()
    conn.close()
    return render_template("members.html", members=data)
@main_bp.route("/add-member", methods=["GET", "POST"])
def add_member():
    if request.method == "POST":
        full_name = request.form["full_name"]
        age = request.form["age"]
        gender = request.form["gender"]
        membership_type = request.form["membership_type"]
        join_date = request.form["join_date"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO members (full_name, age, gender, membership_type, join_date, last_visit)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (full_name, age, gender, membership_type, join_date, join_date)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("main.members"))

    return render_template("add_member.html")
@main_bp.route("/add-attendance", methods=["GET", "POST"])
def add_attendance():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        member_id = request.form["member_id"]
        visit_date = request.form["visit_date"]

        cursor.execute(
            "INSERT INTO attendance (member_id, visit_date) VALUES (%s, %s)",
            (member_id, visit_date)
        )

        cursor.execute(
            "UPDATE members SET last_visit = %s WHERE member_id = %s",
            (visit_date, member_id)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("main.members"))

    cursor.execute("SELECT member_id, full_name FROM members")
    members = cursor.fetchall()
    conn.close()

    return render_template("add_attendance.html", members=members)
@main_bp.route("/run-churn")
def run_churn():
    from app.utils.churn import calculate_churn
    calculate_churn()
    return "Churn calculation completed"
@main_bp.route("/churn-dashboard")
def churn_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT m.full_name, m.last_visit, c.churned
        FROM members m
        JOIN churn_status c ON m.member_id = c.member_id
    """)

    data = cursor.fetchall()
    conn.close()

    return render_template("churn_dashboard.html", members=data)
@main_bp.route("/churn-predictions")
def churn_predictions():
    from app.utils.model import load_model
    import pandas as pd
    from datetime import date

    model = load_model()
    conn = get_db_connection()

    query = """
    SELECT 
        m.member_id,
        m.full_name,
        m.age,
        m.membership_type,
        m.last_visit,
        COUNT(a.attendance_id) AS total_visits
    FROM members m
    LEFT JOIN attendance a ON m.member_id = a.member_id
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

    features = df[["age", "membership_type", "total_visits", "days_since_last_visit"]]
    probs = model.predict_proba(features)[:, 1]

    df["churn_probability"] = probs

    results = df[["full_name", "churn_probability"]].values.tolist()

    return render_template("churn_predictions.html", results=results)
@main_bp.route("/debug")
def debug():
    return "Blueprint routes are working"


