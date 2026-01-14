# Deployment Guide

## Combined Deployment (Single Server) ✅ Recommended for Getting Started

Deploy both React frontend and Django backend together on one server.

### Quick Start

1. **Build React frontend:**
   ```bash
   npm run build
   ```

2. **Set up Django backend:**
   ```bash
   cd backend
   source ../venv/bin/activate  # or create new venv
   pip install -r requirements.txt
   python manage.py makemigrations
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

3. **Run locally:**
   ```bash
   python manage.py runserver
   ```
   Visit `http://localhost:8000` - both frontend and API work!

### Deploy to Production

#### Option A: Railway / Render (Easiest)

**Railway:**
1. Install Railway CLI: `npm i -g @railway/cli`
2. Login: `railway login`
3. Initialize: `railway init` (in project root)
4. Deploy: `railway up`

**Render:**
1. Create `render.yaml` in project root:
   ```yaml
   services:
     - type: web
       name: options-dashboard
       env: python
       buildCommand: |
         npm run build
         cd backend && pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
       startCommand: cd backend && gunicorn backend.wsgi:application
       envVars:
         - key: DJANGO_SETTINGS_MODULE
           value: backend.settings
   ```
2. Connect GitHub repo to Render dashboard

#### Option B: Traditional VPS (DigitalOcean, AWS EC2)

1. **SSH into server**
2. **Install dependencies:**
   ```bash
   sudo apt update
   sudo apt install python3-pip nginx
   npm install -g npm
   ```

3. **Clone and build:**
   ```bash
   git clone <your-repo>
   cd project-1
   npm run build
   cd backend
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

4. **Run with Gunicorn:**
   ```bash
   gunicorn backend.wsgi:application --bind 0.0.0.0:8000
   ```

5. **Configure Nginx** (reverse proxy):
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

---

## Separate Deployment (Advanced) 🔄 For Scaling

### Frontend → Netlify/Vercel (Free)

1. **Build React:**
   ```bash
   npm run build
   ```

2. **Deploy `dist/` folder:**
   - Netlify: Drag & drop `dist/` folder
   - Vercel: `vercel --prod`

3. **Set environment variable:**
   ```
   VITE_API_URL=https://your-django-backend.com
   ```

4. **Update React API calls** to use `import.meta.env.VITE_API_URL`

### Backend → Railway/Render/Heroku

1. **Deploy Django only:**
   ```bash
   cd backend
   # Follow platform-specific instructions
   ```

2. **Set CORS** in Django settings:
   ```python
   INSTALLED_APPS = [
       # ...
       'corsheaders',
   ]
   MIDDLEWARE = [
       'corsheaders.middleware.CorsMiddleware',
       # ...
   ]
   CORS_ALLOWED_ORIGINS = [
       "https://your-frontend.netlify.app",
   ]
   ```

---

## Environment Variables

Create `.env` file in `backend/`:
```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

---

## Database

Default uses SQLite (fine for small projects). For production, use PostgreSQL:

1. Install: `pip install psycopg2-binary`
2. Update `settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': os.environ.get('DB_NAME'),
           'USER': os.environ.get('DB_USER'),
           'PASSWORD': os.environ.get('DB_PASSWORD'),
           'HOST': os.environ.get('DB_HOST', 'localhost'),
           'PORT': os.environ.get('DB_PORT', '5432'),
       }
   }
   ```

---

## Quick Commands

```bash
# Build frontend
npm run build

# Run Django migrations
cd backend && python manage.py migrate

# Create superuser (for admin)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

