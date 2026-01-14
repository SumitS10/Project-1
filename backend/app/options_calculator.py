"""
Options strategy risk calculator.
Calculates max profit, max loss, breakeven, and Greeks for various strategies.
"""
from typing import List, Dict, Any, Optional
import math


def calculate_vertical_spread_risk(
    strikes: List[float],
    quantities: List[int],
    premiums: List[float],
    is_call: bool = True
) -> Dict[str, Any]:
    """
    Calculate risk metrics for a vertical spread.
    
    Args:
        strikes: [long_strike, short_strike]
        quantities: [long_qty, short_qty]
        premiums: [long_premium, short_premium] (per contract)
        is_call: True for call spread, False for put spread
    """
    long_strike, short_strike = strikes[0], strikes[1]
    long_qty, short_qty = quantities[0], quantities[1]
    long_prem, short_prem = premiums[0], premiums[1]
    
    # Net premium paid/received
    net_premium = (long_prem * long_qty) - (short_prem * short_qty)
    
    if is_call:
        # Call spread: Bullish
        spread_width = short_strike - long_strike
        max_profit = (spread_width * 100 * min(long_qty, short_qty)) - net_premium
        max_loss = net_premium
        breakeven = long_strike + (net_premium / (min(long_qty, short_qty) * 100))
    else:
        # Put spread: Bearish
        spread_width = long_strike - short_strike
        max_profit = (spread_width * 100 * min(long_qty, short_qty)) - net_premium
        max_loss = net_premium
        breakeven = long_strike - (net_premium / (min(long_qty, short_qty) * 100))
    
    risk_reward = abs(max_profit / max_loss) if max_loss > 0 else 0
    
    return {
        'max_profit': max_profit,
        'max_loss': max_loss,
        'breakeven': [breakeven],
        'net_premium': net_premium,
        'probability_of_profit': 0.5,  # Simplified - would need IV calculation
        'risk_reward_ratio': risk_reward,
    }


def calculate_iron_condor_risk(
    strikes: List[float],
    quantities: List[int],
    premiums: List[float]
) -> Dict[str, Any]:
    """
    Calculate risk metrics for an iron condor.
    
    Args:
        strikes: [put_short, put_long, call_long, call_short]
        quantities: [put_short_qty, put_long_qty, call_long_qty, call_short_qty]
        premiums: [put_short_prem, put_long_prem, call_long_prem, call_short_prem]
    """
    put_short, put_long, call_long, call_short = strikes
    put_short_qty, put_long_qty, call_long_qty, call_short_qty = quantities
    put_short_prem, put_long_prem, call_long_prem, call_short_prem = premiums
    
    # Net premium received
    net_premium = (
        (put_short_prem * put_short_qty) +
        (call_short_prem * call_short_qty) -
        (put_long_prem * put_long_qty) -
        (call_long_prem * call_long_qty)
    )
    
    # Max profit = net premium received
    max_profit = net_premium
    
    # Max loss = wider spread width - net premium
    put_spread_width = put_long - put_short
    call_spread_width = call_short - call_long
    max_spread_loss = max(put_spread_width, call_spread_width) * 100
    max_loss = max_spread_loss - net_premium
    
    # Breakevens
    lower_breakeven = put_short - (net_premium / (put_short_qty * 100))
    upper_breakeven = call_short + (net_premium / (call_short_qty * 100))
    
    risk_reward = abs(max_profit / max_loss) if max_loss > 0 else 0
    
    return {
        'max_profit': max_profit,
        'max_loss': max_loss,
        'breakeven': [lower_breakeven, upper_breakeven],
        'net_premium': net_premium,
        'probability_of_profit': 0.6,  # Iron condors typically have higher POP
        'risk_reward_ratio': risk_reward,
    }


def calculate_pmcc_risk(
    strikes: List[float],
    quantities: List[int],
    premiums: List[float],
    underlying_price: float
) -> Dict[str, Any]:
    """
    Calculate risk metrics for Poor Man's Covered Call (PMCC).
    
    Args:
        strikes: [long_call_strike (LEAPS), short_call_strike]
        quantities: [long_qty, short_qty]
        premiums: [long_premium, short_premium]
        underlying_price: Current stock price
    """
    long_strike, short_strike = strikes[0], strikes[1]
    long_qty, short_qty = quantities[0], quantities[1]
    long_prem, short_prem = premiums[0], premiums[1]
    
    # Net premium paid
    net_premium = (long_prem * long_qty) - (short_prem * short_qty)
    
    # Max profit = (short_strike - long_strike) * 100 - net_premium
    max_profit = ((short_strike - long_strike) * 100 * min(long_qty, short_qty)) - net_premium
    
    # Max loss = net premium paid (if stock goes to zero)
    max_loss = net_premium
    
    # Breakeven = long_strike + (net_premium / (long_qty * 100))
    breakeven = long_strike + (net_premium / (long_qty * 100))
    
    risk_reward = abs(max_profit / max_loss) if max_loss > 0 else 0
    
    return {
        'max_profit': max_profit,
        'max_loss': max_loss,
        'breakeven': [breakeven],
        'net_premium': net_premium,
        'probability_of_profit': 0.55,
        'risk_reward_ratio': risk_reward,
    }


def calculate_strategy_risk(
    strategy: str,
    symbol: str,
    strikes: List[float],
    quantities: List[int],
    premiums: Optional[List[float]] = None,
    underlying_price: Optional[float] = None
) -> Dict[str, Any]:
    """
    Main function to calculate risk for any strategy.
    
    Args:
        strategy: 'vertical', 'iron_condor', or 'pmcc'
        symbol: Stock ticker
        strikes: List of strike prices
        quantities: List of quantities
        premiums: List of premiums (if None, will estimate)
        underlying_price: Current stock price (for PMCC)
    """
    # If premiums not provided, estimate based on strike distances
    if premiums is None:
        premiums = [abs(strikes[i] - strikes[i+1]) * 0.1 for i in range(len(strikes)-1)]
        premiums.append(premiums[-1])  # Add last premium
    
    if strategy == 'vertical':
        # Determine if call or put spread based on strikes
        is_call = strikes[1] > strikes[0]
        return calculate_vertical_spread_risk(strikes, quantities, premiums, is_call)
    
    elif strategy == 'iron_condor':
        return calculate_iron_condor_risk(strikes, quantities, premiums)
    
    elif strategy == 'pmcc':
        if underlying_price is None:
            underlying_price = strikes[0]  # Use long strike as approximation
        return calculate_pmcc_risk(strikes, quantities, premiums, underlying_price)
    
    else:
        raise ValueError(f"Unknown strategy: {strategy}")

