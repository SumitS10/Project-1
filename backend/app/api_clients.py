"""
API clients for Webull and Tradier to fetch real market data.
"""
import requests
from django.conf import settings
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


def get_tradier_quote(symbol: str) -> Optional[float]:
    """
    Get current market price from Tradier API.
    
    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL')
    
    Returns:
        Current price as float, or None if error
    """
    if not settings.TRADIER_API_KEY:
        logger.warning("Tradier API key not configured")
        return None
    
    try:
        url = f"{settings.TRADIER_BASE_URL}/markets/quotes"
        headers = {
            'Authorization': f'Bearer {settings.TRADIER_API_KEY}',
            'Accept': 'application/json'
        }
        params = {
            'symbols': symbol,
            'greeks': 'false'
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if 'quotes' in data and 'quote' in data['quotes']:
            quotes = data['quotes']['quote']
            # Handle both single quote and list of quotes
            if isinstance(quotes, list):
                if len(quotes) > 0:
                    return float(quotes[0].get('last', 0))
            else:
                return float(quotes.get('last', 0))
        
        logger.warning(f"No quote data found for {symbol} from Tradier")
        return None
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Tradier API error for {symbol}: {str(e)}")
        return None
    except (KeyError, ValueError, TypeError) as e:
        logger.error(f"Error parsing Tradier response for {symbol}: {str(e)}")
        return None


def get_webull_quote(symbol: str) -> Optional[float]:
    """
    Get current market price from Webull API.
    
    Note: Webull API requires authentication and may have different endpoints.
    This is a basic implementation - adjust based on Webull's actual API docs.
    
    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL')
    
    Returns:
        Current price as float, or None if error
    """
    if not settings.WEBULL_API_KEY:
        logger.warning("Webull API key not configured")
        return None
    
    try:
        # Webull API endpoint (adjust based on actual Webull API documentation)
        url = f"{settings.WEBULL_BASE_URL}/quote"
        headers = {
            'Authorization': f'Bearer {settings.WEBULL_API_KEY}',
            'Content-Type': 'application/json'
        }
        params = {
            'symbol': symbol
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        # Adjust based on Webull's actual response structure
        if 'data' in data and 'price' in data['data']:
            return float(data['data']['price'])
        elif 'close' in data:
            return float(data['close'])
        elif 'last' in data:
            return float(data['last'])
        
        logger.warning(f"No price data found for {symbol} from Webull")
        return None
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Webull API error for {symbol}: {str(e)}")
        return None
    except (KeyError, ValueError, TypeError) as e:
        logger.error(f"Error parsing Webull response for {symbol}: {str(e)}")
        return None


def get_market_price_from_apis(symbol: str, preferred_source: str = 'tradier') -> Optional[float]:
    """
    Get market price from APIs, with fallback logic.
    
    Args:
        symbol: Stock ticker symbol
        preferred_source: 'tradier' or 'webull'
    
    Returns:
        Current price as float, or None if all APIs fail
    """
    # Try preferred source first
    if preferred_source == 'tradier':
        price = get_tradier_quote(symbol)
        if price:
            return price
        # Fallback to Webull
        price = get_webull_quote(symbol)
        if price:
            return price
    else:
        price = get_webull_quote(symbol)
        if price:
            return price
        # Fallback to Tradier
        price = get_tradier_quote(symbol)
        if price:
            return price
    
    return None


def get_tradier_options_chain(symbol: str, expiry: str = None) -> Optional[Dict[str, Any]]:
    """
    Get options chain from Tradier API.
    
    Args:
        symbol: Stock ticker symbol
        expiry: Expiration date (YYYY-MM-DD format), optional
    
    Returns:
        Options chain data as dict, or None if error
    """
    if not settings.TRADIER_API_KEY:
        return None
    
    try:
        url = f"{settings.TRADIER_BASE_URL}/markets/options/chains"
        headers = {
            'Authorization': f'Bearer {settings.TRADIER_API_KEY}',
            'Accept': 'application/json'
        }
        params = {
            'symbol': symbol,
            'greeks': 'true'
        }
        if expiry:
            params['expiration'] = expiry
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Tradier options chain error for {symbol}: {str(e)}")
        return None


def place_webull_trade(
    symbol: str,
    option_id: str,
    quantity: int,
    action: str = 'BUY',
    order_type: str = 'LMT',
    price: float = None
) -> Optional[Dict[str, Any]]:
    """
    Place an options trade via Webull API.
    
    Args:
        symbol: Stock ticker symbol
        option_id: Webull option contract ID
        quantity: Number of contracts
        action: 'BUY' or 'SELL'
        order_type: 'LMT' (limit), 'MKT' (market), etc.
        price: Limit price (required for limit orders)
    
    Returns:
        Order response dict, or None if error
    """
    if not settings.WEBULL_API_KEY:
        logger.warning("Webull API key not configured")
        return None
    
    try:
        # Webull API endpoint for placing orders
        # Note: Adjust based on actual Webull API documentation
        url = f"{settings.WEBULL_BASE_URL}/order/place"
        headers = {
            'Authorization': f'Bearer {settings.WEBULL_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'symbol': symbol,
            'option_id': option_id,
            'quantity': quantity,
            'action': action.upper(),
            'order_type': order_type.upper(),
        }
        
        if price and order_type.upper() == 'LMT':
            payload['price'] = price
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Webull trade placement error: {str(e)}")
        return None


def get_webull_option_chain(symbol: str, expiry: str = None) -> Optional[Dict[str, Any]]:
    """
    Get options chain from Webull API.
    
    Args:
        symbol: Stock ticker symbol
        expiry: Expiration date (YYYY-MM-DD format), optional
    
    Returns:
        Options chain data as dict, or None if error
    """
    if not settings.WEBULL_API_KEY:
        return None
    
    try:
        url = f"{settings.WEBULL_BASE_URL}/quote/option"
        headers = {
            'Authorization': f'Bearer {settings.WEBULL_API_KEY}',
            'Accept': 'application/json'
        }
        params = {
            'symbol': symbol
        }
        if expiry:
            params['expiry'] = expiry
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Webull options chain error for {symbol}: {str(e)}")
        return None

