import pandas as pd
import numpy as np
from .models import FidelityTrade, TradierTrade

def get_market_price(symbol: str) -> float:
    """Get current market price for a symbol. Replace with real API."""
    # TODO: Replace with real market data API (Alpha Vantage, Yahoo Finance, etc.)
    return 100.0 + float(np.random.rand() * 20.0)

def import_fidelity(file_path: str) -> None:
    """Import Fidelity CSV and save to database."""
    df = pd.read_csv(file_path)
    df.columns = [c.strip().lower() for c in df.columns]

    for _, row in df.iterrows():
        trade = FidelityTrade.objects.create(
            symbol=row['symbol'],
            trade_date=pd.to_datetime(row['trade_date']).date(),
            option_type=row['option_type'].upper(),
            strike=float(row['strike']),
            expiry=pd.to_datetime(row['expiry']).date(),
            quantity=int(row['quantity']),
            premium=float(row['premium']),
        )
        set_trade_pnl(trade)

def import_tradier(file_path: str) -> None:
    """Import Tradier CSV and save to database."""
    df = pd.read_csv(file_path)
    df.columns = [c.strip().lower() for c in df.columns]

    for _, row in df.iterrows():
        trade = TradierTrade.objects.create(
            symbol=row['symbol'],
            trade_date=pd.to_datetime(row['trade_date']).date(),
            option_type=row['option_type'].upper(),
            strike=float(row['strike']),
            expiry=pd.to_datetime(row['expiry']).date(),
            quantity=int(row['quantity']),
            premium=float(row['premium']),
        )
        set_trade_pnl(trade)

def set_trade_pnl(trade) -> None:
    """Calculate and set P&L for a trade."""
    current_price = get_market_price(trade.symbol)
    trade.pnl = (current_price - trade.premium) * trade.quantity
    trade.save()

