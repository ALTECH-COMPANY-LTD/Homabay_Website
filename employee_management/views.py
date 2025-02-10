from rest_framework import viewsets
from .models import Department, Position, Employee, Attendance, Leave, Salary, Performance, Document, Training, TrainingParticipant, Shift, EmployeeShift
from .serializers import (
    DepartmentSerializer, PositionSerializer, EmployeeSerializer,
    AttendanceSerializer, LeaveSerializer, SalarySerializer,
    PerformanceSerializer, DocumentSerializer, TrainingSerializer,
    TrainingParticipantSerializer, ShiftSerializer, EmployeeShiftSerializer
)

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

class LeaveViewSet(viewsets.ModelViewSet):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer

class SalaryViewSet(viewsets.ModelViewSet):
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer

class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class TrainingViewSet(viewsets.ModelViewSet):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer

class TrainingParticipantViewSet(viewsets.ModelViewSet):
    queryset = TrainingParticipant.objects.all()
    serializer_class = TrainingParticipantSerializer

class ShiftViewSet(viewsets.ModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer

class EmployeeShiftViewSet(viewsets.ModelViewSet):
    queryset = EmployeeShift.objects.all()
    serializer_class = EmployeeShiftSerializer