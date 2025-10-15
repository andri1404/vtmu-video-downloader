# 🎨 Content Management System (CMS) API Documentation

## Overview

VTmu sekarang dilengkapi dengan **Content Management System (CMS) API** yang memungkinkan Anda untuk:

✅ **Update seluruh konten website tanpa edit code**
✅ **Ganti branding, warna, dan tema secara dinamis**
✅ **Ubah FAQ, tutorial, dan fitur-fitur**
✅ **Kelola website dari browser atau API client**

Semua perubahan disimpan dalam file JSON dan dapat diupdate kapan saja via API.

---

## 📋 Table of Contents

1. [Configuration API](#1-configuration-api)
2. [FAQ Content API](#2-faq-content-api)
3. [How-to-Use Content API](#3-how-to-use-content-api)
4. [Theme API](#4-theme-api)
5. [Quick Examples](#5-quick-examples)
6. [Browser Testing](#6-browser-testing)

---

## 1. Configuration API

### GET `/api/cms/config`
Ambil konfigurasi website saat ini (branding, theme, features, platforms)

**Response:**
```json
{
  "success": true,
  "config": {
    "branding": {
      "site_name": "VTmu",
      "site_tagline": "Download Video Cepat & Gratis",
      "site_description": "Platform download video dari berbagai platform sosial media",
      "author": {
        "name": "Andri1404",
        "whatsapp": "6283874636450"
      }
    },
    "theme": {
      "primary_color": "#ff0050",
      "secondary_color": "#00f2ea",
      "dark_bg": "#000000",
      "card_bg": "#1a1a1a",
      "success_color": "#00ff88"
    },
    "features": [...],
    "supported_platforms": [...]
  },
  "timestamp": "2025-01-15T10:30:00"
}
```

### POST `/api/cms/config`
Update konfigurasi website

**Request Body:**
```json
{
  "branding": {
    "site_name": "MyVideoDownloader",
    "site_tagline": "Download Cepat & Mudah"
  },
  "theme": {
    "primary_color": "#0066ff",
    "secondary_color": "#ff6600"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Configuration updated successfully",
  "config": {...},
  "timestamp": "2025-01-15T10:35:00"
}
```

**Curl Example:**
```bash
curl -X POST https://your-site.vercel.app/api/cms/config \
  -H "Content-Type: application/json" \
  -d '{
    "branding": {
      "site_name": "VTmu Pro",
      "author": {
        "name": "Andri1404",
        "whatsapp": "6283874636450"
      }
    }
  }'
```

**JavaScript Example:**
```javascript
fetch('https://your-site.vercel.app/api/cms/config', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    branding: {
      site_name: 'VTmu Pro',
      site_tagline: 'Download Super Cepat'
    },
    theme: {
      primary_color: '#ff0080',
      secondary_color: '#00ffcc'
    }
  })
})
.then(res => res.json())
.then(data => console.log(data))
```

---

## 2. FAQ Content API

### GET `/api/cms/faq`
Ambil semua FAQ items

**Response:**
```json
{
  "success": true,
  "content": {
    "faq_items": [
      {
        "id": 1,
        "category": "general",
        "question": "Apa itu VTmu?",
        "answer": "VTmu adalah platform download video..."
      }
    ],
    "categories": [...]
  },
  "timestamp": "2025-01-15T10:30:00"
}
```

### POST `/api/cms/faq`
Update FAQ content

**Request Body:**
```json
{
  "faq_items": [
    {
      "id": 1,
      "category": "general",
      "question": "Pertanyaan baru?",
      "answer": "Jawaban baru"
    }
  ],
  "categories": [
    {"id": "general", "name": "Umum", "icon": "fa-info-circle"}
  ]
}
```

**Curl Example:**
```bash
curl -X POST https://your-site.vercel.app/api/cms/faq \
  -H "Content-Type: application/json" \
  -d '{
    "faq_items": [
      {
        "id": 14,
        "category": "general",
        "question": "Berapa lama video bisa didownload?",
        "answer": "Video disimpan di server 24 jam, download segera setelah proses selesai"
      }
    ]
  }'
```

---

## 3. How-to-Use Content API

### GET `/api/cms/howto`
Ambil tutorial cara pakai

**Response:**
```json
{
  "success": true,
  "content": {
    "tutorial_steps": [
      {
        "step": 1,
        "title": "Copy Link Video",
        "description": "...",
        "icon": "fa-link",
        "tips": "..."
      }
    ],
    "platform_guides": [...],
    "general_tips": [...]
  },
  "timestamp": "2025-01-15T10:30:00"
}
```

### POST `/api/cms/howto`
Update tutorial content

**Request Body:**
```json
{
  "tutorial_steps": [
    {
      "step": 1,
      "title": "Langkah Pertama",
      "description": "Deskripsi lengkap",
      "icon": "fa-play",
      "tips": "Tips tambahan"
    }
  ],
  "platform_guides": [...],
  "general_tips": ["Tip 1", "Tip 2"]
}
```

**Curl Example:**
```bash
curl -X POST https://your-site.vercel.app/api/cms/howto \
  -H "Content-Type: application/json" \
  -d @howto_content.json
```

---

## 4. Theme API

### POST `/api/cms/theme`
Update theme colors saja (shortcut untuk ganti warna cepat)

**Request Body:**
```json
{
  "theme": {
    "primary_color": "#ff0080",
    "secondary_color": "#00ffcc",
    "success_color": "#00ff66"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Theme updated successfully",
  "theme": {
    "primary_color": "#ff0080",
    "secondary_color": "#00ffcc",
    "dark_bg": "#000000",
    "card_bg": "#1a1a1a",
    "success_color": "#00ff66"
  },
  "timestamp": "2025-01-15T10:40:00"
}
```

**Curl Example:**
```bash
curl -X POST https://your-site.vercel.app/api/cms/theme \
  -H "Content-Type: application/json" \
  -d '{
    "theme": {
      "primary_color": "#0099ff",
      "secondary_color": "#ff6600"
    }
  }'
```

---

## 5. Quick Examples

### Example 1: Ganti Nama Website & Author

```bash
curl -X POST https://your-site.vercel.app/api/cms/config \
  -H "Content-Type: application/json" \
  -d '{
    "branding": {
      "site_name": "VideoMax",
      "site_tagline": "Download Semua Video Gratis",
      "author": {
        "name": "YourName",
        "whatsapp": "628123456789"
      }
    }
  }'
```

### Example 2: Update Warna Theme

```bash
curl -X POST https://your-site.vercel.app/api/cms/theme \
  -H "Content-Type: application/json" \
  -d '{
    "theme": {
      "primary_color": "#9C27B0",
      "secondary_color": "#FF9800"
    }
  }'
```

### Example 3: Tambah FAQ Baru

```bash
curl -X GET https://your-site.vercel.app/api/cms/faq > current_faq.json

# Edit current_faq.json, tambah item baru

curl -X POST https://your-site.vercel.app/api/cms/faq \
  -H "Content-Type: application/json" \
  -d @current_faq.json
```

### Example 4: Lihat Konfigurasi Saat Ini

```bash
# GET config
curl https://your-site.vercel.app/api/cms/config | jq

# GET FAQ
curl https://your-site.vercel.app/api/cms/faq | jq

# GET How-to
curl https://your-site.vercel.app/api/cms/howto | jq
```

---

## 6. Browser Testing

### Method 1: Browser Console

Buka browser, tekan F12, masuk ke Console, paste kode berikut:

**Get Current Config:**
```javascript
fetch('https://your-site.vercel.app/api/cms/config')
  .then(res => res.json())
  .then(data => console.log(data))
```

**Update Website Name:**
```javascript
fetch('https://your-site.vercel.app/api/cms/config', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    branding: {
      site_name: 'MyVideoSite',
      site_tagline: 'Download Cepat & Mudah'
    }
  })
})
.then(res => res.json())
.then(data => {
  console.log('✅ Success:', data);
  alert('Website updated! Refresh halaman untuk lihat perubahan.');
})
.catch(err => console.error('❌ Error:', err))
```

**Update Theme Colors:**
```javascript
fetch('https://your-site.vercel.app/api/cms/theme', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    theme: {
      primary_color: '#e91e63',
      secondary_color: '#00bcd4',
      success_color: '#4caf50'
    }
  })
})
.then(res => res.json())
.then(data => {
  console.log('✅ Theme Updated:', data);
  alert('Theme colors updated!');
})
```

### Method 2: Online API Tester

Gunakan tools seperti:
- [Hoppscotch](https://hoppscotch.io/)
- [Postman](https://www.postman.com/)
- [Insomnia](https://insomnia.rest/)

**Steps:**
1. Buka Hoppscotch/Postman
2. Set method ke POST
3. URL: `https://your-site.vercel.app/api/cms/config`
4. Headers: `Content-Type: application/json`
5. Body (raw JSON):
```json
{
  "branding": {
    "site_name": "NewName"
  }
}
```
6. Click Send

---

## 🎯 Use Cases

### 1. Rebranding Complete Website
```javascript
// Update semua branding sekaligus
fetch('/api/cms/config', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    branding: {
      site_name: 'VidDown Pro',
      site_tagline: 'Professional Video Downloader',
      site_description: 'Download videos from 20+ platforms',
      author: {
        name: 'YourCompany',
        whatsapp: '628123456789'
      }
    },
    theme: {
      primary_color: '#1976d2',
      secondary_color: '#ffc107',
      success_color: '#4caf50'
    }
  })
})
```

### 2. Update FAQ Saat Ada Pertanyaan Baru
```bash
# Download FAQ saat ini
curl https://your-site.vercel.app/api/cms/faq > faq.json

# Edit faq.json, tambah item baru
# Upload kembali
curl -X POST https://your-site.vercel.app/api/cms/faq \
  -H "Content-Type: application/json" \
  -d @faq.json
```

### 3. A/B Testing Theme Colors
```javascript
// Test theme A (warm)
fetch('/api/cms/theme', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    theme: {
      primary_color: '#ff5722',
      secondary_color: '#ff9800'
    }
  })
})

// Kemudian test theme B (cool)
// primary_color: '#2196f3', secondary_color: '#00bcd4'
```

---

## 🔒 Security Notes

1. **CORS Enabled**: API dapat diakses dari browser manapun
2. **No Authentication**: Saat ini tanpa auth (untuk kemudahan development)
3. **Production Recommendation**:
   - Tambahkan API Key authentication
   - Rate limiting sudah ada (flask-limiter)
   - Whitelist IP untuk API endpoint
   - Backup config files secara berkala

### Adding API Key Protection (Optional)

Jika ingin protect API dengan API key:

```python
# Di app.py, tambahkan decorator
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key != os.getenv('CMS_API_KEY'):
            return jsonify({'error': 'Invalid API key'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Gunakan di endpoint
@app.route('/api/cms/config', methods=['POST'])
@require_api_key
def update_website_config():
    # ... existing code
```

Kemudian gunakan dengan header:
```bash
curl -X POST https://your-site.vercel.app/api/cms/config \
  -H "X-API-Key: your-secret-key-here" \
  -H "Content-Type: application/json" \
  -d '{"branding": {...}}'
```

---

## 📝 Data Structure Reference

### Website Config Structure
```json
{
  "branding": {
    "site_name": "string",
    "site_tagline": "string",
    "site_description": "string",
    "author": {
      "name": "string",
      "whatsapp": "string (phone number)"
    }
  },
  "theme": {
    "primary_color": "string (hex color)",
    "secondary_color": "string (hex color)",
    "dark_bg": "string (hex color)",
    "card_bg": "string (hex color)",
    "success_color": "string (hex color)"
  },
  "features": [
    {
      "icon": "string (Font Awesome class)",
      "title": "string",
      "description": "string"
    }
  ],
  "supported_platforms": [
    {
      "name": "string",
      "icon": "string (Font Awesome class)",
      "color": "string (hex or 'gradient')"
    }
  ],
  "version": "string"
}
```

### FAQ Content Structure
```json
{
  "faq_items": [
    {
      "id": "number",
      "category": "string",
      "question": "string",
      "answer": "string"
    }
  ],
  "categories": [
    {
      "id": "string",
      "name": "string",
      "icon": "string (Font Awesome class)"
    }
  ]
}
```

### How-to Content Structure
```json
{
  "tutorial_steps": [
    {
      "step": "number",
      "title": "string",
      "description": "string",
      "icon": "string (Font Awesome class)",
      "tips": "string"
    }
  ],
  "platform_guides": [
    {
      "platform": "string",
      "icon": "string",
      "color": "string",
      "instructions": ["array of strings"],
      "tips": "string"
    }
  ],
  "general_tips": ["array of strings"]
}
```

---

## 🚀 Deployment Notes

File konfigurasi akan dibuat otomatis di folder `config/`:
- `config/website_config.json`
- `config/faq_content.json`
- `config/howto_content.json`

**IMPORTANT**:
- Config folder **SUDAH** ada dan berisi default configuration
- File-file ini **AKAN** di-commit ke git (agar deploy pertama kali sudah ada config)
- Untuk production, bisa exclude `config/` di .gitignore jika ingin (sudah disiapkan)

---

## 📞 Support

Untuk pertanyaan atau bantuan:
- WhatsApp: wa.me/6283874636450 (Andri1404)
- GitHub Issues: [Create issue](https://github.com)

---

**Happy Managing! 🎉**

Sekarang website VTmu bisa dikelola 100% via API tanpa perlu edit code sama sekali!
