# 🚀 Netlify Deployment Guide - VTmu

## 📋 Daftar Isi
1. [Prerequisites](#prerequisites)
2. [Method 1: Deploy via Netlify Dashboard (RECOMMENDED)](#method-1-deploy-via-netlify-dashboard)
3. [Method 2: Deploy via Netlify CLI](#method-2-deploy-via-netlify-cli)
4. [Method 3: Deploy via GitHub](#method-3-deploy-via-github)
5. [Configuration](#configuration)
6. [Custom Domain](#custom-domain)
7. [Environment Variables](#environment-variables)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

✅ **Yang Anda Butuhkan:**
- Akun Netlify (gratis) - [Sign up di netlify.com](https://app.netlify.com/signup)
- Repository GitHub/GitLab (optional tapi recommended)
- Source code VTmu yang sudah lengkap

⚠️ **PENTING - Netlify vs Vercel:**

**Netlify:**
- ✅ Free tier generous
- ✅ Easy setup
- ❌ Functions timeout 10 detik (free tier)
- ⚠️ **TIDAK COCOK** untuk video download yang lama
- ✅ Cocok untuk static sites + API ringan

**Vercel (RECOMMENDED untuk VTmu):**
- ✅ Functions timeout 60 detik (free tier)
- ✅ Better untuk Python apps
- ✅ **COCOK** untuk video downloader
- ✅ Unlimited bandwidth

**Rekomendasi:** Gunakan **Vercel** untuk VTmu karena timeout lebih lama!

---

## Method 1: Deploy via Netlify Dashboard

### Step 1: Prepare Repository

```bash
# Initialize git (jika belum)
cd video-downloader-website
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit for Netlify deployment"

# Create GitHub repo dan push
# (Buat repo baru di github.com terlebih dahulu)
git remote add origin https://github.com/username/vtmu.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy di Netlify

1. **Login ke Netlify**
   - Buka [app.netlify.com](https://app.netlify.com/)
   - Login dengan GitHub/GitLab/Email

2. **Import Project**
   - Click **"Add new site"** → **"Import an existing project"**
   - Pilih **GitHub** (atau platform lain)
   - Authorize Netlify untuk akses repo
   - Pilih repository **vtmu**

3. **Configure Build Settings**
   ```
   Build command: pip install -r requirements.txt
   Publish directory: .
   Functions directory: functions
   ```

4. **Deploy**
   - Click **"Deploy site"**
   - Tunggu proses build (2-5 menit)
   - Site akan live di `random-name.netlify.app`

### Step 3: Test Deployment

```bash
# Test health check
curl https://your-site.netlify.app/api/health

# Test CMS API
curl https://your-site.netlify.app/api/cms/config
```

---

## Method 2: Deploy via Netlify CLI

### Step 1: Install Netlify CLI

```bash
# Install globally
npm install -g netlify-cli

# Atau via pkg
pkg install netlify-cli
```

### Step 2: Login

```bash
netlify login
# Browser akan terbuka, authorize Netlify CLI
```

### Step 3: Deploy

```bash
# Navigate ke project folder
cd video-downloader-website

# Initialize Netlify project
netlify init

# Pilih opsi:
# - "Create & configure a new site"
# - Team: Your team
# - Site name: vtmu (atau nama lain)

# Deploy to production
netlify deploy --prod
```

### Step 4: Verify

```bash
# Open site in browser
netlify open:site

# Check functions
netlify functions:list
```

---

## Method 3: Deploy via GitHub (Continuous Deployment)

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Deploy VTmu to Netlify"
git remote add origin https://github.com/username/vtmu.git
git push -u origin main
```

### Step 2: Connect to Netlify

1. Di Netlify Dashboard:
   - **Add new site** → **Import an existing project**
   - Pilih **GitHub**
   - Select repository **vtmu**

2. Build settings akan auto-detect dari `netlify.toml`

3. Click **Deploy**

### Step 3: Continuous Deployment Active!

Setiap push ke GitHub akan otomatis deploy:

```bash
# Make changes
git add .
git commit -m "Update feature"
git push

# Netlify akan auto-deploy dalam 2-3 menit
```

---

## Configuration

### File Configuration

**netlify.toml** (sudah ada di project):
```toml
[build]
  command = "pip install -r requirements.txt"
  publish = "."

[functions]
  directory = "functions"

[[redirects]]
  from = "/*"
  to = "/.netlify/functions/api/:splat"
  status = 200
```

**runtime.txt** (sudah ada):
```
3.9
```

**functions/api.py** (sudah ada):
```python
from app import app
import serverless_wsgi

def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)
```

---

## Custom Domain

### Step 1: Add Domain

1. Di Netlify Dashboard → **Domain settings**
2. Click **Add custom domain**
3. Enter domain: `vtmu.com` atau `download.yoursite.com`

### Step 2: Configure DNS

Di DNS provider (Cloudflare, Namecheap, dll):

**Option A: Apex Domain (vtmu.com)**
```
Type: A
Name: @
Value: 75.2.60.5 (Netlify IP)
```

**Option B: Subdomain (download.yoursite.com)**
```
Type: CNAME
Name: download
Value: your-site.netlify.app
```

### Step 3: Enable HTTPS

- Netlify auto-provision SSL certificate
- Tunggu 1-24 jam untuk DNS propagation
- HTTPS akan aktif otomatis

---

## Environment Variables

### Set di Netlify Dashboard

1. **Site settings** → **Environment variables**
2. Add variables:

```
Key: CMS_API_KEY
Value: your-secret-key-here

Key: FLASK_ENV
Value: production

Key: MAX_CONTENT_LENGTH
Value: 104857600
```

### Access di Code

```python
import os

api_key = os.getenv('CMS_API_KEY')
```

---

## Troubleshooting

### Problem 1: Function Timeout

**Error:**
```
Task timed out after 10.00 seconds
```

**Solution:**
- Netlify free tier: 10 detik timeout
- Upgrade ke Pro ($19/month) untuk 26 detik
- **ATAU** gunakan Vercel (60 detik free)

**Temporary Fix:**
```python
# Di app.py, tambah timeout handling
from flask import request, abort

@app.before_request
def check_timeout():
    # Reject requests yang mungkin timeout
    if 'download' in request.path:
        # Implement queue system atau async download
        pass
```

### Problem 2: Module Not Found

**Error:**
```
ModuleNotFoundError: No module named 'yt_dlp'
```

**Solution:**
```bash
# Pastikan requirements.txt lengkap
cat requirements.txt

# Harus berisi:
Flask==3.0.0
yt-dlp==2025.9.26
Werkzeug==3.0.1
flask-limiter==3.5.0
serverless-wsgi==3.0.3

# Re-deploy
netlify deploy --prod
```

### Problem 3: Static Files Not Loading

**Error:**
CSS/JS tidak load

**Solution:**

Check `netlify.toml`:
```toml
[[redirects]]
  from = "/static/*"
  to = "/static/:splat"
  status = 200

[[redirects]]
  from = "/*"
  to = "/.netlify/functions/api/:splat"
  status = 200
```

Order matters! Static harus sebelum catch-all.

### Problem 4: CORS Errors

**Error:**
```
Access to fetch has been blocked by CORS policy
```

**Solution:**

Di `app.py`, pastikan CORS headers ada:
```python
@app.after_request
def add_security_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response
```

### Problem 5: Config Files Not Found

**Error:**
```
Configuration not found
```

**Solution:**
```bash
# Pastikan config folder di-commit
git add config/
git commit -m "Add config files"
git push

# Atau uncomment di .gitignore
# config/
```

### Problem 6: Downloads Folder Permission

**Error:**
```
PermissionError: [Errno 13] Permission denied: 'downloads'
```

**Solution:**
```python
# Di app.py, gunakan /tmp untuk Netlify
import os

if os.getenv('NETLIFY'):
    DOWNLOAD_FOLDER = '/tmp/downloads'
else:
    DOWNLOAD_FOLDER = 'downloads'

Path(DOWNLOAD_FOLDER).mkdir(exist_ok=True)
```

---

## Performance Tips

### 1. Enable Edge Functions (Beta)

Netlify Edge Functions lebih cepat dari serverless functions:

```toml
# netlify.toml
[functions]
  directory = "functions"

[edge_functions]
  path = "edge-functions"
```

### 2. Cache Configuration

```toml
[[headers]]
  for = "/static/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000"
```

### 3. Compress Responses

```python
# Di app.py
from flask_compress import Compress

app = Flask(__name__)
Compress(app)
```

Add to requirements.txt:
```
flask-compress==1.14
```

---

## Monitoring

### Netlify Analytics

1. **Site settings** → **Analytics**
2. Enable Netlify Analytics ($9/month)

Features:
- Page views
- Unique visitors
- Bandwidth usage
- Top pages

### Free Alternative: Google Analytics

Add to `templates/base.html`:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

---

## Logs & Debugging

### View Logs

```bash
# Via CLI
netlify logs

# Real-time logs
netlify logs:function api --stream

# Via Dashboard
# Site → Functions → Click function → View logs
```

### Debug Mode

```bash
# Deploy dengan debug
NETLIFY_DEBUG=true netlify deploy --prod
```

---

## Limits (Free Tier)

| Resource | Limit |
|----------|-------|
| Bandwidth | 100 GB/month |
| Build minutes | 300 min/month |
| Function invocations | 125K/month |
| Function runtime | 10 seconds |
| Concurrent builds | 1 |
| Sites | Unlimited |

**Upgrade ke Pro ($19/month):**
- Bandwidth: 400 GB
- Build minutes: 1,000
- Function runtime: 26 seconds
- Concurrent builds: 3

---

## Migration dari Vercel ke Netlify

### Step 1: Export Vercel Config

```bash
# vercel.json settings → netlify.toml
```

### Step 2: Update Code

```python
# Change Vercel-specific code
# Before (Vercel):
if os.getenv('VERCEL'):
    ...

# After (Netlify):
if os.getenv('NETLIFY'):
    ...
```

### Step 3: Deploy

```bash
netlify deploy --prod
```

### Step 4: Update DNS

Point domain dari Vercel ke Netlify.

---

## CI/CD Workflow

### GitHub Actions + Netlify

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Netlify

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Deploy to Netlify
        uses: netlify/actions/cli@master
        env:
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
        with:
          args: deploy --prod
```

---

## Backup & Rollback

### Create Backup

```bash
# Download site content
netlify sites:list
netlify pull --site-id your-site-id
```

### Rollback

1. **Via Dashboard:**
   - **Deploys** → Find previous deploy
   - Click **"Publish deploy"**

2. **Via CLI:**
```bash
netlify rollback
```

---

## Security Checklist

✅ Environment variables set
✅ HTTPS enabled
✅ Security headers configured
✅ CORS properly set
✅ Input validation active
✅ API rate limiting enabled
✅ Error logging configured
✅ Secrets in environment (not code)

---

## ⚠️ REKOMENDASI FINAL

**Untuk VTmu Video Downloader:**

**GUNAKAN VERCEL**, bukan Netlify!

**Alasan:**
1. ⏱️ **Timeout:** Vercel 60s vs Netlify 10s
2. 🐍 **Python Support:** Vercel lebih baik
3. 🎬 **Video Download:** Butuh waktu lama
4. 💰 **Free Tier:** Vercel lebih generous

**Netlify cocok untuk:**
- Static sites
- JAMstack apps
- API ringan (< 10 detik)
- Form submissions
- Identity management

**Kalau tetap mau Netlify:**
- Implementasi download queue system
- Gunakan external storage (S3)
- Background jobs dengan webhooks
- Client-side download (CORS proxy)

---

## 📞 Support

**Need help?**
- Netlify Community: [community.netlify.com](https://community.netlify.com)
- Netlify Docs: [docs.netlify.com](https://docs.netlify.com)
- WhatsApp: wa.me/6283874636450 (Andri1404)

---

**Selamat Deploy! 🚀**

*Tapi ingat, Vercel lebih cocok untuk VTmu!*
