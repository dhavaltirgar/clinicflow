from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Count, Sum

from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment
from prescriptions.models import Prescription
from billing.models import Bill

from .serializers import (
    PatientSerializer, DoctorSerializer,
    AppointmentSerializer, PrescriptionSerializer,
    BillSerializer
)


# -------------------------------------------------------
# 1. JWT Login — Function Based View (FBV)
# Returns JWT token on successful login
# -------------------------------------------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Exception Handling — from your PDF!
    try:
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'success' : True,
                'message' : f'Welcome {user.get_full_name() or user.username}!',
                'role'    : user.role,
                'tokens'  : {
                    'access' : str(refresh.access_token),
                    'refresh': str(refresh),
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'message': 'Invalid username or password'
            }, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# -------------------------------------------------------
# 2. Dashboard Stats — Function Based View (FBV)
# -------------------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_dashboard(request):
    # Using built-in functions + Django ORM
    stats = {
        'total_patients'     : Patient.objects.count(),
        'total_doctors'      : Doctor.objects.count(),
        'total_appointments' : Appointment.objects.count(),
        'pending_appointments': Appointment.objects.filter(
                                    status='pending'
                                ).count(),
        'completed_appointments': Appointment.objects.filter(
                                    status='completed'
                                ).count(),
        'total_revenue'      : float(
                                Bill.objects.filter(
                                    payment_status='paid'
                                ).aggregate(
                                    Sum('total_amount')
                                )['total_amount__sum'] or 0
                               ),
        'user'               : {
            'username': request.user.username,
            'role'    : request.user.role,
            'name'    : request.user.get_full_name()
        }
    }
    return Response(stats, status=status.HTTP_200_OK)


# -------------------------------------------------------
# 3. Patient API — Class Based View (CBV)
# Handles both list and create in one class
# -------------------------------------------------------
class PatientListCreateView(generics.ListCreateAPIView):
    # Generic View — ListCreateAPIView handles GET + POST
    queryset           = Patient.objects.all()
    serializer_class   = PatientSerializer
    permission_classes = [IsAuthenticated]

    # Override get_queryset to add search
    def get_queryset(self):
        queryset = Patient.objects.all()
        search   = self.request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(
                first_name__icontains=search
            ) | queryset.filter(
                last_name__icontains=search
            ) | queryset.filter(
                phone__icontains=search
            )
        return queryset


# -------------------------------------------------------
# 4. Patient Detail — Generic View
# Handles GET (one), PUT (update), DELETE
# -------------------------------------------------------
class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset           = Patient.objects.all()
    serializer_class   = PatientSerializer
    permission_classes = [IsAuthenticated]


# -------------------------------------------------------
# 5. Doctor API — Generic Views
# -------------------------------------------------------
class DoctorListView(generics.ListAPIView):
    queryset           = Doctor.objects.select_related('user').all()
    serializer_class   = DoctorSerializer
    permission_classes = [IsAuthenticated]


class DoctorDetailView(generics.RetrieveAPIView):
    queryset           = Doctor.objects.select_related('user').all()
    serializer_class   = DoctorSerializer
    permission_classes = [IsAuthenticated]


# -------------------------------------------------------
# 6. Appointment API — Class Based View (CBV)
# -------------------------------------------------------
class AppointmentListCreateView(generics.ListCreateAPIView):
    serializer_class   = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Appointment.objects.select_related(
            'patient', 'doctor__user'
        ).all()
        # Filter by status if provided
        status_filter = self.request.query_params.get('status', '')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset


class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset           = Appointment.objects.all()
    serializer_class   = AppointmentSerializer
    permission_classes = [IsAuthenticated]


# -------------------------------------------------------
# 7. Prescription API — Function Based View (FBV)
# Shows how FBV handles multiple HTTP methods
# -------------------------------------------------------
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def prescription_api(request):
    if request.method == 'GET':
        # Doctors see only their prescriptions
        if request.user.role == 'doctor':
            prescriptions = Prescription.objects.filter(
                appointment__doctor__user=request.user
            )
        else:
            prescriptions = Prescription.objects.all()

        serializer = PrescriptionSerializer(
            prescriptions, many=True
        )
        return Response({
            'count'  : prescriptions.count(),
            'results': serializer.data
        })

    elif request.method == 'POST':
        serializer = PrescriptionSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# -------------------------------------------------------
# 8. Bill API — Generic View
# -------------------------------------------------------
class BillListCreateView(generics.ListCreateAPIView):
    queryset           = Bill.objects.select_related('patient').all()
    serializer_class   = BillSerializer
    permission_classes = [IsAuthenticated]


class BillDetailView(generics.RetrieveAPIView):
    queryset           = Bill.objects.all()
    serializer_class   = BillSerializer
    permission_classes = [IsAuthenticated]