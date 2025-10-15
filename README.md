# VTmu - Video TikTok Downloader Multiplatform

Download video dari berbagai platform social media tanpa watermark. Gratis, cepat, dan mudah!

## 🚀 Features

- ✅ **Multi-Platform Support**: TikTok, YouTube, Instagram, Twitter, dan lebih banyak lagi
- ✅ **No Watermark**: Video bersih tanpa logo
- ✅ **Multiple Quality Options**: Best, 720p, 480p, 360p, Audio Only
- ✅ **Fast Download**: Process dalam hitungan detik
- ✅ **Modern UI/UX**: Desain yang elegan dan user-friendly
- ✅ **Mobile Responsive**: Berfungsi sempurna di semua device
- ✅ **100% Free**: Tidak ada biaya atau registrasi

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Downloader**: yt-dlp
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Deployment**: Vercel

## 📦 Installation

```bash
# Clone repository
git clone <repository-url>
cd video-downloader-website

# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py
```

Server akan berjalan di `http://localhost:5000`

## 🌐 Deploy ke Vercel

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Login ke Vercel:
```bash
vercel login
```

3. Deploy:
```bash
vercel --prod
```

## 📝 Environment Variables

Tidak ada environment variables yang diperlukan untuk versi dasar.

## 🎨 Customization

### Mengubah Branding
Edit file di `templates/index.html` untuk mengubah logo, nama, dan tagline.

### Mengubah Theme
Edit file `static/css/style.css` pada bagian `:root` untuk mengubah warna theme.

## 🔒 Security Features

- Rate limiting untuk mencegah abuse
- Input validation untuk mencegah injection attacks
- Filename sanitization untuk mencegah path traversal
- Security headers (CSP, XSS Protection, dll)

## 📄 License

MIT License - Feel free to use for personal or commercial projects

## 👨‍💻 Developer

Developed by **Andri1404**

## 🙏 Credits

- yt-dlp for the amazing video download library
- Flask for the web framework
- Font Awesome for the icons
