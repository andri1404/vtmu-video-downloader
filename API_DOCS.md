# 🔧 VTmu API Documentation - Maintenance & Monitoring

Dokumentasi lengkap API untuk maintenance dan monitoring website VTmu.

## 📊 Monitoring APIs

### 1. Health Check
**Cek status website dan versi dependencies**

```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-15T10:30:00",
  "version": {
    "app": "1.0.0",
    "python": "3.9.0",
    "ytdlp": "2025.9.26",
    "flask": "3.0.0"
  },
  "system": {
    "download_folder_size_mb": 125.5,
    "download_folder_files": 15
  },
  "uptime": "running"
}
```

**Cara Pakai:**
```bash
# Via cURL
curl https://your-site.vercel.app/api/health

# Via Browser
# Buka: https://your-site.vercel.app/api/health
```

---

### 2. View Logs
**Lihat 100 log terakhir untuk debugging**

```http
GET /api/logs
```

**Response:**
```json
{
  "logs": [
    "2025-01-15 10:30:00 - INFO - Health check successful",
    "2025-01-15 10:29:55 - INFO - Video downloaded successfully",
    ...
  ],
  "total_lines": 1500,
  "showing": 100,
  "timestamp": "2025-01-15T10:30:00"
}
```

**Cara Pakai:**
```bash
curl https://your-site.vercel.app/api/logs
```

---

## 🔄 Update & Maintenance APIs

### 3. Update yt-dlp
**Update yt-dlp ke versi terbaru (PENTING saat error!)**

```http
POST /api/update-ytdlp
```

**Response (Success):**
```json
{
  "success": true,
  "message": "yt-dlp updated successfully",
  "old_version": "2025.9.26",
  "new_version": "2025.10.15",
  "timestamp": "2025-01-15T10:30:00"
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "Update failed...",
  "timestamp": "2025-01-15T10:30:00"
}
```

**Cara Pakai:**
```bash
# Via cURL
curl -X POST https://your-site.vercel.app/api/update-ytdlp

# Via JavaScript (di browser console)
fetch('https://your-site.vercel.app/api/update-ytdlp', {
  method: 'POST'
})
.then(r => r.json())
.then(data => console.log(data));
```

**⚠️ CATATAN PENTING:**
- Update ini butuh waktu 30-60 detik
- Di Vercel, Anda perlu **redeploy** setelah update
- Gunakan API ini saat:
  - Video TikTok/YouTube error
  - Ada platform baru yang tidak support
  - Error "Unsupported URL"

---

### 4. Cleanup Downloads
**Hapus semua file di folder downloads untuk free up space**

```http
POST /api/cleanup-downloads
```

**Response:**
```json
{
  "success": true,
  "message": "Cleanup successful",
  "files_deleted": 25,
  "space_freed_mb": 450.5,
  "timestamp": "2025-01-15T10:30:00"
}
```

**Cara Pakai:**
```bash
# Via cURL
curl -X POST https://your-site.vercel.app/api/cleanup-downloads

# Via JavaScript
fetch('https://your-site.vercel.app/api/cleanup-downloads', {
  method: 'POST'
})
.then(r => r.json())
.then(data => console.log(data));
```

---

## 🛠️ Quick Fix Guide

### Skenario 1: Video TikTok/YouTube Tidak Bisa Didownload

**Problem:** Error "Unsupported URL" atau "Failed to download"

**Solution:**
```bash
# 1. Update yt-dlp
curl -X POST https://your-site.vercel.app/api/update-ytdlp

# 2. Redeploy di Vercel
# - Go to Vercel Dashboard
# - Deployments > Redeploy

# 3. Test again
```

---

### Skenario 2: Website Lambat / Storage Penuh

**Problem:** Website jadi lambat, mungkin storage penuh

**Solution:**
```bash
# 1. Check health
curl https://your-site.vercel.app/api/health

# 2. Lihat download_folder_size_mb
# Jika > 500 MB, cleanup

# 3. Cleanup
curl -X POST https://your-site.vercel.app/api/cleanup-downloads
```

---

### Skenario 3: Ada Error Tapi Tidak Tahu Penyebabnya

**Problem:** Error tidak jelas

**Solution:**
```bash
# 1. Check logs
curl https://your-site.vercel.app/api/logs

# 2. Cari error message di logs
# Look for "ERROR" keyword

# 3. Jika tidak ada info di logs, check health
curl https://your-site.vercel.app/api/health
```

---

## 📱 WhatsApp Automation (Bonus)

Anda bisa buat bot WhatsApp sederhana untuk maintenance via WA!

### Example: Auto Health Check via WhatsApp

```python
# Script sederhana untuk monitor via WhatsApp
import requests
import time

def check_health():
    response = requests.get('https://your-site.vercel.app/api/health')
    data = response.json()

    if data['status'] != 'healthy':
        # Send WhatsApp notification
        send_wa_message(
            f"⚠️ Website Unhealthy!\n"
            f"Error: {data.get('error', 'Unknown')}"
        )

# Run every hour
while True:
    check_health()
    time.sleep(3600)  # 1 hour
```

---

## 🔐 Security Notes

**⚠️ PENTING - Protect Your Update APIs!**

API `/api/update-ytdlp` dan `/api/cleanup-downloads` bisa di-abuse.

### Recommended: Add Simple Auth

Update app.py untuk tambah auth:

```python
from functools import wraps

# Secret key (simpan di environment variable)
UPDATE_API_KEY = os.environ.get('UPDATE_API_KEY', 'your-secret-key-123')

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key != UPDATE_API_KEY:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

# Tambahkan decorator
@app.route('/api/update-ytdlp', methods=['POST'])
@require_api_key
def update_ytdlp():
    # ... existing code
```

**Usage dengan auth:**
```bash
curl -X POST https://your-site.vercel.app/api/update-ytdlp \
  -H "X-API-Key: your-secret-key-123"
```

---

## 📊 Monitoring Schedule

### Recommended Monitoring:

| Task | Frequency | API |
|------|-----------|-----|
| Health Check | Every 5 min | `/api/health` |
| View Logs | When error | `/api/logs` |
| Update yt-dlp | Weekly | `/api/update-ytdlp` |
| Cleanup Downloads | Daily | `/api/cleanup-downloads` |

---

## 🚨 Error Codes Reference

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | All good! |
| 400 | Bad Request | Check URL validity |
| 403 | Forbidden | Path traversal detected |
| 404 | Not Found | File/endpoint not exist |
| 408 | Timeout | Update took too long |
| 500 | Server Error | Check logs |

---

## 💡 Pro Tips

1. **Bookmark Health Check**
   - Save `https://your-site.vercel.app/api/health` di browser
   - Check setiap hari

2. **Auto Update Script**
   - Buat cron job untuk auto-update weekly
   - Prevents errors sebelum terjadi

3. **Monitor Vercel Logs**
   - Vercel Dashboard > Logs
   - Combine dengan `/api/logs`

4. **Use Uptime Monitor**
   - UptimeRobot (free)
   - Ping `/api/health` every 5 minutes

---

## 📞 Support

Jika masih error setelah pakai API:

**WhatsApp:** https://wa.me/6283874636450  
**Developer:** Andri1404

---

Made with ❤️ for easy maintenance!
