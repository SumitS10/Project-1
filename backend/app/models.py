from django.db import models

class FidelityTrade(models.Model):
    symbol = models.CharField(max_length=20)
    trade_date = models.DateField()
    option_type = models.CharField(max_length=4)  # CALL/PUT
    strike = models.FloatField()
    expiry = models.DateField()
    quantity = models.IntegerField()
    premium = models.FloatField()
    pnl = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-trade_date', 'symbol']

class TradierTrade(models.Model):
    symbol = models.CharField(max_length=20)
    trade_date = models.DateField()
    option_type = models.CharField(max_length=4)
    strike = models.FloatField()
    expiry = models.DateField()
    quantity = models.IntegerField()
    premium = models.FloatField()
    pnl = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-trade_date', 'symbol']
