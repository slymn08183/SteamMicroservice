from drf_writable_nested import UniqueFieldsMixin
from rest_framework import serializers
from core.models.developer import Developer


class DeveloperSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = ['name']

    def create(self, validated_data):
        return Developer.objects.get_or_create(**validated_data)[0]
