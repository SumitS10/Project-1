# API Setup Guide

This project supports integration with **Tradier** and **Webull** APIs to fetch real-time market data.

## Configuration

### Environment Variables

Set these environment variables in your deployment platform (Render, Heroku, etc.):

#### Tradier API
- `TRADIER_API_KEY` - Your Tradier API key
- `TRADIER_API_SECRET` - Your Tradier API secret (if required)
- `TRADIER_ACCOUNT_ID` - Your Tradier account ID
- `TRADIER_BASE_URL` - API base URL (default: `https://api.tradier.com/v1`)

#### Webull API
- `WEBULL_API_KEY` - Your Webull API key
- `WEBULL_API_SECRET` - Your Webull API secret (if required)
- `WEBULL_BASE_URL` - API base URL (default: `https://api.webull.com/api`)

## Getting API Keys

### Tradier API

1. Sign up at [Tradier](https://developer.tradier.com/)
2. Create an application to get your API key
3. Copy your API key and account ID
4. Set environment variables in your deployment platform

**Tradier API Documentation:**
- Base URL: `https://api.tradier.com/v1`
- Endpoints:
  - Quotes: `GET /markets/quotes?symbols={symbol}`
  - Options Chain: `GET /markets/options/chains?symbol={symbol}`

### Webull API

1. Sign up for Webull API access (check Webull developer documentation)
2. Get your API credentials
3. Set environment variables in your deployment platform

**Note:** Webull API endpoints may vary. Adjust `api_clients.py` based on Webull's actual API documentation.

## Local Development

Create a `.env` file in the `backend/` directory:

```bash
TRADIER_API_KEY=your_key_here
TRADIER_API_SECRET=your_secret_here
TRADIER_ACCOUNT_ID=your_account_id
TRADIER_BASE_URL=https://api.tradier.com/v1

WEBULL_API_KEY=your_key_here
WEBULL_API_SECRET=your_secret_here
WEBULL_BASE_URL=https://api.webull.com/api
```

Then load them in `settings.py` (you may need `python-decouple` or `django-environ` package).

## How It Works

1. **Market Price Fetching:**
   - When calculating P&L, the system calls `get_market_price_from_apis(symbol)`
   - Tries Tradier first, falls back to Webull if Tradier fails
   - Falls back to dummy data if both APIs fail or are not configured

2. **API Clients:**
   - `backend/app/api_clients.py` contains the API integration code
   - `get_tradier_quote(symbol)` - Fetches current price from Tradier
   - `get_webull_quote(symbol)` - Fetches current price from Webull
   - `get_tradier_options_chain(symbol, expiry)` - Gets options chain data

3. **Usage in Code:**
   ```python
   from app.api_clients import get_market_price_from_apis
   
   price = get_market_price_from_apis('AAPL', preferred_source='tradier')
   ```

## Render Deployment

1. Go to your Render service dashboard
2. Navigate to **Environment** tab
3. Add the environment variables listed above
4. Redeploy your service

## Testing

Test the API integration:

```python
# In Django shell: python manage.py shell
from app.api_clients import get_tradier_quote, get_webull_quote

# Test Tradier
price = get_tradier_quote('AAPL')
print(f"AAPL price from Tradier: {price}")

# Test Webull
price = get_webull_quote('AAPL')
print(f"AAPL price from Webull: {price}")
```

## Fallback Behavior

If APIs are not configured or fail:
- System falls back to dummy/random price data
- Logs warnings but continues to function
- You'll see warnings in logs: "API key not configured"

## Troubleshooting

1. **"API key not configured" warning:**
   - Check environment variables are set correctly
   - Verify variable names match exactly (case-sensitive)

2. **API requests failing:**
   - Check API keys are valid and not expired
   - Verify network access from your server
   - Check API rate limits

3. **Wrong price data:**
   - Verify API endpoints are correct
   - Check response parsing in `api_clients.py`
   - Review API documentation for response format changes

