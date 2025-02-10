from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DepartmentViewSet, PositionViewSet, EmployeeViewSet,
    AttendanceViewSet, LeaveViewSet, SalaryViewSet,
    PerformanceViewSet, DocumentViewSet, TrainingViewSet,
    TrainingParticipantViewSet, ShiftViewSet, EmployeeShiftViewSet
)

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'positions', PositionViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'attendance', AttendanceViewSet)
router.register(r'leaves', LeaveViewSet)
router.register(r'salaries', SalaryViewSet)
router.register(r'performances', PerformanceViewSet)
router.register(r'documents', DocumentViewSet)
router.register(r'trainings', TrainingViewSet)
router.register(r'training-participants', TrainingParticipantViewSet)
router.register(r'shifts', ShiftViewSet)
router.register(r'employee-shifts', EmployeeShiftViewSet)

urlpatterns = [
    path('', include(router.urls)),
]