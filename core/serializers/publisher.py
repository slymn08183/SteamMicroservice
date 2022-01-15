from drf_writable_nested import UniqueFieldsMixin
from rest_framework import serializers
from core.models.publisher import Publisher


class PublisherSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['name']

    def create(self, validated_data):
        return Publisher.objects.get_or_create(**validated_data)[0]
