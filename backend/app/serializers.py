from rest_framework import serializers
from .models import FidelityTrade, TradierTrade

class FidelityTradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FidelityTrade
        fields = '__all__'

class TradierTradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradierTrade
        fields = '__all__'

