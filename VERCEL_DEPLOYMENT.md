# 🚀 Panduan Deploy VTmu ke Vercel

## ✅ File yang Sudah Disiapkan

- ✅ `vercel.json` - Konfigurasi Vercel
- ✅ `requirements.txt` - Dependencies Python
- ✅ `.gitignore` - File yang tidak diupload
- ✅ `README.md` - Dokumentasi
- ✅ `app.py` - Main Flask application

## 📋 Langkah Deploy ke Vercel

### 1️⃣ Install Vercel CLI

```bash
# Install Vercel CLI globally
npm i -g vercel
```

### 2️⃣ Login ke Vercel

```bash
vercel login
```

Pilih metode login (GitHub, GitLab, Bitbucket, atau Email)

### 3️⃣ Deploy Project

```bash
# Deploy pertama kali (preview)
vercel

# Deploy ke production
vercel --prod
```

### 4️⃣ Konfigurasi Otomatis

Saat deploy, Vercel akan menanyakan:

```
? Set up and deploy "~/video-downloader-website"? [Y/n] Y
? Which scope do you want to deploy to? [Your Account]
? Link to existing project? [y/N] N
? What's your project's name? vtmu
? In which directory is your code located? ./
```

Jawab sesuai preferensi Anda.

## 🌐 Deploy via GitHub (Recommended)

### 1️⃣ Push ke GitHub

```bash
# Initialize git (jika belum)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: VTmu video downloader"

# Add remote repository
git remote add origin https://github.com/username/vtmu.git

# Push to GitHub
git push -u origin main
```

### 2️⃣ Connect ke Vercel

1. Buka https://vercel.com/new
2. Import Git Repository
3. Pilih repository Anda
4. Vercel akan otomatis detect Flask app
5. Klik "Deploy"

## ⚙️ Environment Variables (Opsional)

Jika diperlukan, tambahkan di Vercel Dashboard:

- `FLASK_ENV=production`
- `PYTHON_VERSION=3.11`

## 📝 Struktur Project

```
video-downloader-website/
├── app.py                  # Main Flask app
├── vercel.json            # Vercel config
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── README.md             # Documentation
├── static/               # CSS, JS, images
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
└── templates/            # HTML templates
    ├── index.html
    ├── download.html
    ├── how-to-use.html
    └── faq.html
```

## 🔧 Troubleshooting

### Error: "Module not found"
- Pastikan semua dependencies ada di `requirements.txt`
- Rebuild project di Vercel dashboard

### Error: "Build timeout"
- yt-dlp membutuhkan waktu install yang lama
- Tunggu beberapa menit atau coba deploy ulang

### Error: "Function timeout"
- Vercel free plan memiliki timeout 10 detik
- Upgrade ke Pro plan untuk timeout 60 detik
- Atau gunakan platform lain (Railway, Render, dll)

## 💡 Tips

1. **Custom Domain**: Tambahkan custom domain di Vercel dashboard
2. **Analytics**: Enable Vercel Analytics untuk monitoring
3. **Auto Deploy**: Setiap push ke GitHub akan auto deploy
4. **Preview URL**: Setiap PR mendapat preview URL

## 🎯 Alternatif Platform

Jika Vercel tidak cocok, coba:

- **Railway**: https://railway.app (lebih generous timeout)
- **Render**: https://render.com (free tier bagus)
- **Fly.io**: https://fly.io (global deployment)
- **PythonAnywhere**: https://pythonanywhere.com (khusus Python)

## 🔗 Useful Links

- Vercel Docs: https://vercel.com/docs
- Vercel Python: https://vercel.com/docs/functions/serverless-functions/runtimes/python
- Flask on Vercel: https://vercel.com/guides/using-flask-with-vercel

## ✅ Checklist Deploy

- [ ] Install Vercel CLI
- [ ] Login ke Vercel
- [ ] Push code ke GitHub (opsional)
- [ ] Run `vercel --prod`
- [ ] Test URL yang diberikan
- [ ] Setup custom domain (opsional)
- [ ] Enable analytics (opsional)

## 🎉 Setelah Deploy

Website Anda akan live di URL seperti:
`https://vtmu.vercel.app`

atau

`https://your-project-name.vercel.app`

Selamat! 🚀
