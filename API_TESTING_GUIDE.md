# 🧪 API Testing Guide - Postman & Hoppscotch

## Panduan Lengkap Testing Semua API VTmu

---

## 📦 Import Collection

### Method 1: Postman

1. **Download & Install Postman**
   - Download dari [postman.com](https://www.postman.com/downloads/)
   - Atau gunakan web version di [web.postman.co](https://web.postman.co)

2. **Import Collection**
   - Buka Postman
   - Click **Import** (top left)
   - Drag & drop file `VTmu_API_Collection.postman.json`
   - Atau click **Upload Files** → pilih file
   - Click **Import**

3. **Set Environment Variable**
   - Click **Environments** (left sidebar)
   - Click **+** untuk create new environment
   - Name: `VTmu Production`
   - Add variable:
     ```
     Variable: base_url
     Initial Value: https://your-site.vercel.app
     Current Value: https://your-site.vercel.app
     ```
   - Click **Save**
   - Select environment dari dropdown (top right)

4. **Test API**
   - Click collection **VTmu API Collection**
   - Pilih endpoint (e.g., "Health Check")
   - Click **Send**
   - Lihat response di bawah

---

### Method 2: Hoppscotch (Recommended - No Install)

1. **Open Hoppscotch**
   - Buka [hoppscotch.io](https://hoppscotch.io)
   - Tidak perlu install atau sign up

2. **Import Collection**
   - Click **Import/Export** (top menu)
   - Click **Import**
   - Paste content dari `VTmu_API_Collection.postman.json`
   - Atau drag & drop file
   - Click **Import**

3. **Set Environment**
   - Click **Environments** (top menu)
   - Click **Add**
   - Name: `Production`
   - Add variable:
     ```
     Key: base_url
     Value: https://your-site.vercel.app
     ```
   - Click **Save**
   - Select environment

4. **Test API**
   - Click collection pada sidebar kiri
   - Pilih endpoint
   - Click **Send**
   - Lihat response

---

## 🧪 Testing Each API

### 1. Video Download APIs

#### Test 1: Get Video Info (TikTok)

**Endpoint:** POST `/api/get-info`

**Request Body:**
```json
{
  "url": "https://www.tiktok.com/@username/video/7234567890123456789"
}
```

**Expected Response:**
```json
{
  "title": "Video Title",
  "thumbnail": "https://...",
  "duration": 15,
  "uploader": "username",
  "view_count": 1000000,
  "platform": "TikTok",
  "formats": [...]
}
```

**What to Check:**
- ✅ Status: 200 OK
- ✅ Response has `title`, `thumbnail`, `formats`
- ✅ `formats` array has items
- ✅ Response time < 5 seconds

**Common Errors:**
- 400: Invalid URL → Check URL format
- 404: Video not found → Try different URL
- 500: Server error → Check logs

---

#### Test 2: Get Video Info (YouTube)

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

**Expected Response:**
Similar to TikTok, but platform = "YouTube"

---

#### Test 3: Download Video

**Endpoint:** POST `/api/download`

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "quality": "Best Quality",
  "format_id": "bv*+ba/b"
}
```

**Expected Response:**
```json
{
  "success": true,
  "filename": "abc12345.mp4",
  "download_url": "/download/abc12345.mp4",
  "filesize": 5242880
}
```

**What to Check:**
- ✅ Status: 200 OK
- ✅ `success` = true
- ✅ `download_url` exists
- ✅ `filesize` > 0

**Follow-up Test:**
```
GET {{base_url}}/download/abc12345.mp4
```
Should download the file.

---

### 2. Maintenance APIs

#### Test 4: Health Check

**Endpoint:** GET `/api/health`

**Expected Response:**
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

**What to Check:**
- ✅ Status: 200 OK
- ✅ `status` = "healthy"
- ✅ All version fields exist
- ✅ Response time < 1 second

**Red Flags:**
- ❌ Status: 500 → Site unhealthy
- ❌ Response time > 5s → Performance issue
- ❌ `download_folder_size_mb` > 1000 → Need cleanup

---

#### Test 5: View Logs

**Endpoint:** GET `/api/logs`

**Expected Response:**
```json
{
  "logs": [
    "2025-01-15 10:30:00 - app - INFO - ...\n"
  ],
  "total_lines": 1500,
  "showing": 100,
  "timestamp": "2025-01-15T10:30:00"
}
```

**What to Check:**
- ✅ `logs` array not empty
- ✅ `showing` <= 100
- ✅ Logs have timestamps

**Analysis:**
Count errors:
```bash
# In Postman Tests tab
pm.test("Error count acceptable", function() {
    var logs = pm.response.json().logs;
    var errors = logs.filter(l => l.includes('ERROR'));
    pm.expect(errors.length).to.be.below(10);
});
```

---

#### Test 6: Update yt-dlp

**Endpoint:** POST `/api/update-ytdlp`

**Expected Response:**
```json
{
  "success": true,
  "message": "yt-dlp updated successfully",
  "old_version": "2025.09.26",
  "new_version": "2025.10.15",
  "timestamp": "2025-01-15T10:35:00"
}
```

**What to Check:**
- ✅ `success` = true
- ✅ `new_version` >= `old_version`
- ✅ Response time < 60 seconds

**Note:** This endpoint is slow (30-60s), increase timeout!

**Postman Settings:**
- Settings → Request timeout → Set to 120000ms (2 min)

---

#### Test 7: Cleanup Downloads

**Endpoint:** POST `/api/cleanup-downloads`

**Expected Response:**
```json
{
  "success": true,
  "message": "Cleanup successful",
  "files_deleted": 25,
  "space_freed_mb": 450.75,
  "timestamp": "2025-01-15T10:40:00"
}
```

**What to Check:**
- ✅ `success` = true
- ✅ `files_deleted` >= 0
- ✅ `space_freed_mb` >= 0

---

### 3. CMS APIs

#### Test 8: Get Website Config

**Endpoint:** GET `/api/cms/config`

**Expected Response:**
```json
{
  "success": true,
  "config": {
    "branding": {...},
    "theme": {...},
    "features": [...],
    "supported_platforms": [...]
  },
  "timestamp": "2025-01-15T10:45:00"
}
```

**What to Check:**
- ✅ `config.branding` has `site_name`, `author`
- ✅ `config.theme` has color fields
- ✅ `config.features` is array

---

#### Test 9: Update Website Config

**Endpoint:** POST `/api/cms/config`

**Request Body:**
```json
{
  "branding": {
    "site_name": "Test Site",
    "site_tagline": "Testing CMS API"
  }
}
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Configuration updated successfully",
  "config": {...},
  "timestamp": "2025-01-15T10:50:00"
}
```

**Verification:**
After update, call GET `/api/cms/config` again and verify:
- ✅ `site_name` = "Test Site"
- ✅ `site_tagline` = "Testing CMS API"

**Rollback:**
```json
{
  "branding": {
    "site_name": "VTmu",
    "site_tagline": "Download Video Cepat & Gratis"
  }
}
```

---

#### Test 10: Update Theme

**Endpoint:** POST `/api/cms/theme`

**Request Body:**
```json
{
  "theme": {
    "primary_color": "#FF5722",
    "secondary_color": "#FFC107"
  }
}
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Theme updated successfully",
  "theme": {
    "primary_color": "#FF5722",
    "secondary_color": "#FFC107",
    "dark_bg": "#000000",
    "card_bg": "#1a1a1a",
    "success_color": "#00ff88"
  },
  "timestamp": "2025-01-15T10:55:00"
}
```

**Visual Verification:**
- Open website in browser
- Check if colors changed
- Refresh page (Ctrl+Shift+R)

---

## 🔄 Complete Test Workflow

### Workflow 1: Video Download Flow

**Step 1:** Health Check
```
GET /api/health
Expected: status = "healthy"
```

**Step 2:** Get Video Info
```
POST /api/get-info
Body: {"url": "https://youtube.com/..."}
Expected: formats array
```

**Step 3:** Download Video
```
POST /api/download
Body: {
  "url": "...",
  "quality": "Best Quality",
  "format_id": "bv*+ba/b"
}
Expected: success = true, download_url exists
```

**Step 4:** Download File
```
GET /download/<filename>
Expected: File downloads
```

---

### Workflow 2: Maintenance Flow

**Step 1:** Check Health
```
GET /api/health
```

**Step 2:** Check Storage
```
If download_folder_size_mb > 500:
  POST /api/cleanup-downloads
```

**Step 3:** Update yt-dlp
```
POST /api/update-ytdlp
```

**Step 4:** Verify Logs
```
GET /api/logs
Check for errors
```

---

### Workflow 3: CMS Update Flow

**Step 1:** Backup Current Config
```
GET /api/cms/config
Save response
```

**Step 2:** Update Theme
```
POST /api/cms/theme
Body: {"theme": {...}}
```

**Step 3:** Update Branding
```
POST /api/cms/config
Body: {"branding": {...}}
```

**Step 4:** Verify Changes
```
GET /api/cms/config
Compare with backup
```

**Step 5:** Test Website
```
Open in browser
Verify visual changes
```

---

## 🧪 Postman Test Scripts

### Auto Tests for Health Check

Tambahkan di **Tests** tab:

```javascript
// Test status code
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// Test response time
pm.test("Response time < 1000ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(1000);
});

// Test health status
pm.test("Site is healthy", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.status).to.eql("healthy");
});

// Test version exists
pm.test("Versions exist", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.version.app).to.exist;
    pm.expect(jsonData.version.ytdlp).to.exist;
});

// Warning on high storage
pm.test("Storage check", function () {
    var jsonData = pm.response.json();
    var storage = jsonData.system.download_folder_size_mb;

    if (storage > 500) {
        console.warn("⚠️ High storage usage:", storage, "MB");
    }

    pm.expect(storage).to.be.below(1000);
});
```

---

### Auto Tests for Download

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Download successful", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.success).to.be.true;
    pm.expect(jsonData.filename).to.exist;
    pm.expect(jsonData.download_url).to.exist;
});

pm.test("File size valid", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.filesize).to.be.above(0);
});

// Save filename for next request
pm.environment.set("last_filename", pm.response.json().filename);
```

---

### Chain Requests

**Request 1: Get Info**
```javascript
// In Tests tab
pm.test("Get video info success", function() {
    var info = pm.response.json();
    pm.expect(info.formats).to.be.an('array');

    // Save format_id for next request
    pm.environment.set("format_id", info.formats[0].format_id);
    pm.environment.set("video_url", pm.request.body.raw.url);
});
```

**Request 2: Download**
Use variables:
```json
{
  "url": "{{video_url}}",
  "quality": "Best Quality",
  "format_id": "{{format_id}}"
}
```

---

## 🎯 Testing Checklist

### Before Deploy

- [ ] Health check returns 200
- [ ] All video platforms work (TikTok, YouTube, Instagram)
- [ ] Download completes successfully
- [ ] CMS APIs work
- [ ] Theme update reflects on website
- [ ] Logs are readable
- [ ] Update yt-dlp works

### After Deploy

- [ ] Health check on production URL
- [ ] Test download from each platform
- [ ] Verify environment variables
- [ ] Check CORS headers
- [ ] Test custom domain (if any)
- [ ] Monitor logs for errors
- [ ] Performance test (response times)

### Weekly

- [ ] Run health check
- [ ] Check storage usage
- [ ] Review error logs
- [ ] Update yt-dlp if needed
- [ ] Cleanup downloads
- [ ] Backup configuration

---

## 📊 Performance Benchmarks

**Expected Response Times:**

| Endpoint | Expected | Max Acceptable |
|----------|----------|----------------|
| GET /api/health | < 500ms | 1s |
| GET /api/logs | < 1s | 2s |
| POST /api/get-info | < 5s | 10s |
| POST /api/download | < 30s | 60s |
| POST /api/update-ytdlp | < 45s | 120s |
| GET /api/cms/config | < 500ms | 1s |
| POST /api/cms/config | < 1s | 2s |

**Red Flags:**
- ⚠️ Health check > 2s → Server overloaded
- ⚠️ Download > 120s → Timeout likely
- ⚠️ Any GET > 5s → Performance issue

---

## 🔍 Debugging Failed Tests

### Error 400 (Bad Request)

**Check:**
- Request body format (valid JSON?)
- Required fields present?
- URL format valid?

**Fix:**
```json
// Bad
{"url": "tiktok.com/video"}

// Good
{"url": "https://www.tiktok.com/@user/video/123"}
```

---

### Error 404 (Not Found)

**Check:**
- Endpoint URL correct?
- Base URL variable set?
- Filename exists (for /download)?

---

### Error 500 (Server Error)

**Check:**
- View logs: GET /api/logs
- Check health: GET /api/health
- Recent changes?

**Quick Fix:**
```bash
# Update yt-dlp
POST /api/update-ytdlp

# Cleanup
POST /api/cleanup-downloads
```

---

### Timeout

**Check:**
- Network connection stable?
- Server responding?
- Timeout setting in Postman/Hoppscotch

**Increase Timeout:**
- Postman: Settings → Request timeout → 120000ms
- Hoppscotch: Settings → Timeout → 120s

---

## 📱 Mobile Testing

### Hoppscotch Mobile

1. Open hoppscotch.io on mobile browser
2. Import collection (copy-paste JSON)
3. Test APIs
4. Works on iOS & Android

### Postman Mobile

1. Install Postman app (iOS/Android)
2. Sign in to sync collections
3. Test APIs on mobile

---

## ✅ Summary

**Files Created:**
- ✅ `VTmu_API_Collection.postman.json` - API collection
- ✅ `API_TESTING_GUIDE.md` - This guide

**How to Use:**
1. Import collection ke Postman/Hoppscotch
2. Set base_url variable
3. Test each endpoint
4. Run test scripts
5. Monitor results

**Quick Start:**
```bash
# Download collection
curl -O https://your-repo/VTmu_API_Collection.postman.json

# Or use online
# Open hoppscotch.io
# Import collection
# Set base_url
# Start testing!
```

---

**Happy Testing! 🧪**

Semua 15 API siap ditest dengan collection yang lengkap!
