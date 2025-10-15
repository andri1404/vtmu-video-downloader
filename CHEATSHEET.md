# 📋 VTmu - Quick Reference Cheat Sheet

Copy & paste commands untuk maintenance cepat!

## 🔧 API Endpoints

```bash
# Base URL (ganti dengan URL Anda)
BASE_URL="https://vtmu.vercel.app"
```

### 1. Health Check
```bash
curl $BASE_URL/api/health
# atau via browser:
# https://vtmu.vercel.app/api/health
```

### 2. Update yt-dlp
```bash
curl -X POST $BASE_URL/api/update-ytdlp
```

### 3. View Logs
```bash
curl $BASE_URL/api/logs
```

### 4. Cleanup Storage
```bash
curl -X POST $BASE_URL/api/cleanup-downloads
```

---

## 🚀 Common Tasks

### Fix TikTok/YouTube Error
```bash
# 1. Update yt-dlp
curl -X POST https://vtmu.vercel.app/api/update-ytdlp

# 2. Redeploy via Vercel CLI
vercel --prod

# Or redeploy via dashboard
```

### Weekly Maintenance (Copy-Paste!)
```bash
#!/bin/bash
echo "🔧 VTmu Weekly Maintenance"
echo "=========================="

# 1. Health check
echo "📊 Checking health..."
curl https://vtmu.vercel.app/api/health
echo ""

# 2. Update yt-dlp
echo "🔄 Updating yt-dlp..."
curl -X POST https://vtmu.vercel.app/api/update-ytdlp
echo ""

echo "✅ Maintenance complete!"
echo "⚠️  Remember to redeploy in Vercel!"
```

### Monthly Cleanup
```bash
# Cleanup downloads folder
curl -X POST https://vtmu.vercel.app/api/cleanup-downloads
```

---

## 📱 Browser Shortcuts

Bookmark these URLs:

```
Health:  https://vtmu.vercel.app/api/health
Update:  https://vtmu.vercel.app/api/update-ytdlp
Logs:    https://vtmu.vercel.app/api/logs
```

**Update via Browser:**
1. Paste: `https://vtmu.vercel.app/api/update-ytdlp`
2. Wait for JSON response
3. Redeploy in Vercel

---

## 🐛 Error Quick Fix

| Error | Command |
|-------|---------|
| TikTok error | `curl -X POST $URL/api/update-ytdlp` + redeploy |
| YouTube error | `curl -X POST $URL/api/update-ytdlp` + redeploy |
| Storage full | `curl -X POST $URL/api/cleanup-downloads` |
| Unknown error | `curl $URL/api/logs` |

---

## 📊 Monitoring Setup

### UptimeRobot Config
```
Type:     HTTP(s)
URL:      https://vtmu.vercel.app/api/health
Interval: 5 minutes
Alert:    Email / WhatsApp
```

---

## 🔐 Security (Optional)

### Add API Key Protection

In `app.py`:
```python
UPDATE_API_KEY = "your-secret-key-123"

# Then use:
curl -X POST https://vtmu.vercel.app/api/update-ytdlp \
  -H "X-API-Key: your-secret-key-123"
```

---

## 📅 Maintenance Schedule

```
DAILY:   curl https://vtmu.vercel.app/api/health
WEEKLY:  curl -X POST .../api/update-ytdlp + redeploy
MONTHLY: curl -X POST .../api/cleanup-downloads
```

---

## 📞 Emergency

WhatsApp: https://wa.me/6283874636450
Developer: Andri1404

---

**Quick Links:**
- [API_DOCS.md](API_DOCS.md) - Full documentation
- [QUICK_FIX_GUIDE.md](QUICK_FIX_GUIDE.md) - Troubleshooting
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deploy guide
