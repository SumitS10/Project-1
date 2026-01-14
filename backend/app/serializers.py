from rest_framework import serializers
from .models import FidelityTrade, TradierTrade, WebullTrade, TradeLog

class FidelityTradeSerializer(serializers.ModelSerializer):
    # Computed fields for backward compatibility with frontend
    option_type = serializers.SerializerMethodField()
    pnl = serializers.SerializerMethodField()
    expiry = serializers.DateField(read_only=True)  # Removed source='expiry'
    
    class Meta:
        model = FidelityTrade
        fields = '__all__'
    
    def get_option_type(self, obj):
        if obj.action:
            if obj.action in ['BTO', 'STC']:
                return 'CALL'
            elif obj.action in ['STO', 'BTC']:
                return 'PUT'
        return 'CALL'
    
    def get_pnl(self, obj):
        return None

class TradierTradeSerializer(serializers.ModelSerializer):
    option_type = serializers.SerializerMethodField()
    pnl = serializers.SerializerMethodField()
    expiry = serializers.DateField(read_only=True)  # Removed source='expiry'
    
    class Meta:
        model = TradierTrade
        fields = '__all__'
    
    def get_option_type(self, obj):
        if obj.action:
            if obj.action in ['BTO', 'STC']:
                return 'CALL'
            elif obj.action in ['STO', 'BTC']:
                return 'PUT'
        return 'CALL'
    
    def get_pnl(self, obj):
        return None

class WebullTradeSerializer(serializers.ModelSerializer):
    option_type = serializers.SerializerMethodField()
    pnl = serializers.SerializerMethodField()
    expiry = serializers.DateField(read_only=True)  # Removed source='expiry'
    
    class Meta:
        model = WebullTrade
        fields = '__all__'
    
    def get_option_type(self, obj):
        if obj.action:
            if obj.action in ['BTO', 'STC']:
                return 'CALL'
            elif obj.action in ['STO', 'BTC']:
                return 'PUT'
        return 'CALL'
    
    def get_pnl(self, obj):
        return None

class TradeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeLog
        fields = '__all__'
