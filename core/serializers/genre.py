from drf_writable_nested import UniqueFieldsMixin
from rest_framework import serializers
from core.models.genre import Genre


class GenreSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

    def create(self, validated_data):
        return Genre.objects.get_or_create(**validated_data)[0]
