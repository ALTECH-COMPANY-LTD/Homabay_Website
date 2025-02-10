from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductionLineViewSet,
    ProductionRunViewSet,
    ProductionOutputViewSet,
    RawMaterialRequirementViewSet
)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'production-lines', ProductionLineViewSet)
router.register(r'production-runs', ProductionRunViewSet)
router.register(r'production-outputs', ProductionOutputViewSet)
router.register(r'raw-material-requirements', RawMaterialRequirementViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]