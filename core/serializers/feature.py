from drf_writable_nested import UniqueFieldsMixin
from rest_framework import serializers
from core.models.feature import Feature


class FeatureSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'

    def create(self, validated_data):
        return Feature.objects.get_or_create(**validated_data)[0]
