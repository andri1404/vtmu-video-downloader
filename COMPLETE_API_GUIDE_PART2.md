# 🚀 Complete API Guide Part 2 - Practical Examples & Scripts

## API 11-15 dan Complete Workflows

---

## 11. Get FAQ Content

**Endpoint:** `GET /api/cms/faq`

**Request:**
```bash
curl https://your-site.vercel.app/api/cms/faq
```

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
    "categories": [
      {
        "id": "general",
        "name": "Umum",
        "icon": "fa-info-circle"
      }
    ]
  },
  "timestamp": "2025-01-15T11:00:00"
}
```

---

## 12. Update FAQ Content

**Endpoint:** `POST /api/cms/faq`

**Example: Add New FAQ**
```bash
# 1. Download current FAQ
curl https://your-site.vercel.app/api/cms/faq > faq.json

# 2. Edit faq.json (add new item)
# 3. Upload
curl -X POST https://your-site.vercel.app/api/cms/faq \
  -H "Content-Type: application/json" \
  -d @faq.json
```

**JavaScript Example:**
```javascript
async function addFAQ(question, answer, category = 'general') {
  // Get current FAQ
  const response = await fetch('/api/cms/faq');
  const data = await response.json();

  // Add new item
  const newId = Math.max(...data.content.faq_items.map(f => f.id)) + 1;
  data.content.faq_items.push({
    id: newId,
    category,
    question,
    answer
  });

  // Update
  const updateResponse = await fetch('/api/cms/faq', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data.content)
  });

  return await updateResponse.json();
}

// Usage
addFAQ(
  'Berapa lama video disimpan?',
  'Video disimpan 24 jam di server, download segera.',
  'technical'
).then(result => console.log('FAQ added!', result));
```

---

## 13. Get How-to Content

**Endpoint:** `GET /api/cms/howto`

**Request:**
```bash
curl https://your-site.vercel.app/api/cms/howto
```

**Response:**
```json
{
  "success": true,
  "content": {
    "tutorial_steps": [
      {
        "step": 1,
        "title": "Copy Link Video",
        "description": "Buka aplikasi...",
        "icon": "fa-link",
        "tips": "Pastikan link valid"
      }
    ],
    "platform_guides": [...],
    "general_tips": [...]
  },
  "timestamp": "2025-01-15T11:05:00"
}
```

---

## 14. Update How-to Content

**Endpoint:** `POST /api/cms/howto`

**Example: Update Tutorial Steps**
```bash
curl -X POST https://your-site.vercel.app/api/cms/howto \
  -H "Content-Type: application/json" \
  -d '{
    "tutorial_steps": [
      {
        "step": 1,
        "title": "Langkah 1",
        "description": "Deskripsi baru",
        "icon": "fa-play",
        "tips": "Tips baru"
      }
    ],
    "platform_guides": [...],
    "general_tips": ["Tip 1", "Tip 2"]
  }'
```

---

## 15. Update Theme

**Endpoint:** `POST /api/cms/theme`

**Quick Update Theme Colors:**
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

**Popular Theme Presets:**
```bash
# Purple & Orange
curl -X POST /api/cms/theme -d '{"theme":{"primary_color":"#9C27B0","secondary_color":"#FF9800"}}'

# Blue & Yellow
curl -X POST /api/cms/theme -d '{"theme":{"primary_color":"#2196F3","secondary_color":"#FFC107"}}'

# Pink & Cyan
curl -X POST /api/cms/theme -d '{"theme":{"primary_color":"#E91E63","secondary_color":"#00E5FF"}}'

# Green & Teal
curl -X POST /api/cms/theme -d '{"theme":{"primary_color":"#4CAF50","secondary_color":"#00BCD4"}}'
```

---

# 16. Complete Workflows

## Workflow 1: Download Video (Full Process)

```javascript
/**
 * Complete video download workflow
 */
async function completeDownloadWorkflow(videoUrl) {
  console.log('🎬 Starting download workflow...');

  try {
    // Step 1: Validate URL
    if (!videoUrl.startsWith('http')) {
      throw new Error('Invalid URL');
    }

    console.log('✓ URL validated');

    // Step 2: Get video info
    console.log('📊 Fetching video info...');
    const infoResponse = await fetch('/api/get-info', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: videoUrl })
    });

    if (!infoResponse.ok) {
      const error = await infoResponse.json();
      throw new Error(error.error);
    }

    const info = await infoResponse.json();
    console.log('✓ Video info retrieved');
    console.log('  Title:', info.title);
    console.log('  Duration:', info.duration, 'seconds');
    console.log('  Platform:', info.platform);

    // Step 3: Select quality
    const quality = 'Best Quality';
    const format = info.formats.find(f => f.quality === quality);

    if (!format) {
      throw new Error('Quality not available');
    }

    console.log('✓ Quality selected:', quality);

    // Step 4: Download
    console.log('⬇️ Starting download...');
    const downloadResponse = await fetch('/api/download', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        url: videoUrl,
        quality,
        format_id: format.format_id
      })
    });

    if (!downloadResponse.ok) {
      const error = await downloadResponse.json();
      throw new Error(error.error);
    }

    const result = await downloadResponse.json();

    if (!result.success) {
      throw new Error(result.error || 'Download failed');
    }

    console.log('✓ Download successful');
    console.log('  Filename:', result.filename);
    console.log('  Size:', (result.filesize / 1024 / 1024).toFixed(2), 'MB');

    // Step 5: Trigger browser download
    window.location.href = result.download_url;

    console.log('✅ Workflow complete!');
    return result;

  } catch (error) {
    console.error('❌ Workflow failed:', error.message);

    // Log error to server
    await fetch('/api/logs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        level: 'ERROR',
        message: `Download failed: ${error.message}`,
        url: videoUrl
      })
    });

    throw error;
  }
}

// Usage
completeDownloadWorkflow('https://www.youtube.com/watch?v=dQw4w9WgXcQ');
```

---

## Workflow 2: Weekly Maintenance (Bash Script)

```bash
#!/bin/bash
# weekly_maintenance.sh - Run every Monday

SITE="https://your-site.vercel.app"
LOG_FILE="maintenance_$(date +%Y%m%d).log"

echo "🔧 Starting weekly maintenance..." | tee -a $LOG_FILE
echo "Site: $SITE" | tee -a $LOG_FILE
echo "Date: $(date)" | tee -a $LOG_FILE
echo "" | tee -a $LOG_FILE

# 1. Health Check
echo "1️⃣ Health Check..." | tee -a $LOG_FILE
HEALTH=$(curl -s "$SITE/api/health")
STATUS=$(echo $HEALTH | jq -r '.status')

if [ "$STATUS" == "healthy" ]; then
  echo "✅ Site is healthy" | tee -a $LOG_FILE
  echo $HEALTH | jq | tee -a $LOG_FILE
else
  echo "❌ Site is unhealthy!" | tee -a $LOG_FILE
  echo $HEALTH | jq | tee -a $LOG_FILE
  exit 1
fi

echo "" | tee -a $LOG_FILE

# 2. Update yt-dlp
echo "2️⃣ Updating yt-dlp..." | tee -a $LOG_FILE
UPDATE=$(curl -s -X POST "$SITE/api/update-ytdlp")
UPDATE_SUCCESS=$(echo $UPDATE | jq -r '.success')

if [ "$UPDATE_SUCCESS" == "true" ]; then
  OLD=$(echo $UPDATE | jq -r '.old_version')
  NEW=$(echo $UPDATE | jq -r '.new_version')
  echo "✅ Update successful!" | tee -a $LOG_FILE
  echo "  Old: $OLD" | tee -a $LOG_FILE
  echo "  New: $NEW" | tee -a $LOG_FILE
else
  ERROR=$(echo $UPDATE | jq -r '.error')
  echo "⚠️ Update failed: $ERROR" | tee -a $LOG_FILE
fi

echo "" | tee -a $LOG_FILE

# 3. Cleanup Downloads
echo "3️⃣ Cleaning up downloads..." | tee -a $LOG_FILE
CLEANUP=$(curl -s -X POST "$SITE/api/cleanup-downloads")
CLEANUP_SUCCESS=$(echo $CLEANUP | jq -r '.success')

if [ "$CLEANUP_SUCCESS" == "true" ]; then
  FILES=$(echo $CLEANUP | jq -r '.files_deleted')
  SPACE=$(echo $CLEANUP | jq -r '.space_freed_mb')
  echo "✅ Cleanup successful!" | tee -a $LOG_FILE
  echo "  Files deleted: $FILES" | tee -a $LOG_FILE
  echo "  Space freed: ${SPACE}MB" | tee -a $LOG_FILE
else
  ERROR=$(echo $CLEANUP | jq -r '.error')
  echo "⚠️ Cleanup failed: $ERROR" | tee -a $LOG_FILE
fi

echo "" | tee -a $LOG_FILE

# 4. Check Logs for Errors
echo "4️⃣ Checking logs..." | tee -a $LOG_FILE
LOGS=$(curl -s "$SITE/api/logs")
ERROR_COUNT=$(echo $LOGS | jq -r '.logs[]' | grep -c ERROR || echo "0")

echo "Errors in last 100 logs: $ERROR_COUNT" | tee -a $LOG_FILE

if [ "$ERROR_COUNT" -gt "10" ]; then
  echo "⚠️ High error count!" | tee -a $LOG_FILE
  echo $LOGS | jq -r '.logs[]' | grep ERROR | tail -10 | tee -a $LOG_FILE
else
  echo "✅ Error count normal" | tee -a $LOG_FILE
fi

echo "" | tee -a $LOG_FILE

# 5. Summary
echo "✅ Maintenance complete!" | tee -a $LOG_FILE
echo "Log saved to: $LOG_FILE" | tee -a $LOG_FILE

# Send notification (optional)
# curl -X POST https://hooks.slack.com/your-webhook \
#   -d "{\"text\": \"VTmu weekly maintenance complete!\"}"
```

**Setup Cron Job:**
```bash
# Edit crontab
crontab -e

# Add this line (every Monday at 2 AM)
0 2 * * 1 /path/to/weekly_maintenance.sh
```

---

## Workflow 3: Complete Rebranding (Python Script)

```python
#!/usr/bin/env python3
# rebrand.py - Complete website rebranding script

import requests
import json
import sys

SITE_URL = "https://your-site.vercel.app"

def rebrand_website(config):
    """
    Rebrand entire website with new config
    """
    print("🎨 Starting rebranding process...")

    # Update config
    print("\n1️⃣ Updating configuration...")
    response = requests.post(
        f"{SITE_URL}/api/cms/config",
        json=config
    )

    if response.ok:
        result = response.json()
        print("✅ Configuration updated successfully!")
        print(f"  Site Name: {result['config']['branding']['site_name']}")
        print(f"  Theme: {result['config']['theme']['primary_color']}")
    else:
        print(f"❌ Failed: {response.text}")
        sys.exit(1)

    print("\n✅ Rebranding complete!")
    return result

# Example configurations
CONFIGS = {
    "professional": {
        "branding": {
            "site_name": "ProVideoDownloader",
            "site_tagline": "Professional Video Downloading Platform",
            "site_description": "Enterprise-grade video downloader",
            "author": {
                "name": "ProCompany",
                "whatsapp": "628123456789"
            }
        },
        "theme": {
            "primary_color": "#1976D2",
            "secondary_color": "#FFC107",
            "success_color": "#4CAF50"
        },
        "features": [
            {
                "icon": "fa-shield-alt",
                "title": "Enterprise Security",
                "description": "Bank-level encryption"
            },
            {
                "icon": "fa-tachometer-alt",
                "title": "Lightning Fast",
                "description": "1Gbps download speed"
            },
            {
                "icon": "fa-headset",
                "title": "24/7 Support",
                "description": "Always here to help"
            },
            {
                "icon": "fa-globe",
                "title": "Global CDN",
                "description": "Servers worldwide"
            }
        ]
    },

    "fun": {
        "branding": {
            "site_name": "VidNinja 🥷",
            "site_tagline": "Grab Videos Like A Ninja!",
            "site_description": "The coolest video downloader ever",
            "author": {
                "name": "VidNinja Team",
                "whatsapp": "628123456789"
            }
        },
        "theme": {
            "primary_color": "#E91E63",
            "secondary_color": "#00E5FF",
            "success_color": "#76FF03"
        },
        "features": [
            {
                "icon": "fa-rocket",
                "title": "Rocket Speed",
                "description": "Faster than light!"
            },
            {
                "icon": "fa-fire",
                "title": "Hot Features",
                "description": "Blazing fast downloads"
            },
            {
                "icon": "fa-star",
                "title": "5-Star Quality",
                "description": "Best quality always"
            },
            {
                "icon": "fa-heart",
                "title": "Made with Love",
                "description": "We care about you"
            }
        ]
    },

    "minimal": {
        "branding": {
            "site_name": "VidGet",
            "site_tagline": "Simple. Fast. Free.",
            "site_description": "Minimalist video downloader",
            "author": {
                "name": "VidGet",
                "whatsapp": "628123456789"
            }
        },
        "theme": {
            "primary_color": "#212121",
            "secondary_color": "#FFFFFF",
            "success_color": "#00C853"
        },
        "features": [
            {
                "icon": "fa-check",
                "title": "Simple",
                "description": "Easy to use"
            },
            {
                "icon": "fa-bolt",
                "title": "Fast",
                "description": "Lightning quick"
            }
        ]
    }
}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python rebrand.py [professional|fun|minimal]")
        sys.exit(1)

    style = sys.argv[1]

    if style not in CONFIGS:
        print(f"❌ Unknown style: {style}")
        print(f"Available: {', '.join(CONFIGS.keys())}")
        sys.exit(1)

    config = CONFIGS[style]
    rebrand_website(config)
```

**Usage:**
```bash
# Rebrand to professional style
python rebrand.py professional

# Rebrand to fun style
python rebrand.py fun

# Rebrand to minimal style
python rebrand.py minimal
```

---

## Workflow 4: Monitor & Auto-Fix

```bash
#!/bin/bash
# monitor_and_fix.sh - Continuous monitoring with auto-fix

SITE="https://your-site.vercel.app"
CHECK_INTERVAL=300  # 5 minutes

echo "🔍 Starting monitoring (checking every ${CHECK_INTERVAL}s)..."

while true; do
  echo "$(date) - Checking site health..."

  # Health check
  HEALTH=$(curl -s "$SITE/api/health")
  STATUS=$(echo $HEALTH | jq -r '.status')

  if [ "$STATUS" != "healthy" ]; then
    echo "❌ Site unhealthy! Attempting auto-fix..."

    # Try updating yt-dlp
    echo "  Updating yt-dlp..."
    curl -s -X POST "$SITE/api/update-ytdlp"

    # Cleanup
    echo "  Cleaning downloads..."
    curl -s -X POST "$SITE/api/cleanup-downloads"

    # Send alert
    curl -X POST https://hooks.slack.com/your-webhook \
      -d "{\"text\": \"⚠️ VTmu was unhealthy, auto-fix applied\"}"

    echo "  ✅ Auto-fix complete"
  else
    echo "  ✅ Site healthy"

    # Check storage
    STORAGE=$(echo $HEALTH | jq -r '.system.download_folder_size_mb')

    if (( $(echo "$STORAGE > 1000" | bc -l) )); then
      echo "  ⚠️ Storage high (${STORAGE}MB), cleaning..."
      curl -s -X POST "$SITE/api/cleanup-downloads"
    fi
  fi

  echo "  Sleeping ${CHECK_INTERVAL}s..."
  sleep $CHECK_INTERVAL
done
```

**Run in background:**
```bash
# Start monitoring
nohup ./monitor_and_fix.sh > monitor.log 2>&1 &

# Check logs
tail -f monitor.log

# Stop monitoring
pkill -f monitor_and_fix.sh
```

---

# 17. Automation Scripts

## Script 1: Daily Report

```python
#!/usr/bin/env python3
# daily_report.py

import requests
from datetime import datetime
import json

SITE = "https://your-site.vercel.app"

def generate_daily_report():
    print("📊 VTmu Daily Report")
    print("=" * 50)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Health
    health = requests.get(f"{SITE}/api/health").json()
    print("🏥 Health Status")
    print(f"  Status: {health['status']}")
    print(f"  App Version: {health['version']['app']}")
    print(f"  yt-dlp Version: {health['version']['ytdlp']}")
    print(f"  Storage Used: {health['system']['download_folder_size_mb']}MB")
    print(f"  Files: {health['system']['download_folder_files']}")
    print()

    # Logs analysis
    logs = requests.get(f"{SITE}/api/logs").json()
    log_lines = logs['logs']

    error_count = sum(1 for log in log_lines if 'ERROR' in log)
    warning_count = sum(1 for log in log_lines if 'WARNING' in log)
    info_count = sum(1 for log in log_lines if 'INFO' in log)

    print("📋 Logs Summary (last 100 entries)")
    print(f"  Errors: {error_count}")
    print(f"  Warnings: {warning_count}")
    print(f"  Info: {info_count}")
    print()

    if error_count > 0:
        print("❌ Recent Errors:")
        for log in log_lines:
            if 'ERROR' in log:
                print(f"  {log.strip()}")
        print()

    # Config check
    config = requests.get(f"{SITE}/api/cms/config").json()
    print("⚙️ Configuration")
    print(f"  Site Name: {config['config']['branding']['site_name']}")
    print(f"  Theme: {config['config']['theme']['primary_color']}")
    print()

    print("=" * 50)

if __name__ == "__main__":
    generate_daily_report()
```

**Cron Job (Daily at 9 AM):**
```bash
0 9 * * * python /path/to/daily_report.py | mail -s "VTmu Daily Report" your@email.com
```

---

## Script 2: Backup Configuration

```bash
#!/bin/bash
# backup_config.sh

SITE="https://your-site.vercel.app"
BACKUP_DIR="$HOME/vtmu_backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

echo "💾 Backing up VTmu configuration..."

# Backup website config
curl -s "$SITE/api/cms/config" > "$BACKUP_DIR/config_$DATE.json"
echo "✓ Website config backed up"

# Backup FAQ
curl -s "$SITE/api/cms/faq" > "$BACKUP_DIR/faq_$DATE.json"
echo "✓ FAQ backed up"

# Backup How-to
curl -s "$SITE/api/cms/howto" > "$BACKUP_DIR/howto_$DATE.json"
echo "✓ How-to backed up"

# Backup health status
curl -s "$SITE/api/health" > "$BACKUP_DIR/health_$DATE.json"
echo "✓ Health status backed up"

# Create tarball
tar -czf "$BACKUP_DIR/vtmu_backup_$DATE.tar.gz" -C "$BACKUP_DIR" \
  "config_$DATE.json" \
  "faq_$DATE.json" \
  "howto_$DATE.json" \
  "health_$DATE.json"

# Cleanup individual files
rm "$BACKUP_DIR"/*.json

echo "✅ Backup complete: vtmu_backup_$DATE.tar.gz"
echo "Location: $BACKUP_DIR"

# Keep only last 30 backups
ls -t "$BACKUP_DIR"/vtmu_backup_*.tar.gz | tail -n +31 | xargs -r rm

echo "Old backups cleaned up"
```

---

## 18. Error Handling

### Common Errors & Solutions

```javascript
/**
 * Comprehensive error handling for all APIs
 */
class VTmuAPI {
  constructor(baseUrl) {
    this.baseUrl = baseUrl;
  }

  async request(endpoint, options = {}) {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, options);

      // Handle HTTP errors
      if (!response.ok) {
        const error = await response.json();
        throw new VTmuError(error.error || 'Request failed', response.status);
      }

      return await response.json();

    } catch (error) {
      // Network error
      if (error instanceof TypeError) {
        throw new VTmuError('Network error. Check your connection.', 0);
      }

      // Re-throw VTmuError
      if (error instanceof VTmuError) {
        throw error;
      }

      // Unknown error
      throw new VTmuError(error.message, 500);
    }
  }

  // Download video with retry
  async downloadVideo(url, quality = 'Best Quality', maxRetries = 3) {
    let lastError;

    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        console.log(`Attempt ${attempt}/${maxRetries}...`);

        // Get info
        const info = await this.request('/api/get-info', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ url })
        });

        // Find format
        const format = info.formats.find(f => f.quality === quality);
        if (!format) {
          throw new VTmuError('Quality not available', 404);
        }

        // Download
        const result = await this.request('/api/download', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            url,
            quality,
            format_id: format.format_id
          })
        });

        return result;

      } catch (error) {
        lastError = error;

        // Don't retry on client errors (4xx)
        if (error.code >= 400 && error.code < 500) {
          throw error;
        }

        // Wait before retry (exponential backoff)
        if (attempt < maxRetries) {
          const delay = Math.pow(2, attempt) * 1000;
          console.log(`Retrying in ${delay}ms...`);
          await new Promise(resolve => setTimeout(resolve, delay));
        }
      }
    }

    throw new VTmuError(
      `Failed after ${maxRetries} attempts: ${lastError.message}`,
      lastError.code
    );
  }

  // Update yt-dlp with timeout
  async updateYtdlp(timeout = 120000) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    try {
      const result = await this.request('/api/update-ytdlp', {
        method: 'POST',
        signal: controller.signal
      });

      clearTimeout(timeoutId);
      return result;

    } catch (error) {
      clearTimeout(timeoutId);

      if (error.name === 'AbortError') {
        throw new VTmuError('Update timeout', 408);
      }

      throw error;
    }
  }
}

class VTmuError extends Error {
  constructor(message, code) {
    super(message);
    this.name = 'VTmuError';
    this.code = code;
  }
}

// Usage
const api = new VTmuAPI('https://your-site.vercel.app');

api.downloadVideo('https://youtube.com/watch?v=...', 'HD 720p')
  .then(result => {
    console.log('✅ Success:', result);
    window.location.href = result.download_url;
  })
  .catch(error => {
    if (error instanceof VTmuError) {
      switch (error.code) {
        case 400:
          alert('Invalid URL or request');
          break;
        case 404:
          alert('Video not found or unavailable');
          break;
        case 408:
          alert('Request timeout. Try again.');
          break;
        case 500:
          alert('Server error. Please try again later.');
          break;
        default:
          alert(`Error: ${error.message}`);
      }
    } else {
      alert('Unknown error occurred');
    }
    console.error(error);
  });
```

---

**✅ SELESAI! Panduan Lengkap Semua API VTmu**

Semua 15 API sudah dijelaskan dengan:
- ✅ Request/Response examples
- ✅ JavaScript & Bash examples
- ✅ Complete workflows
- ✅ Automation scripts
- ✅ Error handling
- ✅ Production-ready code

Lihat juga:
- CMS_API_DOCS.md - CMS API details
- API_DOCS.md - Maintenance API details
- COMPLETE_API_GUIDE.md (Part 1) - Download APIs

