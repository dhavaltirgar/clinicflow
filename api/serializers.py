from rest_framework import serializers
from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment
from prescriptions.models import Prescription
from billing.models import Bill
from accounts.models import User


# -------------------------------------------------------
# What is a Serializer?
# It converts Django model objects to JSON (and back)
# Model → Serializer → JSON (for API response)
# JSON → Serializer → Model (for saving data)
# -------------------------------------------------------

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ['id', 'username', 'email', 'role', 'phone']


class PatientSerializer(serializers.ModelSerializer):
    # SerializerMethodField — add custom computed field
    age = serializers.SerializerMethodField()

    class Meta:
        model  = Patient
        fields = [
            'id', 'first_name', 'last_name',
            'email', 'phone', 'gender',
            'blood_group', 'date_of_birth',
            'age', 'address', 'medical_history',
            'created_at'
        ]

    # Custom method field — from your PDF built-in functions!
    def get_age(self, obj):
        return obj.age


class DoctorSerializer(serializers.ModelSerializer):
    # Nested serializer — show user details inside doctor
    user = UserSerializer(read_only=True)

    class Meta:
        model  = Doctor
        fields = [
            'id', 'user', 'specialization',
            'qualification', 'experience_years',
            'consultation_fee', 'is_available', 'bio'
        ]


class AppointmentSerializer(serializers.ModelSerializer):
    # Nested serializers — show full patient and doctor details
    patient_name = serializers.SerializerMethodField()
    doctor_name  = serializers.SerializerMethodField()

    class Meta:
        model  = Appointment
        fields = [
            'id', 'patient', 'patient_name',
            'doctor', 'doctor_name',
            'appointment_date', 'appointment_time',
            'status', 'reason', 'notes',
            'reminder_sent', 'created_at'
        ]

    def get_patient_name(self, obj):
        return str(obj.patient)

    def get_doctor_name(self, obj):
        return str(obj.doctor)


class PrescriptionSerializer(serializers.ModelSerializer):
    # Lambda-like — get medicine list as array
    medicine_list = serializers.SerializerMethodField()
    patient_name  = serializers.SerializerMethodField()

    class Meta:
        model  = Prescription
        fields = [
            'id', 'appointment', 'patient_name',
            'diagnosis', 'medicines', 'medicine_list',
            'instructions', 'follow_up_date', 'created_at'
        ]

    def get_medicine_list(self, obj):
        # Using list + map — from your PDF!
        return list(map(
            lambda m: m.strip(),
            obj.medicines.split(',')
        ))

    def get_patient_name(self, obj):
        return str(obj.appointment.patient)


class BillSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()

    class Meta:
        model  = Bill
        fields = [
            'id', 'invoice_number', 'appointment',
            'patient', 'patient_name',
            'consultation_fee', 'medicine_charges',
            'other_charges', 'total_amount',
            'payment_status', 'payment_method',
            'created_at'
        ]

    def get_patient_name(self, obj):
        return str(obj.patient)