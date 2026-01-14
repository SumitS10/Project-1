## Options Tracking & Risk Dashboard

A web dashboard for tracking options positions and viewing portfolio risk metrics. Built with React + Django backend.

### Quick Start (Frontend Only)

1. Install dependencies:
```bash
npm install
```

2. Start dev server:
```bash
npm run dev
```

### Full Stack (Frontend + Backend)

**Option 1: Combined Deployment (Recommended)**
- Deploy everything together on one server
- See `DEPLOYMENT.md` for details

**Quick test:**
```bash
# 1. Build React
npm run build

# 2. Set up Django
cd backend
source ../venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate

# 3. Run server
python manage.py runserver
```
Visit `http://localhost:8000` - both frontend and API work!

**Option 2: Separate Deployment**
- Frontend → Netlify/Vercel (static hosting)
- Backend → Railway/Render (Django API)
- See `DEPLOYMENT.md` for details

### Features

- **Options tracking**: Interactive table where you can add, edit, or remove listed options positions (symbol, strike, expiry, type, quantity, premium, IV).
- **Risk summary**: High-level metrics including:
  - **Total delta**: Simple approximate delta exposure in underlying shares.
  - **Net premium**: Total premium paid/received across positions.
  - **Stress P/L (±15%)**: Hypothetical worst case P/L under ±15% price shocks.
  - **Configurable risk-free rate**: Used as a configurable assumption in your risk view.


