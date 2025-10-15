# 🚨 Quick Fix Guide - VTmu

Panduan cepat untuk fix error tanpa ribet!

## 🎯 3 Langkah Mudah Fix Error Apapun

### Langkah 1: Cek Health
```bash
curl https://vtmu.vercel.app/api/health
```
atau buka di browser: `https://vtmu.vercel.app/api/health`

### Langkah 2: Update yt-dlp (Jika Error Download)
```bash
curl -X POST https://vtmu.vercel.app/api/update-ytdlp
```

### Langkah 3: Redeploy
- Login ke vercel.com
- Pilih project VTmu
- Klik "Deployments"
- Klik "Redeploy" pada deployment terakhir
- Tunggu 2 menit
- DONE! ✅

---

## 📱 Cara Paling Mudah (Via Browser/HP)

### Fix Error TikTok/YouTube:

**Step 1:** Buka browser atau HP
**Step 2:** Copy link ini dan paste di browser:
```
https://vtmu.vercel.app/api/update-ytdlp
```
**Step 3:** Tunggu muncul response JSON seperti ini:
```json
{
  "success": true,
  "message": "yt-dlp updated successfully",
  "old_version": "2025.9.26",
  "new_version": "2025.10.15"
}
```
**Step 4:** Redeploy di Vercel (via HP juga bisa!)
**Step 5:** Test download lagi!

---

## 🔍 Troubleshooting by Error Message

### Error: "Unsupported URL"
**Penyebab:** yt-dlp butuh update
**Solusi:**
```bash
curl -X POST https://vtmu.vercel.app/api/update-ytdlp
# Lalu redeploy
```

### Error: "Failed to download"
**Penyebab:** URL tidak valid atau video private
**Solusi:**
1. Check URL valid
2. Pastikan video public
3. Update yt-dlp jika masih error

### Error: "File tidak ditemukan"
**Penyebab:** File sudah dihapus atau cleanup
**Solusi:** Download ulang video

### Error: "Timeout"
**Penyebab:** Video terlalu besar atau internet lambat
**Solusi:**
1. Pilih kualitas lebih rendah (480p instead of 1080p)
2. Check koneksi internet
3. Coba lagi

---

## 📊 Monitor Health Otomatis

### Setup UptimeRobot (Free):

1. Daftar di https://uptimerobot.com
2. Add New Monitor
3. Type: HTTP(s)
4. URL: `https://vtmu.vercel.app/api/health`
5. Interval: 5 minutes
6. Alert via: Email/WhatsApp
7. Save!

Sekarang Anda akan dapat notif otomatis jika website down!

---

## 💡 Pro Tips untuk Maintenance Mudah

### 1. Bookmark API Endpoints

Simpan di browser:
- Health Check: `https://vtmu.vercel.app/api/health`
- Update: `https://vtmu.vercel.app/api/update-ytdlp`
- Logs: `https://vtmu.vercel.app/api/logs`

### 2. Weekly Routine (5 Menit!)

Setiap Minggu, lakukan:
```bash
# 1. Check health
curl https://vtmu.vercel.app/api/health

# 2. Update yt-dlp
curl -X POST https://vtmu.vercel.app/api/update-ytdlp

# 3. Cleanup (optional)
curl -X POST https://vtmu.vercel.app/api/cleanup-downloads

# 4. Redeploy di Vercel
```

### 3. Auto-Fix Script (Termux/Linux)

Save sebagai `vtmu-fix.sh`:
```bash
#!/bin/bash
echo "🔧 VTmu Auto Fix Script"
echo "======================="

# Update yt-dlp
echo "📥 Updating yt-dlp..."
curl -X POST https://vtmu.vercel.app/api/update-ytdlp

echo ""
echo "✅ Update complete!"
echo "⚠️  Don't forget to redeploy in Vercel!"
```

Run:
```bash
chmod +x vtmu-fix.sh
./vtmu-fix.sh
```

---

## 🔄 Update Schedule Recommendation

| Task | When | How |
|------|------|-----|
| Update yt-dlp | Weekly | POST `/api/update-ytdlp` |
| Check Health | Daily | GET `/api/health` |
| View Logs | When error | GET `/api/logs` |
| Cleanup Storage | Monthly | POST `/api/cleanup-downloads` |

---

## 📱 Fix Via WhatsApp (Coming Soon)

Saya bisa buatkan WhatsApp bot untuk auto-fix jika Anda mau!

Features:
- Send "fix" → Auto update yt-dlp
- Send "health" → Get website status
- Send "logs" → Get recent errors
- Auto notification jika website down

**Interested?** Contact: https://wa.me/6283874636450

---

## ⚡ Emergency Contact

Jika semua cara di atas gagal:

**WhatsApp:** https://wa.me/6283874636450  
**Developer:** Andri1404  
**Response Time:** < 24 hours

---

## 🎓 Learn More

- [API_DOCS.md](API_DOCS.md) - Full API documentation
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide
- [README.md](README.md) - Project overview

---

Made with ❤️ for easy maintenance!

**Remember:** 
✅ Update Weekly = Zero Errors!
✅ Monitor Daily = Peace of Mind!
