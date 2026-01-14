# Options Trading Feature

## Overview

The dashboard now includes a complete options trading section that allows you to:
- Set up complex options strategies (Vertical Spread, Iron Condor, Poor Man's Covered Call)
- Analyze risk metrics before trading
- Execute trades directly via Webull API

## Features

### Supported Strategies

1. **Vertical Spread**
   - Bull Call Spread / Bear Put Spread
   - 2 strikes (long and short)
   - Defined risk/reward

2. **Iron Condor**
   - 4 strikes (put spread + call spread)
   - High probability of profit
   - Limited risk

3. **Poor Man's Covered Call (PMCC)**
   - Long LEAPS call + short call
   - Lower capital requirement than traditional covered call
   - 2 strikes (LEAPS strike, short call strike)

### Risk Analysis

For each strategy, the system calculates:
- **Max Profit**: Maximum potential profit
- **Max Loss**: Maximum potential loss
- **Breakeven**: Price(s) where trade breaks even
- **Net Premium**: Total premium paid/received
- **Probability of Profit**: Estimated probability (simplified)
- **Risk/Reward Ratio**: Ratio of potential profit to potential loss

## API Endpoints

### Calculate Risk
```
POST /api/options/calculate-risk/
Body: {
  "strategy": "vertical" | "iron_condor" | "pmcc",
  "symbol": "AAPL",
  "expiry": "2025-03-21",
  "strikes": [150, 155],
  "quantities": [1, 1]
}
```

### Place Trade
```
POST /api/options/place-trade/
Body: {
  "strategy": "vertical",
  "symbol": "AAPL",
  "expiry": "2025-03-21",
  "strikes": [150, 155],
  "quantities": [1, 1],
  "action": "open" | "close"
}
```

## Webull API Configuration

To use the trading feature, configure Webull API credentials:

### Environment Variables

Add to Render dashboard or `.env` file:

```
WEBULL_API_KEY=your_webull_api_key
WEBULL_API_SECRET=your_webull_api_secret
WEBULL_BASE_URL=https://api.webull.com/api
```

### Getting Webull API Access

1. Contact Webull for API access (may require business account)
2. Obtain API credentials
3. Set environment variables in your deployment

**Note:** Webull API endpoints may vary. Adjust `api_clients.py` based on actual Webull API documentation.

## Usage Flow

1. **Select Strategy**: Choose from dropdown (Vertical, Iron Condor, PMCC)
2. **Enter Details**:
   - Symbol (e.g., AAPL)
   - Expiry date
   - Strikes (automatically adjusts based on strategy)
   - Quantities for each leg
3. **Analyze Risk**: Click "Analyze Risk" to see:
   - Max profit/loss
   - Breakeven points
   - Risk metrics
4. **Execute Trade**: If satisfied, click "Execute Trade" to place order via Webull

## Risk Calculations

### Vertical Spread
- **Max Profit**: (Spread width × 100 × min quantity) - Net premium
- **Max Loss**: Net premium paid
- **Breakeven**: Long strike ± (Net premium / (Quantity × 100))

### Iron Condor
- **Max Profit**: Net premium received
- **Max Loss**: (Wider spread width × 100) - Net premium
- **Breakeven**: Two points (lower and upper)

### PMCC
- **Max Profit**: ((Short strike - Long strike) × 100 × quantity) - Net premium
- **Max Loss**: Net premium paid
- **Breakeven**: Long strike + (Net premium / (Quantity × 100))

## Important Notes

1. **API Integration**: The Webull API integration is a template. You may need to adjust endpoints and payloads based on Webull's actual API documentation.

2. **Premium Estimation**: If premiums aren't provided, the system estimates them. For accurate risk analysis, use real option prices from the API.

3. **Order Execution**: Trade execution requires valid Webull API credentials and proper authentication.

4. **Testing**: Test with paper trading/simulated accounts before using real money.

5. **Risk Disclaimer**: Options trading involves significant risk. Always verify calculations and understand the risks before executing trades.

## Future Enhancements

- Real-time option chain data
- Greeks calculation (Delta, Gamma, Theta, Vega)
- P&L charts
- Position management (close trades)
- Multiple broker support (Tradier, etc.)
- Paper trading mode

