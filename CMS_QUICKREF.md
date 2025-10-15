# 📝 CMS Quick Reference - VTmu

## 🚀 One-Line Commands

### View Current Settings
```bash
# View website config
curl https://your-site.vercel.app/api/cms/config | jq

# View FAQ
curl https://your-site.vercel.app/api/cms/faq | jq

# View How-to
curl https://your-site.vercel.app/api/cms/howto | jq
```

### Update Website Name
```bash
curl -X POST https://your-site.vercel.app/api/cms/config \
  -H "Content-Type: application/json" \
  -d '{"branding":{"site_name":"NewName","site_tagline":"New Tagline"}}'
```

### Change Theme Colors
```bash
curl -X POST https://your-site.vercel.app/api/cms/theme \
  -H "Content-Type: application/json" \
  -d '{"theme":{"primary_color":"#ff0080","secondary_color":"#00ffcc"}}'
```

### Update Author Info
```bash
curl -X POST https://your-site.vercel.app/api/cms/config \
  -H "Content-Type: application/json" \
  -d '{"branding":{"author":{"name":"YourName","whatsapp":"628123456789"}}}'
```

---

## 🎨 Popular Theme Combinations

### Red & Blue (Default)
```json
{"theme":{"primary_color":"#ff0050","secondary_color":"#00f2ea"}}
```

### Purple & Orange
```json
{"theme":{"primary_color":"#9C27B0","secondary_color":"#FF9800"}}
```

### Blue & Yellow
```json
{"theme":{"primary_color":"#2196F3","secondary_color":"#FFC107"}}
```

### Green & Teal
```json
{"theme":{"primary_color":"#4CAF50","secondary_color":"#00BCD4"}}
```

### Pink & Cyan
```json
{"theme":{"primary_color":"#E91E63","secondary_color":"#00E5FF"}}
```

---

## 📋 Common Tasks

### Task 1: Complete Rebranding
```bash
curl -X POST https://your-site.vercel.app/api/cms/config \
  -H "Content-Type: application/json" \
  -d '{
    "branding": {
      "site_name": "VidMax Pro",
      "site_tagline": "Download Video Premium",
      "site_description": "Platform terbaik untuk download video",
      "author": {
        "name": "CompanyName",
        "whatsapp": "628123456789"
      }
    },
    "theme": {
      "primary_color": "#1976D2",
      "secondary_color": "#FFC107",
      "success_color": "#4CAF50"
    }
  }'
```

### Task 2: Add New FAQ
```bash
# 1. Download current FAQ
curl https://your-site.vercel.app/api/cms/faq > faq.json

# 2. Edit faq.json, add new item:
# {
#   "id": 14,
#   "category": "general",
#   "question": "New question?",
#   "answer": "New answer"
# }

# 3. Upload updated FAQ
curl -X POST https://your-site.vercel.app/api/cms/faq \
  -H "Content-Type: application/json" \
  -d @faq.json
```

### Task 3: Update Features List
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
        "title": "Secure",
        "description": "100% safe and private"
      },
      {
        "icon": "fa-gift",
        "title": "Free Forever",
        "description": "No hidden charges"
      },
      {
        "icon": "fa-mobile",
        "title": "All Devices",
        "description": "Works everywhere"
      }
    ]
  }'
```

---

## 🌐 Browser Console Commands

Paste di Browser Console (F12 → Console):

### Get Config
```javascript
fetch('/api/cms/config').then(r=>r.json()).then(console.log)
```

### Update Site Name
```javascript
fetch('/api/cms/config',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({branding:{site_name:'NewName'}})}).then(r=>r.json()).then(d=>{console.log(d);alert('Updated!')})
```

### Change Colors
```javascript
fetch('/api/cms/theme',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({theme:{primary_color:'#e91e63',secondary_color:'#00bcd4'}})}).then(r=>r.json()).then(d=>{console.log(d);alert('Theme updated!')})
```

### View All FAQs
```javascript
fetch('/api/cms/faq').then(r=>r.json()).then(d=>console.table(d.content.faq_items))
```

---

## 📊 Data Templates

### FAQ Item Template
```json
{
  "id": 1,
  "category": "general",
  "question": "Your question here?",
  "answer": "Your answer here"
}
```

### Tutorial Step Template
```json
{
  "step": 1,
  "title": "Step Title",
  "description": "Step description",
  "icon": "fa-icon-name",
  "tips": "Helpful tips"
}
```

### Feature Template
```json
{
  "icon": "fa-icon-name",
  "title": "Feature Title",
  "description": "Feature description"
}
```

### Platform Template
```json
{
  "name": "Platform Name",
  "icon": "fa-icon-name",
  "color": "#hexcolor"
}
```

---

## 🔧 Troubleshooting

### Error: Configuration not found
**Solution:** Config files belum ada. Buat manual atau deploy ulang.

### Error: Invalid data structure
**Solution:** Pastikan JSON valid dan mengandung field yang benar:
- FAQ: harus ada `faq_items` (array)
- How-to: harus ada `tutorial_steps` (array)
- Config: object dengan fields yang valid

### Changes Not Showing
**Solution:**
1. Hard refresh browser (Ctrl+Shift+R)
2. Clear cache
3. Check if update was successful (check API response)

### CORS Error
**Solution:** API sudah enable CORS. Jika masih error:
1. Check browser console for exact error
2. Pastikan Content-Type header ada
3. Gunakan curl untuk test

---

## 💡 Pro Tips

1. **Backup Before Update**
   ```bash
   # Backup all configs
   curl https://your-site.vercel.app/api/cms/config > backup_config.json
   curl https://your-site.vercel.app/api/cms/faq > backup_faq.json
   curl https://your-site.vercel.app/api/cms/howto > backup_howto.json
   ```

2. **Test Changes Locally First**
   ```bash
   # Run local server
   python app.py

   # Test on localhost
   curl http://localhost:5000/api/cms/config
   ```

3. **Use jq for Pretty Print**
   ```bash
   curl https://your-site.vercel.app/api/cms/config | jq .
   ```

4. **Automate with Scripts**
   ```bash
   #!/bin/bash
   # update_branding.sh
   curl -X POST https://your-site.vercel.app/api/cms/config \
     -H "Content-Type: application/json" \
     -d @new_config.json

   echo "✅ Branding updated!"
   ```

5. **Schedule Updates with Cron**
   ```bash
   # Update theme every Monday at 9am
   0 9 * * 1 curl -X POST https://your-site.vercel.app/api/cms/theme -d @theme_monday.json
   ```

---

## 📞 Quick Help

**Need help?**
- WhatsApp: wa.me/6283874636450
- Check API_DOCS.md for full documentation
- Check CMS_API_DOCS.md for detailed guides

**Test API:**
- Health: `curl https://your-site.vercel.app/api/health`
- Config: `curl https://your-site.vercel.app/api/cms/config`

---

**Last Updated:** 2025-01-15
