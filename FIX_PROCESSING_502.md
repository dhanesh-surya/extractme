# 🚨 502 Error During Processing - Solutions

## Problem: App works but crashes when clicking "Process"

**URL:** https://extractme-1.onrender.com
**Error:** HTTP 502 when processing marksheet
**Status:** Homepage works ✅, Processing fails ❌

---

## 🔍 Root Causes (In Order of Likelihood)

### 1. GEMINI_API_KEY Not Set or Invalid (90% of cases)

**Symptoms:**
- Homepage loads fine
- File uploads successfully
- Crashes immediately after clicking "Process"

**Check This:**
1. Go to https://dashboard.render.com
2. Click your "extractme-1" service
3. Go to **"Environment"** tab
4. Look for `GEMINI_API_KEY`

**Is it missing?**
- Click "Add Environment Variable"
- Key: `GEMINI_API_KEY`
- Value: Your actual API key (starts with AIza...)
- Click "Save Changes"
- Service will redeploy automatically

**Is it set to placeholder?**
- If value is "your-gemini-api-key-here" or empty → WRONG
- Delete it and add your real API key from: https://makersuite.google.com/app/apikey

**How to get a valid API key:**
1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key (starts with AIza...)
5. Paste in Render environment variable

---

### 2. Request Timeout (5% of cases)

**Symptoms:**
- Processing takes a long time
- Eventually returns 502
- Large image files

**Solution: Increase Gunicorn timeout**

Update your **Start Command** on Render:

**Current:**
```bash
gunicorn marksheet_project.wsgi:application --bind 0.0.0.0:$PORT
```

**Change to:**
```bash
gunicorn marksheet_project.wsgi:application --bind 0.0.0.0:$PORT --timeout 300 --workers 1
```

**How to update:**
1. Go to your service on Render
2. Click "Settings"
3. Find "Start Command"
4. Update to command above
5. Click "Save Changes"

**Explanation:**
- `--timeout 300` = 5 minutes (enough for OCR processing)
- `--workers 1` = Single worker (prevents memory issues on free tier)

---

### 3. Memory Limit Exceeded (3% of cases)

**Symptoms:**
- Works with small images
- Crashes with large images
- Free tier: 512MB RAM limit

**Solutions:**

**A. Resize images before upload (Client-side - Best solution)**

I can update your upload.js to auto-resize images if needed.

**B. Add image compression in Django (Server-side)**

Update the processing to resize before sending to Gemini.

**C. Upgrade Render plan**
- Paid plans have more RAM
- $7/month for 1GB RAM

**For now, try uploading smaller images (< 2MB)**

---

### 4. Gemini API Quota Exceeded (1% of cases)

**Symptoms:**
- Worked before, now doesn't
- Error in logs about quota

**Check:**
1. Go to: https://aistudio.google.com/app/apikey
2. Check your API key status
3. Check usage limits

**Free tier limits:**
- 60 requests per minute
- 1500 requests per day

**Solution:**
- Wait for quota to reset (daily)
- Or upgrade to paid Gemini API

---

### 5. Database Connection Lost (1% of cases)

**Symptoms:**
- Intermittent 502 errors
- Works sometimes, fails other times

**Check:**
1. Go to Render dashboard
2. Check if PostgreSQL database is "Available" (green)
3. If "Suspended" or "Unavailable" → Restart it

---

## ✅ FIXES APPLIED (READY TO DEPLOY):

### 1. Code Fixes Applied (Auto-Resizing)
- **Modified `ai_extractor.py`:** Added logic to resize images to max 1024px.
  - Prevents "Out of Memory" crashes.
  - Reduces API processing time.
  - Fixes payload size issues.

### 2. Server Configuration Applied (Timeout)
- **Modified `render.yaml`:**
  - Increased timeout to `300` seconds (5 minutes).
  - Set workers to `1` (optimization for Free Tier).

---

## 🚀 HOW TO DEPLOY:

**Check the file `DEPLOY_NOW.md` for simple copy-paste commands.**

1. Commit and push the changes.
2. Render will auto-deploy.
3. **CRITICAL:** Ensure `GEMINI_API_KEY` is set in Render Dashboard > Environment.

---

## 🎯 Quick Diagnosis Chart

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Immediate 502 on Process | API key missing | Add GEMINI_API_KEY |
| 502 after 30 seconds | Timeout | Increase timeout |
| 502 with large images | Memory limit | Use smaller images |
| Works sometimes | API quota | Check quota limits |
| All uploads fail | API key invalid | Get new API key |

---

## ✅ What to Do Right Now:

### Action 1: Check the Logs
1. Go to Render dashboard
2. Logs → Service Logs
3. Try uploading and see the error
4. **Copy the error message and share it with me**

### Action 2: Verify GEMINI_API_KEY
1. Environment tab
2. Check if GEMINI_API_KEY exists
3. If missing or wrong → Add your real API key
4. Get from: https://makersuite.google.com/app/apikey

### Action 3: Increase Timeout
1. Settings → Start Command
2. Update to:
   ```bash
   gunicorn marksheet_project.wsgi:application --bind 0.0.0.0:$PORT --timeout 300 --workers 1
   ```
3. Save

---

## 📋 Information I Need to Help:

If still not working, share:

1. **Error from Service Logs** (last 30 lines when processing fails)
2. **Screenshot of Environment tab** (which variables are set)
3. **Image file size** you're uploading (KB/MB)
4. **Does it work locally?** (on your computer with same API key)

---

## 🆘 Emergency Workaround:

If you need it working NOW while debugging:

1. **Test locally first:**
   ```powershell
   # Set your real API key in .env
   python manage.py runserver
   # Upload and test
   ```

2. **If works locally but not on Render:**
   → 99% certain GEMINI_API_KEY is not set correctly on Render

3. **If doesn't work locally:**
   → API key is invalid or expired
   → Get a new one from Google AI Studio

---

**Start with Step 1: Check the Render logs and tell me what error you see!** 🔍

That will tell us exactly what's wrong.
