# Gym Churn Analytics & Prediction System

## Overview
An end-to-end data science web application that tracks gym members,
detects churn, and predicts churn probability using machine learning.

## Screenshots

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Members Page
![Members](screenshots/members.png)

### Churn Prediction
![Prediction](screenshots/prediction.png)

### Attendance Mark
![Attendance](screenshots/attendance.png)

## How It Works

1. Member data is stored in MySQL
2. Attendance updates last_visit
3. Churn is calculated using inactivity logic
4. Features are generated for ML model
5. Logistic Regression predicts churn probability
6. Results are displayed in dashboard

## Key Features

- Member management system
- Attendance tracking
- Churn detection logic
- Machine learning prediction
- Risk classification (High/Medium/Low)
- Interactive dashboard
- Dark mode UI

## Features
- Member management
- Attendance tracking
- Churn detection logic
- Machine learning prediction
- Dashboard with insights
- Dark mode UI

## Tech Stack
- Python
- Flask
- MySQL
- Scikit-learn
- Tailwind CSS

## How to Run

```bash
git clone <your_repo_link>
cd gym-churn-analytics
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m app.app
