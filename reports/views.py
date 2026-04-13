from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_required
from django.db import connection
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import csv


# -------------------------------------------------------
# Helper function — run raw SQL and return DataFrame
# This covers: Raw SQL, GROUP BY, HAVING, Aliases
# -------------------------------------------------------
def run_query(sql, params=None):
    with connection.cursor() as cursor:
        cursor.execute(sql, params or [])
        columns = [col[0] for col in cursor.description]
        rows    = cursor.fetchall()
    return pd.DataFrame(rows, columns=columns)


# -------------------------------------------------------
# Main Reports Dashboard
# -------------------------------------------------------
@login_required
@admin_required
def reports_dashboard(request):

    # --- 1. Monthly Revenue using raw SQL + Pandas ---
    revenue_sql = """
        SELECT
            DATE_FORMAT(created_at, '%%Y-%%m') AS month,
            SUM(total_amount)                  AS total_revenue,
            COUNT(*)                           AS total_bills,
            AVG(total_amount)                  AS avg_bill
        FROM billing_bill
        WHERE payment_status = 'paid'
        GROUP BY DATE_FORMAT(created_at, '%%Y-%%m')
        ORDER BY month DESC
        LIMIT 6
    """
    revenue_df = run_query(revenue_sql)

    # --- 2. Doctor Performance using raw SQL ---
    doctor_sql = """
        SELECT
            CONCAT(u.first_name, ' ', u.last_name) AS doctor_name,
            d.specialization,
            COUNT(a.id)                            AS total_appointments,
            SUM(CASE WHEN a.status = 'completed'
                THEN 1 ELSE 0 END)                 AS completed,
            SUM(CASE WHEN a.status = 'cancelled'
                THEN 1 ELSE 0 END)                 AS cancelled
        FROM doctors_doctor d
        JOIN accounts_user u ON d.user_id = u.id
        LEFT JOIN appointments_appointment a ON a.doctor_id = d.id
        GROUP BY d.id, u.first_name, u.last_name, d.specialization
        HAVING total_appointments > 0
        ORDER BY total_appointments DESC
    """
    doctor_df = run_query(doctor_sql)

    # --- 3. Patient Statistics using raw SQL ---
    patient_sql = """
        SELECT
            gender,
            COUNT(*)    AS total,
            AVG(
                TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE())
            )           AS avg_age
        FROM patients_patient
        GROUP BY gender
    """
    patient_df = run_query(patient_sql)

    # --- 4. Appointment Status Summary ---
    appt_sql = """
        SELECT
            status,
            COUNT(*) AS total
        FROM appointments_appointment
        GROUP BY status
        ORDER BY total DESC
    """
    appt_df = run_query(appt_sql)

    # --- 5. Numpy calculations on revenue ---
    # Using Numpy from your PDF!
    if not revenue_df.empty and 'total_revenue' in revenue_df.columns:
        revenue_values = revenue_df['total_revenue'].astype(float).values
        revenue_stats  = {
            'total' : float(np.sum(revenue_values)),
            'avg'   : round(float(np.mean(revenue_values)), 2),
            'max'   : float(np.max(revenue_values)),
            'min'   : float(np.min(revenue_values)),
        }
    else:
        revenue_stats = {
            'total': 0, 'avg': 0, 'max': 0, 'min': 0
        }

    # --- 6. Convert DataFrames to lists for template ---
    # Using built-in functions — list(), zip()
    context = {
        'revenue_data'  : revenue_df.to_dict('records') if not revenue_df.empty else [],
        'doctor_data'   : doctor_df.to_dict('records') if not doctor_df.empty else [],
        'patient_data'  : patient_df.to_dict('records') if not patient_df.empty else [],
        'appt_data'     : appt_df.to_dict('records') if not appt_df.empty else [],
        'revenue_stats' : revenue_stats,
    }

    return render(request, 'reports/dashboard.html', context)


# -------------------------------------------------------
# Export Patient List as CSV — File I/O from your PDF!
# -------------------------------------------------------
@login_required
@admin_required
def export_patients_csv(request):
    # Create HTTP response with CSV content type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = \
        'attachment; filename="patients_report.csv"'

    # File I/O — writing to CSV using Python's built-in csv module
    writer = csv.writer(response)

    # Write header row
    writer.writerow([
        'ID', 'First Name', 'Last Name',
        'Email', 'Phone', 'Gender',
        'Blood Group', 'Age', 'Registered On'
    ])

    # Raw SQL for patient export
    patient_export_sql = """
        SELECT
            id,
            first_name,
            last_name,
            email,
            phone,
            gender,
            blood_group,
            TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) AS age,
            DATE_FORMAT(created_at, '%%d-%%m-%%Y')        AS registered
        FROM patients_patient
        ORDER BY created_at DESC
    """
    df = run_query(patient_export_sql)

    # Write each row — using iterrows() from Pandas
    for _, row in df.iterrows():
        writer.writerow([
            row['id'],
            row['first_name'],
            row['last_name'],
            row['email'],
            f"'{row['phone']}",    # apostrophe forces Excel to treat as text
            row['gender'].title(), # capitalize — Male not male
            row['blood_group'],
            row['age'],
            row['registered']
        ])

    return response


# -------------------------------------------------------
# Export Revenue Report as CSV
# -------------------------------------------------------
@login_required
@admin_required
def export_revenue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = \
        'attachment; filename="revenue_report.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Month', 'Total Revenue (₹)',
        'Total Bills', 'Average Bill (₹)'
    ])

    revenue_sql = """
        SELECT
            DATE_FORMAT(created_at, '%%Y-%%m') AS month,
            SUM(total_amount)                  AS total_revenue,
            COUNT(*)                           AS total_bills,
            ROUND(AVG(total_amount), 2)        AS avg_bill
        FROM billing_bill
        WHERE payment_status = 'paid'
        GROUP BY DATE_FORMAT(created_at, '%%Y-%%m')
        ORDER BY month DESC
    """
    df = run_query(revenue_sql)

    for _, row in df.iterrows():
        writer.writerow(row.tolist())

    return response