from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import ProductionLine, ProductionRun, ProductionOutput, RawMaterialRequirement
from .serializers import (
    ProductionLineSerializer, ProductionRunSerializer,
    ProductionOutputSerializer, RawMaterialRequirementSerializer
)

class ProductionLineViewSet(viewsets.ModelViewSet):
    queryset = ProductionLine.objects.all()
    serializer_class = ProductionLineSerializer
    permission_classes = [AllowAny]

class ProductionRunViewSet(viewsets.ModelViewSet):
    queryset = ProductionRun.objects.all()
    serializer_class = ProductionRunSerializer
    permission_classes = [AllowAny]

class ProductionOutputViewSet(viewsets.ModelViewSet):
    queryset = ProductionOutput.objects.all()
    serializer_class = ProductionOutputSerializer
    permission_classes = [AllowAny]

class RawMaterialRequirementViewSet(viewsets.ModelViewSet):
    queryset = RawMaterialRequirement.objects.all()
    serializer_class = RawMaterialRequirementSerializer
    permission_classes = [AllowAny]