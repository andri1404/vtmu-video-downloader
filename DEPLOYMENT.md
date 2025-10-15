# 🚀 Panduan Deployment VTmu ke Vercel

Dokumentasi lengkap cara deploy website VTmu Video Downloader ke Vercel.

## 📋 Prasyarat

Sebelum deploy, pastikan Anda sudah punya:

- ✅ Akun GitHub (gratis di [github.com](https://github.com))
- ✅ Akun Vercel (gratis di [vercel.com](https://vercel.com))
- ✅ Project sudah di-push ke GitHub repository

## 🎯 Metode 1: Deploy via Vercel Dashboard (Recommended)

### Step 1: Login ke Vercel

1. Buka [vercel.com](https://vercel.com)
2. Klik **"Sign Up"** jika belum punya akun
3. Login dengan GitHub account Anda
4. Authorize Vercel untuk mengakses GitHub repositories

### Step 2: Import Project

1. Di Vercel Dashboard, klik tombol **"Add New Project"**
2. Pilih **"Import Git Repository"**
3. Cari dan pilih repository **"video-downloader-website"**
4. Klik **"Import"**

### Step 3: Configure Project

Vercel akan otomatis detect bahwa ini adalah Python project:

```
Framework Preset: Other
Build Command: (leave empty)
Output Directory: (leave empty)
Install Command: pip install -r requirements.txt
```

**PENTING:** Tidak perlu ubah apapun, biarkan default!

### Step 4: Deploy

1. Klik tombol **"Deploy"**
2. Tunggu 2-3 menit proses deployment
3. ✅ Website sudah live!
4. Copy URL deployment (contoh: `https://vtmu.vercel.app`)

### Step 5: Custom Domain (Opsional)

Jika ingin pakai custom domain:

1. Di Project Settings, pilih tab **"Domains"**
2. Klik **"Add Domain"**
3. Masukkan domain Anda (contoh: `vtmu.com`)
4. Ikuti instruksi DNS configuration
5. Tunggu propagasi DNS (5-15 menit)

## 🖥️ Metode 2: Deploy via Vercel CLI

### Step 1: Install Vercel CLI

```bash
# Via NPM
npm i -g vercel

# Via Yarn
yarn global add vercel
```

### Step 2: Login

```bash
vercel login
```

Pilih method login (GitHub/Email) dan authorize.

### Step 3: Deploy

```bash
# Navigate ke project folder
cd /path/to/video-downloader-website

# Deploy to preview
vercel

# Atau deploy langsung ke production
vercel --prod
```

### Step 4: Konfigurasi (Jika Diminta)

```
? Set up and deploy? Yes
? Which scope? (pilih account Anda)
? Link to existing project? No
? What's your project's name? vtmu
? In which directory is your code located? ./
? Want to override the settings? No
```

## 🔧 Environment Variables

Tidak ada environment variable yang wajib! Tapi jika ingin menambahkan:

```bash
# Via Dashboard
Settings > Environment Variables

# Via CLI
vercel env add VARIABLE_NAME
```

## 📦 File-file Penting

Pastikan file-file ini ada di repository:

```
video-downloader-website/
├── app.py                 # Main application
├── requirements.txt       # Python dependencies
├── vercel.json           # Vercel configuration
├── .gitignore            # Files to ignore
├── README.md             # Documentation
├── static/               # CSS, JS, images
│   ├── css/
│   └── js/
└── templates/            # HTML templates
    ├── index.html
    ├── faq.html
    ├── how-to-use.html
    └── download.html
```

## ✅ Checklist Sebelum Deploy

- [ ] Semua file sudah di commit ke GitHub
- [ ] `requirements.txt` berisi semua dependencies
- [ ] `vercel.json` sudah dikonfigurasi
- [ ] `.gitignore` sudah exclude folder `downloads/`
- [ ] Tidak ada file sensitive (API keys, passwords)
- [ ] Test locally dengan `python app.py`

## 🐛 Troubleshooting

### 1. Build Failed

**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solusi:**
```bash
# Pastikan requirements.txt lengkap
Flask==3.0.0
yt-dlp==2025.9.26
Werkzeug==3.0.1
flask-limiter==3.5.0
```

### 2. 404 Not Found

**Error:** Pages tidak load

**Solusi:**
- Check `vercel.json` routing configuration
- Pastikan `templates/` folder ada
- Verify file paths di app.py

### 3. Static Files 404

**Error:** CSS/JS tidak load

**Solusi:**
- Pastikan `static/` folder ada di root
- Check path di HTML: `/static/css/style.css`
- Verify `vercel.json` static file routing

### 4. Download Tidak Bekerja

**Error:** Video tidak terdownload

**Solusi:**
- Update yt-dlp ke versi latest
- Check yt-dlp compatibility
- Vercel mungkin ada timeout (10 seconds serverless)

### 5. CORS Error

**Solusi sudah ditambahkan di app.py:**
```python
@app.after_request
def add_security_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
```

## 🔐 Keamanan

File `vercel.json` sudah include security headers:

```json
{
  "headers": [
    {
      "key": "X-Content-Type-Options",
      "value": "nosniff"
    },
    {
      "key": "X-Frame-Options",
      "value": "DENY"
    },
    {
      "key": "X-XSS-Protection",
      "value": "1; mode=block"
    }
  ]
}
```

File `app.py` sudah include:
- ✅ URL validation
- ✅ Filename sanitization
- ✅ Path traversal protection
- ✅ Security headers

## 📊 Monitoring

### Vercel Analytics (Free)

1. Go to Project > Analytics
2. View:
   - Page views
   - Unique visitors
   - Top pages
   - Geographic data

### Vercel Logs

```bash
# View logs via CLI
vercel logs <deployment-url>

# Or via Dashboard
Project > Deployments > Select deployment > Logs
```

## 🔄 Update & Re-deploy

### Auto Deploy (Default)

Setiap push ke GitHub akan otomatis trigger deployment:

```bash
git add .
git commit -m "Update feature X"
git push origin main
```

Vercel akan otomatis detect dan deploy!

### Manual Deploy

```bash
# Via CLI
vercel --prod

# Via Dashboard
Deployments > Redeploy
```

## 💡 Tips & Best Practices

1. **Use Production Branch**
   - Main branch untuk production
   - Dev branch untuk testing

2. **Enable Preview Deployments**
   - Otomatis create preview URL untuk setiap PR
   - Test sebelum merge ke production

3. **Monitor Quotas**
   - Free plan: 100GB bandwidth/month
   - 100 deployments/day
   - Serverless function timeout: 10 seconds

4. **Optimize Performance**
   - Minify CSS/JS
   - Compress images
   - Use CDN untuk static assets

5. **Backup Downloads Folder**
   - Downloads folder akan reset setiap deployment
   - Tidak cocok untuk persistent storage
   - Gunakan cloud storage jika perlu

## 🆘 Butuh Bantuan?

**Developer Contact:**
- WhatsApp: [Andri1404](https://wa.me/6283874636450)

**Resources:**
- [Vercel Documentation](https://vercel.com/docs)
- [yt-dlp GitHub](https://github.com/yt-dlp/yt-dlp)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 🎉 Selamat!

Website Anda sudah live di internet! 🚀

Share link website Anda:
```
https://your-project.vercel.app
```

---

Made with ❤️ by [Andri1404](https://wa.me/6283874636450)
