from rest_framework import serializers
from .models import ProductionLine, ProductionRun, ProductionOutput, RawMaterialRequirement

class ProductionLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionLine
        fields = '__all__'

class ProductionRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionRun
        fields = '__all__'
    
    def validate(self, attrs):
        if attrs.get('end_time') and attrs.get('start_time') and attrs['end_time'] < attrs['start_time']:
            raise serializers.ValidationError('End time must be after start time')
        if attrs.get('status') == 'completed' and not attrs.get('actual_output'):
            raise serializers.ValidationError('Completed runs must have actual output')
        return attrs

class ProductionOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionOutput
        fields = '__all__'

class RawMaterialRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterialRequirement
        fields = '__all__'