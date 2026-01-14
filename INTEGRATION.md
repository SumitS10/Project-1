# Frontend-Backend Integration

## ✅ What's Integrated

The React frontend is now fully integrated with the Django backend:

### 1. **API Client** (`src/api.ts`)
- `uploadFidelityCSV()` - Upload Fidelity CSV files
- `uploadTradierCSV()` - Upload Tradier CSV files
- `fetchFidelityTrades()` - Fetch all Fidelity trades
- `fetchTradierTrades()` - Fetch all Tradier trades
- `fetchAllPositions()` - Fetch and merge all trades into positions
- `convertTradeToPosition()` - Convert backend trade format to frontend format

### 2. **CSV Upload Component** (`src/components/CSVUpload.tsx`)
- Upload buttons for Fidelity and Tradier CSVs
- Loading states and error handling
- Success notifications
- Auto-refresh positions after upload

### 3. **App Integration** (`src/App.tsx`)
- Automatically loads positions from backend on mount
- Falls back to sample data if backend unavailable
- Refresh function to reload data after CSV uploads
- Loading and error states

### 4. **Toolbar Updates** (`src/components/Toolbar.tsx`)
- Added CSV upload buttons
- Refresh callback to reload data

## 🔄 Data Flow

```
1. User uploads CSV → Frontend sends to Django API
2. Django parses CSV → Saves to database
3. Frontend fetches trades → Converts to OptionPosition format
4. Positions displayed in OptionsTable
5. Risk calculations use positions data
```

## 🧪 Testing the Integration

### 1. Start Backend
```bash
cd backend
source ../venv/bin/activate
python manage.py migrate
python manage.py runserver
```

### 2. Build & Test Frontend
```bash
npm run build
# Or for dev:
npm run dev
```

### 3. Test CSV Upload
1. Create a test CSV file with columns:
   - `symbol`, `trade_date`, `option_type`, `strike`, `expiry`, `quantity`, `premium`
2. Click "Upload Fidelity CSV" or "Upload Tradier CSV"
3. Select your CSV file
4. Positions should appear in the table

### 4. Test API Endpoints Directly
```bash
# Fetch trades
curl http://localhost:8000/api/fidelity-trades/
curl http://localhost:8000/api/tradier-trades/
```

## 📝 CSV Format Expected

Your CSV files should have these columns (case-insensitive):
- `symbol` - Stock ticker (e.g., "AAPL")
- `trade_date` - Date in YYYY-MM-DD format
- `option_type` - "CALL" or "PUT"
- `strike` - Strike price (number)
- `expiry` - Expiry date in YYYY-MM-DD format
- `quantity` - Number of contracts (positive = long, negative = short)
- `premium` - Premium per contract

Example CSV:
```csv
symbol,trade_date,option_type,strike,expiry,quantity,premium
AAPL,2025-01-15,CALL,190,2025-03-21,10,6.5
AAPL,2025-01-15,PUT,185,2025-03-21,-5,4.2
```

## 🔧 Configuration

### API Base URL
The frontend uses `/api` as the base URL by default (works with combined deployment).

For separate deployments, set environment variable:
```bash
VITE_API_URL=https://your-backend.com/api
```

Then rebuild:
```bash
npm run build
```

## 🐛 Troubleshooting

### Backend not available
- Frontend will show warning and use sample data
- Check Django server is running on port 8000
- Check browser console for CORS errors (if separate deployment)

### CSV upload fails
- Check CSV format matches expected columns
- Check Django logs for parsing errors
- Verify file is valid CSV

### Positions not loading
- Check browser network tab for API calls
- Verify Django migrations are run: `python manage.py migrate`
- Check database has data: Django admin at `/admin/`

