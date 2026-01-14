import pandas as pd
import numpy as np
import re
from datetime import date, datetime
from typing import Dict, List, Any, Optional
from django.conf import settings
from .models import FidelityTrade, TradierTrade, WebullTrade, TradeLog
from .api_clients import get_market_price_from_apis

def get_market_price(symbol: str, source: str = None) -> float:
    """
    Get current market price for a symbol using APIs or fallback.
    
    Args:
        symbol: Stock ticker symbol
        source: 'tradier', 'webull', or None (tries both)
    
    Returns:
        Current price as float, or fallback random price if APIs unavailable
    """
    # Try to get from APIs
    if source:
        price = get_market_price_from_apis(symbol, preferred_source=source)
    else:
        price = get_market_price_from_apis(symbol)
    
    if price:
        return price
    
    # Fallback to random price if APIs not configured or fail
    import random
    return 100.0 + float(random.random() * 20.0)

def parse_date(val) -> Optional[date]:
    """Parse date from various formats, handling unrecognized timezones like 'EST'."""
    if val is None or val == "" or pd.isna(val):
        return None
    if isinstance(val, date):
        return val
    if isinstance(val, datetime):
        return val.date()
    try:
        # Remove timezone abbreviations like 'EST', 'EDT', etc.
        if isinstance(val, str):
            val = re.sub(r'\s[A-Z]{2,4}$', '', val)
        return pd.to_datetime(val).date()
    except Exception:
        return None

def get_trade_id(row: Dict, col_map: Dict[str, int]) -> str:
    """Get Trade ID from row, with fallback."""
    # Column 1: Trade ID
    tid = row.get('trade_id') or row.get('tradeid') or row.get('trade_id')
    if tid and str(tid).strip():
        return str(tid).strip()
    
    # Fallback: TradeDate|Symbol|Strategy
    trade_date = row.get('trade_date') or row.get('tradedate') or row.get('trade_date')
    symbol = row.get('symbol') or row.get('symbol')
    strategy = row.get('strategy') or row.get('strategy') or ""
    
    return f"{trade_date}|{symbol}|{strategy}"

def process_sheet_rows(rows: List[Dict], source: str) -> Dict[str, Dict]:
    """
    Process rows from a sheet and aggregate by Trade ID.
    Equivalent to ProcessSheet VBA function.
    """
    dict_trades = {}
    
    for row in rows:
        # Get Trade ID
        tid = get_trade_id(row, {})
        
        # Initialize trade if not exists
        if tid not in dict_trades:
            dict_trades[tid] = {
                "Source": source,
                "TradeDate": parse_date(row.get('trade_date') or row.get('tradedate')),
                "Symbol": str(row.get('symbol') or row.get('symbol') or "").strip(),
                "Strategy": str(row.get('strategy') or row.get('strategy') or "").strip(),
                "Expiration": parse_date(row.get('expiry') or row.get('expiration') or row.get('expiry')),
                "Strikes": "",
                "Status": "Open",
                "CloseDate": None,
                "Legs": 0,
                "ClosedLegs": 0,
                "OpenNet": 0.0,
                "CloseNet": 0.0,
                "Qty": float(row.get('quantity') or row.get('qty') or 0),
            }
        
        d = dict_trades[tid]
        d["Legs"] += 1
        
        # Get values
        prem = float(row.get('premium') or row.get('premium') or 0)
        qty = float(row.get('quantity') or row.get('qty') or 0)
        act = str(row.get('action') or row.get('action') or "").upper().strip()
        
        # Process actions
        if act == "BTO":
            d["OpenNet"] = d["OpenNet"] - prem * qty
        elif act == "STO":
            d["OpenNet"] = d["OpenNet"] + prem * qty
        elif act == "STC":
            d["CloseNet"] = d["CloseNet"] + prem * qty
            d["ClosedLegs"] += 1
            if not d["CloseDate"]:
                d["CloseDate"] = parse_date(row.get('trade_date') or row.get('tradedate'))
        elif act == "BTC":
            d["CloseNet"] = d["CloseNet"] - prem * qty
            d["ClosedLegs"] += 1
            if not d["CloseDate"]:
                d["CloseDate"] = parse_date(row.get('trade_date') or row.get('tradedate'))
        
        # Strikes
        strike = str(row.get('strike') or row.get('strike') or "")
        if d["Strikes"]:
            d["Strikes"] += "/"
        d["Strikes"] += strike
        
        # Check if closed
        if d["ClosedLegs"] >= d["Legs"]:
            d["Status"] = "Closed"
            d["PL"] = (d["CloseNet"] - d["OpenNet"]) * 100
            if d["OpenNet"] != 0:
                d["PLPercent"] = d["PL"] / abs(d["OpenNet"] * 100)
            else:
                d["PLPercent"] = 0
            
            if d["PL"] > 0:
                d["WinLoss"] = "Win"
            elif d["PL"] < 0:
                d["WinLoss"] = "Loss"
            else:
                d["WinLoss"] = "BreakEven"
        else:
            d["PL"] = 0
            d["PLPercent"] = 0
            d["WinLoss"] = ""
        
        d["NetPremium"] = d["OpenNet"]
        d["TotalCost"] = abs(d["OpenNet"]) * 100
        
        # DTE calculation
        today = date.today()
        if d["Status"] == "Open":
            if d["Expiration"]:
                d["DTE"] = (d["Expiration"] - today).days
            else:
                d["DTE"] = None
        else:
            if d["CloseDate"] and d["TradeDate"]:
                d["DTE"] = (d["CloseDate"] - d["TradeDate"]).days
            else:
                d["DTE"] = None
    
    return dict_trades

def update_trade_log():
    """
    Equivalent to UpdateTradeLog VBA function.
    Processes all import sheets and creates/updates TradeLog entries.
    """
    # Clear existing trade log
    TradeLog.objects.all().delete()
    
    # Process each source
    all_trades = {}
    
    # Process Fidelity
    fidelity_rows = []
    for trade in FidelityTrade.objects.all():
        fidelity_rows.append({
            'trade_id': trade.trade_id,
            'trade_date': trade.trade_date,
            'symbol': trade.symbol,
            'strategy': trade.strategy,
            'strike': trade.strike,
            'action': trade.action,
            'quantity': trade.quantity,
            'premium': trade.premium,
            'expiry': trade.expiry,
        })
    
    if fidelity_rows:
        fidelity_trades = process_sheet_rows(fidelity_rows, "Fidelity")
        all_trades.update(fidelity_trades)
    
    # Process Tradier
    tradier_rows = []
    for trade in TradierTrade.objects.all():
        tradier_rows.append({
            'trade_id': trade.trade_id,
            'trade_date': trade.trade_date,
            'symbol': trade.symbol,
            'strategy': trade.strategy,
            'strike': trade.strike,
            'action': trade.action,
            'quantity': trade.quantity,
            'premium': trade.premium,
            'expiry': trade.expiry,
        })
    
    if tradier_rows:
        tradier_trades = process_sheet_rows(tradier_rows, "Tradier")
        all_trades.update(tradier_trades)
    
    # Process Webull
    webull_rows = []
    for trade in WebullTrade.objects.all():
        webull_rows.append({
            'trade_id': trade.trade_id,
            'trade_date': trade.trade_date,
            'symbol': trade.symbol,
            'strategy': trade.strategy,
            'strike': trade.strike,
            'action': trade.action,
            'quantity': trade.quantity,
            'premium': trade.premium,
            'expiry': trade.expiry,
        })
    
    if webull_rows:
        webull_trades = process_sheet_rows(webull_rows, "Webull")
        all_trades.update(webull_trades)
    
    # Create TradeLog entries
    for tid, d in all_trades.items():
        TradeLog.objects.create(
            trade_id=tid,
            source=d["Source"],
            trade_date=d["TradeDate"] or date.today(),
            close_date=d["CloseDate"],
            symbol=d["Symbol"],
            strategy=d["Strategy"],
            expiration=d["Expiration"],
            strikes=d["Strikes"],
            net_premium=d["NetPremium"],
            total_cost=d["TotalCost"],
            pl=d.get("PL", 0),
            pl_percent=d.get("PLPercent", 0),
            status=d["Status"],
            win_loss=d.get("WinLoss", ""),
            dte=d.get("DTE"),
            legs=d["Legs"],
            closed_legs=d["ClosedLegs"],
            open_net=d["OpenNet"],
            close_net=d["CloseNet"],
        )

def parse_option_symbol(option_name: str) -> Dict[str, Any]:
    """
    Parse Webull option symbol format: SYMBOLYYMMDDC/PSTRIKE
    Example: CRM260206C00270000 = CRM, 2026-02-06, CALL, 270.00
    """
    if not option_name or len(option_name) < 15:
        return {}
    
    try:
        # Find where date starts (after symbol, usually 3-5 chars)
        # Look for pattern: letters followed by 6 digits
        match = re.match(r'^([A-Z]+)(\d{6})([CP])(\d{8})$', option_name)
        if match:
            symbol = match.group(1)
            date_str = match.group(2)  # YYMMDD
            option_type = 'CALL' if match.group(3) == 'C' else 'PUT'
            strike_str = match.group(4)  # 00270000 = 270.00
            
            # Parse date: YYMMDD -> YYYY-MM-DD
            year = 2000 + int(date_str[:2])
            month = int(date_str[2:4])
            day = int(date_str[4:6])
            expiry_date = date(year, month, day)
            
            # Parse strike: 00270000 -> 270.00
            strike = float(strike_str) / 1000.0
            
            return {
                'symbol': symbol,
                'expiry': expiry_date,
                'option_type': option_type,
                'strike': strike
            }
    except:
        pass
    
    return {}


def import_fidelity(file_path: str) -> None:
    """Import Fidelity CSV and save to database."""
    # Clear existing Fidelity trades (like VBA does)
    FidelityTrade.objects.all().delete()
    
    df = pd.read_csv(file_path)
    df.columns = [c.strip().lower() for c in df.columns]
    
    # Map columns (adjust based on your actual CSV structure)
    # Assuming columns: trade_id, trade_date, symbol, strategy, strike, action, quantity, premium, expiry
    for _, row in df.iterrows():
        FidelityTrade.objects.create(
            trade_id=str(row.get('trade_id', '') or row.get('tradeid', '') or ''),
            trade_date=parse_date(row.get('trade_date') or row.get('tradedate')) or date.today(),
            symbol=str(row.get('symbol', '') or row.get('symbol', '')).strip(),
            strategy=str(row.get('strategy', '') or row.get('strategy', '')).strip(),
            strike=float(row.get('strike', 0) or row.get('strike', 0)) if pd.notna(row.get('strike', 0)) else None,
            action=str(row.get('action', '') or row.get('action', '')).strip().upper(),
            quantity=float(row.get('quantity', 0) or row.get('qty', 0)),
            premium=float(row.get('premium', 0) or row.get('premium', 0)),
            expiry=parse_date(row.get('expiry') or row.get('expiration') or row.get('expiry')),
        )
    
    # Update trade log after import
    update_trade_log()

def import_tradier(file_path: str) -> None:
    """Import Tradier CSV and save to database."""
    # Clear existing Tradier trades (like VBA does)
    TradierTrade.objects.all().delete()
    
    df = pd.read_csv(file_path)
    df.columns = [c.strip().lower() for c in df.columns]
    
    for _, row in df.iterrows():
        TradierTrade.objects.create(
            trade_id=str(row.get('trade_id', '') or row.get('tradeid', '') or ''),
            trade_date=parse_date(row.get('trade_date') or row.get('tradedate')) or date.today(),
            symbol=str(row.get('symbol', '') or row.get('symbol', '')).strip(),
            strategy=str(row.get('strategy', '') or row.get('strategy', '')).strip(),
            strike=float(row.get('strike', 0) or row.get('strike', 0)) if pd.notna(row.get('strike', 0)) else None,
            action=str(row.get('action', '') or row.get('action', '')).strip().upper(),
            quantity=float(row.get('quantity', 0) or row.get('qty', 0)),
            premium=float(row.get('premium', 0) or row.get('premium', 0)),
            expiry=parse_date(row.get('expiry') or row.get('expiration') or row.get('expiry')),
        )
    
    # Update trade log after import
    update_trade_log()

def import_webull(file_path: str) -> None:
    """
    Import Webull CSV and save to database.
    Expected columns: Name, Symbol, Side, Status, Filled, Total Qty, Price, Avg Price, Time-in-Force, Placed Time, Filled Time
    """
    # Clear existing Webull trades (like VBA does)
    WebullTrade.objects.all().delete()
    
    df = pd.read_csv(file_path)
    df.columns = [c.strip().lower() for c in df.columns]
    
    for _, row in df.iterrows():
        # Parse option details from "Name" column (e.g., "CRM260206C00270000" or "QQQ Vertical")
        name = str(row.get('name', '') or row.get('name', '')).strip()
        option_details = parse_option_symbol(name)
        
        # Get symbol from Symbol column or parsed from Name
        symbol = str(row.get('symbol', '') or row.get('symbol', '')).strip()
        if not symbol and option_details:
            symbol = option_details.get('symbol', '')
        
        # Get side (BUY/SELL) and convert to action format
        side = str(row.get('side', '') or row.get('side', '')).strip().upper()
        if side == 'BUY':
            action = 'BTO'  # Buy to Open
        elif side == 'SELL':
            action = 'STO'  # Sell to Open
        else:
            action = side
        
        # Get quantity
        quantity = float(row.get('total qty', 0) or row.get('total_qty', 0) or row.get('qty', 0) or 0)
        
        # Get premium (use Avg Price or Price)
        premium = float(row.get('avg price', 0) or row.get('avg_price', 0) or row.get('price', 0) or 0)
        
        # Get placed time for trade_date
        placed_time = row.get('placed time', '') or row.get('placed_time', '') or row.get('trade_date', '')
        trade_date_val = parse_date(placed_time) or date.today()
        
        # Use parsed option details or fallback to row data
        strike = option_details.get('strike') if option_details else (
            float(row.get('strike', 0)) if pd.notna(row.get('strike', 0)) else None
        )
        expiry = option_details.get('expiry') if option_details else (
            parse_date(row.get('expiry') or row.get('expiration') or row.get('expiry'))
        )
        
        # Strategy from Name if it's a strategy name (e.g., "QQQ Vertical")
        strategy = ''
        if 'vertical' in name.lower():
            strategy = 'Vertical'
        elif 'iron condor' in name.lower():
            strategy = 'Iron Condor'
        elif 'pmcc' in name.lower() or 'poor man' in name.lower():
            strategy = 'PMCC'
        elif option_details:
            strategy = option_details.get('option_type', '')
        
        # Create trade record
        WebullTrade.objects.create(
            trade_id=name,  # Use Name as trade_id
            trade_date=trade_date_val,
            symbol=symbol,
            strategy=strategy,
            strike=strike,
            action=action,
            quantity=quantity,
            premium=premium,
            expiry=expiry,
        )
    
    # Update trade log after import
    update_trade_log()
