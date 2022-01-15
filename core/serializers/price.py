from rest_framework import serializers
from core.models.price import Price


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = [
            'discount',
            'original',
            'discount_fmt',
            'original_fmt',
            'created_at'
        ]
