from rest_framework import serializers
from core.models.specification import Specification


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = '__all__'

