# 📘 Complete API Usage Guide - VTmu

## 🎯 Panduan Lengkap Menggunakan Semua Fitur API

Dokumen ini menjelaskan **SEMUA API** yang tersedia di VTmu dan cara menggunakannya step-by-step.

---

## 📋 Daftar Isi

### Part 1: Video Download APIs
1. [Get Video Info](#1-get-video-info)
2. [Download Video](#2-download-video)
3. [Download File](#3-download-file)
4. [Supported Sites](#4-supported-sites)

### Part 2: Maintenance APIs
5. [Health Check](#5-health-check)
6. [View Logs](#6-view-logs)
7. [Update yt-dlp](#7-update-yt-dlp)
8. [Cleanup Downloads](#8-cleanup-downloads)

### Part 3: CMS APIs
9. [Get Website Config](#9-get-website-config)
10. [Update Website Config](#10-update-website-config)
11. [Get FAQ Content](#11-get-faq-content)
12. [Update FAQ Content](#12-update-faq-content)
13. [Get How-to Content](#13-get-how-to-content)
14. [Update How-to Content](#14-update-how-to-content)
15. [Update Theme](#15-update-theme)

### Part 4: Practical Examples
16. [Complete Workflows](#16-complete-workflows)
17. [Automation Scripts](#17-automation-scripts)
18. [Error Handling](#18-error-handling)

---

# PART 1: VIDEO DOWNLOAD APIs

## 1. Get Video Info

**Endpoint:** `POST /api/get-info`

**Deskripsi:** Ambil informasi video (title, thumbnail, formats) tanpa download

**Request:**
```bash
curl -X POST https://your-site.vercel.app/api/get-info \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.tiktok.com/@username/video/1234567890"
  }'
```

**Response Success:**
```json
{
  "title": "Video Title Here",
  "thumbnail": "https://...",
  "duration": 15,
  "uploader": "Username",
  "view_count": 1000000,
  "platform": "TikTok",
  "formats": [
    {
      "quality": "Best Quality",
      "ext": "mp4",
      "filesize": 0,
      "format_id": "bv*+ba/b",
      "description": "Kualitas terbaik"
    },
    {
      "quality": "HD 720p",
      "ext": "mp4",
      "filesize": 0,
      "format_id": "bv*[height<=720]+ba/b[height<=720]/bv*[height<=720]/b",
      "description": "720p HD"
    },
    {
      "quality": "Audio Only (MP3)",
      "ext": "mp3",
      "filesize": 0,
      "format_id": "bestaudio",
      "description": "MP3 Audio"
    }
  ]
}
```

**Response Error:**
```json
{
  "error": "URL tidak valid atau mengandung karakter berbahaya"
}
```

**JavaScript Example:**
```javascript
async function getVideoInfo(url) {
  const response = await fetch('/api/get-info', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url })
  });

  const data = await response.json();

  if (response.ok) {
    console.log('Title:', data.title);
    console.log('Duration:', data.duration, 'seconds');
    console.log('Formats:', data.formats);
    return data;
  } else {
    console.error('Error:', data.error);
    throw new Error(data.error);
  }
}

// Usage
getVideoInfo('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
  .then(info => console.log(info))
  .catch(err => console.error(err));
```

**Supported Platforms:**
- TikTok (including photos/slideshows)
- YouTube
- Instagram (Reels, IGTV, Posts)
- Facebook
- Twitter/X
- Reddit
- Vimeo
- Dan 10+ platform lainnya

---

## 2. Download Video

**Endpoint:** `POST /api/download`

**Deskripsi:** Download video dengan kualitas yang dipilih

**Request:**
```bash
curl -X POST https://your-site.vercel.app/api/download \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.tiktok.com/@username/video/1234567890",
    "quality": "Best Quality",
    "format_id": "bv*+ba/b"
  }'
```

**Parameters:**
- `url` (required): URL video
- `quality` (optional): "Best Quality", "HD 720p", "SD 480p", "Low 360p", "Audio Only (MP3)"
- `format_id` (optional): Format ID dari get-info response

**Response Success:**
```json
{
  "success": true,
  "filename": "abc12345.mp4",
  "download_url": "/download/abc12345.mp4",
  "filesize": 5242880
}
```

**Response Error:**
```json
{
  "error": "Gagal mendownload: Video privat atau tidak tersedia"
}
```

**Full Example (JavaScript):**
```javascript
async function downloadVideo(url, quality = 'Best Quality') {
  // Step 1: Get video info
  const infoResponse = await fetch('/api/get-info', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url })
  });

  const info = await infoResponse.json();

  if (!infoResponse.ok) {
    throw new Error(info.error);
  }

  // Step 2: Find format
  const format = info.formats.find(f => f.quality === quality);

  if (!format) {
    throw new Error('Quality not found');
  }

  // Step 3: Download
  const downloadResponse = await fetch('/api/download', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      url,
      quality,
      format_id: format.format_id
    })
  });

  const result = await downloadResponse.json();

  if (result.success) {
    // Step 4: Trigger browser download
    window.location.href = result.download_url;
    return result;
  } else {
    throw new Error(result.error);
  }
}

// Usage
downloadVideo('https://www.youtube.com/watch?v=dQw4w9WgXcQ', 'HD 720p')
  .then(result => {
    console.log('✅ Download started!');
    console.log('File:', result.filename);
    console.log('Size:', (result.filesize / 1024 / 1024).toFixed(2), 'MB');
  })
  .catch(err => {
    console.error('❌ Download failed:', err.message);
  });
```

---

## 3. Download File

**Endpoint:** `GET /download/<filename>`

**Deskripsi:** Serve file yang sudah didownload

**Request:**
```bash
curl -O https://your-site.vercel.app/download/abc12345.mp4
```

**Browser:**
```html
<a href="/download/abc12345.mp4" download>Download Video</a>
```

**JavaScript:**
```javascript
// Auto-download
window.location.href = '/download/abc12345.mp4';

// Or fetch and show progress
fetch('/download/abc12345.mp4')
  .then(response => {
    const reader = response.body.getReader();
    const contentLength = +response.headers.get('Content-Length');

    let receivedLength = 0;
    let chunks = [];

    return reader.read().then(function processResult(result) {
      if (result.done) {
        const blob = new Blob(chunks);
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'video.mp4';
        a.click();
        return;
      }

      chunks.push(result.value);
      receivedLength += result.value.length;

      const progress = (receivedLength / contentLength) * 100;
      console.log(`Progress: ${progress.toFixed(2)}%`);

      return reader.read().then(processResult);
    });
  });
```

---

## 4. Supported Sites

**Endpoint:** `GET /api/supported-sites`

**Deskripsi:** Daftar platform yang didukung

**Request:**
```bash
curl https://your-site.vercel.app/api/supported-sites
```

**Response:**
```json
{
  "sites": [
    "YouTube",
    "TikTok",
    "Instagram",
    "Facebook",
    "Twitter/X",
    "Reddit",
    "Vimeo",
    "Dailymotion",
    "Twitch",
    "SoundCloud",
    "Bilibili",
    "VK",
    "LinkedIn",
    "Pinterest",
    "Snapchat"
  ]
}
```

---

# PART 2: MAINTENANCE APIs

## 5. Health Check

**Endpoint:** `GET /api/health`

**Deskripsi:** Check status aplikasi, versions, dan resource usage

**Request:**
```bash
curl https://your-site.vercel.app/api/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-15T10:30:00",
  "version": {
    "app": "1.0.0",
    "python": "3.9.18",
    "ytdlp": "2025.09.26",
    "flask": "3.0.0"
  },
  "system": {
    "download_folder_size_mb": 125.5,
    "download_folder_files": 15
  },
  "uptime": "running"
}
```

**Monitoring Script:**
```bash
#!/bin/bash
# health_check.sh

SITE="https://your-site.vercel.app"

# Check health
RESPONSE=$(curl -s "$SITE/api/health")
STATUS=$(echo $RESPONSE | jq -r '.status')

if [ "$STATUS" == "healthy" ]; then
  echo "✅ Site is healthy"

  # Get details
  APP_VERSION=$(echo $RESPONSE | jq -r '.version.app')
  YTDLP_VERSION=$(echo $RESPONSE | jq -r '.version.ytdlp')
  STORAGE=$(echo $RESPONSE | jq -r '.system.download_folder_size_mb')

  echo "App Version: $APP_VERSION"
  echo "yt-dlp Version: $YTDLP_VERSION"
  echo "Storage Used: ${STORAGE}MB"
else
  echo "❌ Site is unhealthy!"
  echo $RESPONSE | jq

  # Send alert (example with curl to webhook)
  curl -X POST https://hooks.slack.com/your-webhook \
    -d "{\"text\": \"⚠️ VTmu is down!\"}"
fi
```

---

## 6. View Logs

**Endpoint:** `GET /api/logs`

**Deskripsi:** View last 100 log lines

**Request:**
```bash
curl https://your-site.vercel.app/api/logs
```

**Response:**
```json
{
  "logs": [
    "2025-01-15 10:30:00 - app - INFO - Health check successful\n",
    "2025-01-15 10:29:55 - app - INFO - Video downloaded successfully\n",
    "2025-01-15 10:29:50 - app - ERROR - Download failed: Video private\n"
  ],
  "total_lines": 1500,
  "showing": 100,
  "timestamp": "2025-01-15T10:30:00"
}
```

**Search Logs:**
```bash
# Get logs and search for errors
curl https://your-site.vercel.app/api/logs | jq -r '.logs[]' | grep ERROR

# Count errors
curl https://your-site.vercel.app/api/logs | jq -r '.logs[]' | grep -c ERROR

# Get last 10 errors
curl https://your-site.vercel.app/api/logs | jq -r '.logs[]' | grep ERROR | tail -10
```

**JavaScript:**
```javascript
async function viewLogs(searchTerm = '') {
  const response = await fetch('/api/logs');
  const data = await response.json();

  const logs = data.logs;

  if (searchTerm) {
    const filtered = logs.filter(log => log.includes(searchTerm));
    console.log(`Found ${filtered.length} logs matching "${searchTerm}"`);
    filtered.forEach(log => console.log(log));
  } else {
    console.log(`Total logs: ${data.total_lines}`);
    console.log(`Showing: ${data.showing}`);
    logs.forEach(log => console.log(log));
  }
}

// Usage
viewLogs('ERROR');  // Show only errors
viewLogs('TikTok'); // Show TikTok-related logs
```

---

## 7. Update yt-dlp

**Endpoint:** `POST /api/update-ytdlp`

**Deskripsi:** Update yt-dlp ke versi terbaru (fix TikTok/YouTube errors)

**Request:**
```bash
curl -X POST https://your-site.vercel.app/api/update-ytdlp
```

**Response Success:**
```json
{
  "success": true,
  "message": "yt-dlp updated successfully",
  "old_version": "2025.09.26",
  "new_version": "2025.10.15",
  "timestamp": "2025-01-15T10:35:00"
}
```

**Response Error:**
```json
{
  "success": false,
  "error": "Update timeout (exceeded 60 seconds)",
  "timestamp": "2025-01-15T10:35:00"
}
```

**When to Use:**
- ❌ TikTok download fails
- ❌ YouTube "Sign in to confirm" error
- ❌ Instagram "Video unavailable"
- ❌ Any platform-specific errors

**Automated Update:**
```bash
#!/bin/bash
# auto_update_ytdlp.sh

SITE="https://your-site.vercel.app"

echo "🔄 Updating yt-dlp..."

RESPONSE=$(curl -s -X POST "$SITE/api/update-ytdlp")
SUCCESS=$(echo $RESPONSE | jq -r '.success')

if [ "$SUCCESS" == "true" ]; then
  OLD=$(echo $RESPONSE | jq -r '.old_version')
  NEW=$(echo $RESPONSE | jq -r '.new_version')

  echo "✅ Update successful!"
  echo "Old version: $OLD"
  echo "New version: $NEW"
else
  ERROR=$(echo $RESPONSE | jq -r '.error')
  echo "❌ Update failed: $ERROR"
fi
```

**Cron Job (Weekly Update):**
```bash
# Edit crontab
crontab -e

# Add this line (every Monday at 3 AM)
0 3 * * 1 /path/to/auto_update_ytdlp.sh
```

---

## 8. Cleanup Downloads

**Endpoint:** `POST /api/cleanup-downloads`

**Deskripsi:** Hapus semua file di folder downloads (free up storage)

**Request:**
```bash
curl -X POST https://your-site.vercel.app/api/cleanup-downloads
```

**Response:**
```json
{
  "success": true,
  "message": "Cleanup successful",
  "files_deleted": 25,
  "space_freed_mb": 450.75,
  "timestamp": "2025-01-15T10:40:00"
}
```

**When to Use:**
- 💾 Storage hampir penuh
- 🧹 Cleanup rutin (mingguan)
- ⚡ Sebelum deploy baru

**Automated Cleanup:**
```bash
#!/bin/bash
# weekly_cleanup.sh

SITE="https://your-site.vercel.app"

# Check current storage
HEALTH=$(curl -s "$SITE/api/health")
STORAGE=$(echo $HEALTH | jq -r '.system.download_folder_size_mb')

echo "Current storage: ${STORAGE}MB"

# Cleanup if > 500MB
if (( $(echo "$STORAGE > 500" | bc -l) )); then
  echo "🧹 Storage high, cleaning up..."

  RESPONSE=$(curl -s -X POST "$SITE/api/cleanup-downloads")
  FREED=$(echo $RESPONSE | jq -r '.space_freed_mb')

  echo "✅ Cleanup complete!"
  echo "Space freed: ${FREED}MB"
else
  echo "✅ Storage OK, no cleanup needed"
fi
```

**Cron Job (Daily Cleanup):**
```bash
# Every day at 2 AM
0 2 * * * /path/to/weekly_cleanup.sh
```

---

# PART 3: CMS APIs

## 9. Get Website Config

**Endpoint:** `GET /api/cms/config`

**Deskripsi:** Ambil konfigurasi website (branding, theme, features, platforms)

**Request:**
```bash
curl https://your-site.vercel.app/api/cms/config
```

**Response:**
```json
{
  "success": true,
  "config": {
    "branding": {
      "site_name": "VTmu",
      "site_tagline": "Download Video Cepat & Gratis",
      "site_description": "Platform download video...",
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
    "features": [
      {
        "icon": "fa-bolt",
        "title": "Super Cepat",
        "description": "Download dalam hitungan detik"
      }
    ],
    "supported_platforms": [
      {
        "name": "TikTok",
        "icon": "fa-tiktok",
        "color": "#ff0050"
      }
    ],
    "version": "1.0.0"
  },
  "timestamp": "2025-01-15T10:45:00"
}
```

**JavaScript:**
```javascript
async function getConfig() {
  const response = await fetch('/api/cms/config');
  const data = await response.json();

  if (data.success) {
    console.log('Site Name:', data.config.branding.site_name);
    console.log('Theme Colors:', data.config.theme);
    console.log('Features:', data.config.features.length);
    return data.config;
  }
}
```

---

## 10. Update Website Config

**Endpoint:** `POST /api/cms/config`

**Deskripsi:** Update branding, theme, features, platforms

**Request (Update Branding):**
```bash
curl -X POST https://your-site.vercel.app/api/cms/config \
  -H "Content-Type: application/json" \
  -d '{
    "branding": {
      "site_name": "VideoMax Pro",
      "site_tagline": "Download Semua Video Gratis",
      "author": {
        "name": "NewDeveloper",
        "whatsapp": "628123456789"
      }
    }
  }'
```

**Request (Update Theme):**
```bash
curl -X POST https://your-site.vercel.app/api/cms/config \
  -H "Content-Type: application/json" \
  -d '{
    "theme": {
      "primary_color": "#9C27B0",
      "secondary_color": "#FF9800",
      "success_color": "#4CAF50"
    }
  }'
```

**Request (Update Features):**
```bash
curl -X POST https://your-site.vercel.app/api/cms/config \
  -H "Content-Type: application/json" \
  -d '{
    "features": [
      {
        "icon": "fa-rocket",
        "title": "Ultra Fast",
        "description": "Lightning speed downloads"
      },
      {
        "icon": "fa-shield",
        "title": "100% Secure",
        "description": "Your data is safe"
      }
    ]
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Configuration updated successfully",
  "config": { ... },
  "timestamp": "2025-01-15T10:50:00"
}
```

---

(Continuing in next message due to length...)
