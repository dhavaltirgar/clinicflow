from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


# =============================================
# TASK 1 — Send Appointment Reminder Emails
# =============================================
@shared_task
def send_appointment_reminder():
    """
    Runs every 15 minutes.
    Finds appointments happening in next 1 hour.
    Sends reminder email to patient.
    """
    from appointments.models import Appointment

    now = timezone.now()
    one_hour_later = now + timedelta(hours=1)

    # Find appointments in next 1 hour that reminder not sent yet
    upcoming = Appointment.objects.filter(
        appointment_date=now.date(),
        appointment_time__gte=now.time(),
        appointment_time__lte=one_hour_later.time(),
        reminder_sent=False,
        status__in=['pending', 'confirmed']
    )

    count = 0
    for appointment in upcoming:
        patient_email = appointment.patient.email
        patient_name = f"{appointment.patient.first_name} {appointment.patient.last_name}"
        doctor_name = f"Dr. {appointment.doctor.user.get_full_name()}"
        appt_time = appointment.appointment_time.strftime("%I:%M %p")
        appt_date = appointment.appointment_date.strftime("%d %B %Y")

        subject = f"ClinicFlow Reminder — Your appointment is in 1 hour!"
        message = f"""
Dear {patient_name},

This is a reminder that you have an appointment scheduled:

    Doctor  : {doctor_name}
    Date    : {appt_date}
    Time    : {appt_time}

Please arrive 10 minutes early.

Regards,
ClinicFlow Team
        """

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[patient_email],
                fail_silently=False,
            )
            # Mark reminder as sent so we don't send it again
            appointment.reminder_sent = True
            appointment.save()
            count += 1
        except Exception as e:
            print(f"[EMAIL ERROR] Could not send reminder for appointment {appointment.id}: {e}")

    return f"Reminders sent: {count}"


# =============================================
# TASK 2 — Send Daily Summary to Admin
# =============================================
@shared_task
def send_daily_summary():
    """
    Runs every day at 8:00 AM.
    Sends a summary of today's appointments to admin.
    """
    from appointments.models import Appointment
    from billing.models import Bill

    today = timezone.now().date()

    # Get today's appointment counts
    total = Appointment.objects.filter(appointment_date=today).count()
    confirmed = Appointment.objects.filter(appointment_date=today, status='confirmed').count()
    pending = Appointment.objects.filter(appointment_date=today, status='pending').count()
    cancelled = Appointment.objects.filter(appointment_date=today, status='cancelled').count()

    # Get today's revenue
    from django.db.models import Sum
    revenue = Bill.objects.filter(
        created_at__date=today,
        payment_status='paid'
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    subject = f"ClinicFlow Daily Summary — {today.strftime('%d %B %Y')}"
    message = f"""
Good Morning!

Here is your ClinicFlow daily summary for {today.strftime('%d %B %Y')}:

    Total Appointments  : {total}
    Confirmed           : {confirmed}
    Pending             : {pending}
    Cancelled           : {cancelled}
    Revenue Collected   : ₹{revenue}

Have a great day!

Regards,
ClinicFlow System
    """

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,
        )
        return f"Daily summary sent for {today}"
    except Exception as e:
        return f"[EMAIL ERROR] Daily summary failed: {e}"


# =============================================
# TASK 3 — Auto Mark Past Appointments as Completed
# =============================================
@shared_task
def mark_completed_appointments():
    """
    Runs every hour.
    Finds appointments that are past their date/time
    and still marked as pending/confirmed.
    Auto-marks them as completed.
    """
    from appointments.models import Appointment

    now = timezone.now()

    # Find all past appointments still pending or confirmed
    past_appointments = Appointment.objects.filter(
        appointment_date__lt=now.date(),
        status__in=['pending', 'confirmed']
    )

    count = past_appointments.update(status='completed')

    return f"Marked {count} appointments as completed"