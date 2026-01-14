from django.db import models
from django.utils import timezone

# Raw import models (store individual CSV rows)
class FidelityTrade(models.Model):
    trade_id = models.CharField(max_length=100, blank=True, null=True)  # Column 1
    trade_date = models.DateField()  # Column 2
    symbol = models.CharField(max_length=20)  # Column 3
    strategy = models.CharField(max_length=50, blank=True)  # Column 4
    strike = models.FloatField(blank=True, null=True)  # Column 8
    action = models.CharField(max_length=10, blank=True)  # Column 9: BTO/STO/STC/BTC
    quantity = models.FloatField()  # Column 10
    premium = models.FloatField()  # Column 11
    expiry = models.DateField(blank=True, null=True)  # Column 7
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-trade_date', 'symbol']

class TradierTrade(models.Model):
    trade_id = models.CharField(max_length=100, blank=True, null=True)  # Column 1
    trade_date = models.DateField()  # Column 2
    symbol = models.CharField(max_length=20)  # Column 3
    strategy = models.CharField(max_length=50, blank=True)  # Column 4
    strike = models.FloatField(blank=True, null=True)  # Column 8
    action = models.CharField(max_length=10, blank=True)  # Column 9: BTO/STO/STC/BTC
    quantity = models.FloatField()  # Column 10
    premium = models.FloatField()  # Column 11
    expiry = models.DateField(blank=True, null=True)  # Column 7
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-trade_date', 'symbol']

class WebullTrade(models.Model):
    trade_id = models.CharField(max_length=100, blank=True, null=True)  # Column 1
    trade_date = models.DateField()  # Column 2
    symbol = models.CharField(max_length=20)  # Column 3
    strategy = models.CharField(max_length=50, blank=True)  # Column 4
    strike = models.FloatField(blank=True, null=True)  # Column 8
    action = models.CharField(max_length=10, blank=True)  # Column 9: BTO/STO/STC/BTC
    quantity = models.FloatField()  # Column 10
    premium = models.FloatField()  # Column 11
    expiry = models.DateField(blank=True, null=True)  # Column 7
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-trade_date', 'symbol']

# Aggregated Trade Log (equivalent to your Trade_Log sheet)
class TradeLog(models.Model):
    trade_id = models.CharField(max_length=200, unique=True)  # Key for grouping
    source = models.CharField(max_length=20)  # Fidelity/Tradier/Webull
    trade_date = models.DateField()
    close_date = models.DateField(null=True, blank=True)
    symbol = models.CharField(max_length=20)
    strategy = models.CharField(max_length=50, blank=True)
    expiration = models.DateField(null=True, blank=True)
    strikes = models.CharField(max_length=200, blank=True)  # Comma-separated strikes
    net_premium = models.FloatField(default=0)  # OpenNet
    total_cost = models.FloatField(default=0)  # Abs(OpenNet) * 100
    pl = models.FloatField(default=0)  # P&L in dollars
    pl_percent = models.FloatField(default=0)  # P&L percentage
    status = models.CharField(max_length=10, default='Open')  # Open/Closed
    win_loss = models.CharField(max_length=20, blank=True)  # Win/Loss/BreakEven
    dte = models.IntegerField(null=True, blank=True)  # Days to expiration
    legs = models.IntegerField(default=0)
    closed_legs = models.IntegerField(default=0)
    open_net = models.FloatField(default=0)
    close_net = models.FloatField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-trade_date', 'symbol']
