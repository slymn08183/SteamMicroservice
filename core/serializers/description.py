from rest_framework import serializers
from core.models.description import Description


class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = '__all__'

