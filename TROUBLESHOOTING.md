# Troubleshooting Guide

## Common Errors and Solutions

### 500 Errors on API Endpoints

**Symptoms:**
- `/api/fidelity-trades/` returns 500
- `/api/tradier-trades/` returns 500
- `/api/webull-trades/` returns 500

**Causes & Solutions:**

1. **Database Migrations Not Run**
   ```bash
   # On Render: Check build logs
   # Should see: python manage.py migrate
   
   # If migrations failed, manually run:
   cd backend
   python manage.py migrate
   ```

2. **Missing Database Tables**
   - The models changed but migrations weren't applied
   - Solution: Run migrations on your server

3. **Import Errors**
   - Check if `api_clients.py` has syntax errors
   - Check if `requests` package is installed

### 400 Error on Upload Endpoints

**Symptoms:**
- `/api/upload-webull/` returns 400

**Causes & Solutions:**

1. **CSV Format Issues**
   - CSV must have required columns: `trade_id`, `trade_date`, `symbol`, `strategy`, `strike`, `action`, `quantity`, `premium`, `expiry`
   - Check CSV file format matches expected structure

2. **Missing Required Fields**
   - Some fields might be required but missing in CSV
   - Solution: Ensure CSV has all required columns

3. **Date Parsing Errors**
   - Dates must be in valid format (YYYY-MM-DD)
   - Solution: Check date format in CSV

### Fix Steps for Render Deployment

1. **Check Build Logs**
   - Go to Render dashboard → Your service → Logs
   - Look for migration errors

2. **Run Migrations Manually (if needed)**
   - Use Render Shell or SSH
   ```bash
   cd backend
   python manage.py migrate
   ```

3. **Check Environment Variables**
   - Ensure all required env vars are set
   - Check for typos in variable names

4. **Verify Dependencies**
   - Check `requirements.txt` includes all packages
   - Ensure `requests==2.31.0` is included

### Testing Locally

```bash
# 1. Run migrations
cd backend
python manage.py migrate

# 2. Test API endpoints
python manage.py runserver

# 3. Test in browser/Postman
curl http://localhost:8000/api/fidelity-trades/
curl http://localhost:8000/api/tradier-trades/
curl http://localhost:8000/api/webull-trades/
```

### Debugging Steps

1. **Check Django Logs**
   ```python
   # In settings.py, ensure logging is configured
   LOGGING = {
       'version': 1,
       'disable_existing_loggers': False,
       'handlers': {
           'console': {
               'class': 'logging.StreamHandler',
           },
       },
       'root': {
           'handlers': ['console'],
           'level': 'INFO',
       },
   }
   ```

2. **Test Serializers**
   ```python
   # In Django shell: python manage.py shell
   from app.models import FidelityTrade
   from app.serializers import FidelityTradeSerializer
   
   trade = FidelityTrade.objects.first()
   serializer = FidelityTradeSerializer(trade)
   print(serializer.data)
   ```

3. **Check Database**
   ```python
   # In Django shell
   from app.models import FidelityTrade, TradierTrade, WebullTrade
   
   print(FidelityTrade.objects.count())
   print(TradierTrade.objects.count())
   print(WebullTrade.objects.count())
   ```

## Quick Fixes

### If migrations are the issue:
```bash
# On Render, add to build command:
python manage.py makemigrations
python manage.py migrate
```

### If serializers are the issue:
- Check that computed fields (`option_type`, `pnl`) are working
- Verify model fields match serializer expectations

### If imports are failing:
- Check `api_clients.py` exists and has no syntax errors
- Verify `requests` is in `requirements.txt`

