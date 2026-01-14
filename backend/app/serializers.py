from rest_framework import serializers
from .models import FidelityTrade, TradierTrade, WebullTrade, TradeLog

class FidelityTradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FidelityTrade
        fields = '__all__'

class TradierTradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradierTrade
        fields = '__all__'

class WebullTradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebullTrade
        fields = '__all__'

class TradeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeLog
        fields = '__all__'

