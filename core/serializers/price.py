from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from core.models.price import Price


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'
