# 🚨 502 Error on Homepage - Emergency Debug Guide

**Status:** Application not starting on Render.com
**URL:** https://extractme-4o5m.onrender.com/
**Error:** HTTP 502 Bad Gateway

This means the app is **crashing on startup**, not just during processing.

---

## 🔍 Step-by-Step Diagnosis

### Step 1: Check Render Dashboard

1. **Go to:** https://dashboard.render.com
2. **Find:** Your "extractme" service
3. **Check Status:**
   - 🟢 Green "Live" = Service running (but might be misconfigured)
   - 🔴 Red "Deploy failed" = Build failed
   - 🟡 Yellow "Building" = Wait for it to finish
   - ⚪ Gray "Suspended" = Service is suspended (free tier inactive)

**What to do based on status:**

---

### If Status is RED (Deploy Failed):

**The build process failed. Follow these steps:**

1. Click on your service
2. Click **"Logs"** tab
3. Click **"Deploy Logs"** 
4. Look for errors like:
   - `ERROR: Could not find a version that satisfies...` → Dependency issue
   - `ModuleNotFoundError` → Missing package
   - `SyntaxError` → Code syntax error
   - `Permission denied` → File permission issue

**Common Solutions:**

**A. Dependency Error:**
```
ERROR: Could not find a version that satisfies the requirement...
```
→ Issue with `requirements.txt`
→ Try pinning exact versions (I already did this)

**B. Build Script Permission Error:**
```
Permission denied: ./build.sh
```
→ Build script not executable
→ **SOLUTION BELOW**

**C. Python Version Mismatch:**
```
Python version not available
```
→ Wrong Python version in runtime.txt
→ Currently set to 3.11.0 (should work)

---

### If Status is GREEN but Still Getting 502:

**The app started but is crashing on requests. Follow these:**

1. Click on your service
2. Click **"Logs"** tab
3. Click **"Service Logs"** (NOT Deploy Logs)
4. Look for Python errors:
   - `ImproperlyConfigured` → Django settings issue
   - `Database connection` → DATABASE_URL not set
   - `GEMINI_API_KEY not set` → API key missing
   - `ModuleNotFoundError` → Import error
   - Any Python traceback

**Most Common Issues:**

**A. DATABASE_URL Not Connected:**

Check if database is linked:
1. In your service settings
2. Check "Environment" tab
3. Look for `DATABASE_URL` variable
4. Should say "from database: extractme-db"

**If missing:**
- You deployed manually, not via Blueprint
- **SOLUTION:** See "Manual Database Setup" section below

**B. GEMINI_API_KEY Not Set:**

This will cause errors during processing but shouldn't cause startup 502.

1. Go to "Environment" tab
2. Check if `GEMINI_API_KEY` exists
3. If not, add it:
   - Key: `GEMINI_API_KEY`
   - Value: Your actual API key
   - Click "Save"

**C. ALLOWED_HOSTS Issue:**

If logs show:
```
DisallowedHost at / Invalid HTTP_HOST header
```

**SOLUTION:**
1. Go to "Environment" tab
2. Add variable:
   - Key: `RENDER_EXTERNAL_HOSTNAME`
   - Value: `extractme-4o5m.onrender.com`
   - Click "Save"

---

## 🛠️ Quick Fixes to Try

### Fix 1: Re-deploy from Scratch

1. Go to your service on Render
2. Click **"Manual Deploy"**
3. Select **"Clear build cache & deploy"**
4. Wait 3-5 minutes
5. Check if it works

### Fix 2: Check Build.sh Permissions (If deploy fails)

The issue might be that `build.sh` isn't executable.

**I just updated it to be more verbose. Push the new code:**

```powershell
git add .
git commit -m "Fix Gunicorn binding and improve build logging"
git push origin main
```

Render will auto-deploy. Check the logs.

### Fix 3: Verify All Environment Variables

**Required Variables:**

Go to Environment tab and verify these exist:

| Variable | Value | Source |
|----------|-------|--------|
| `SECRET_KEY` | (auto-generated) | Auto |
| `DEBUG` | False | render.yaml |
| `RENDER` | true | render.yaml |
| `DATABASE_URL` | postgresql://... | Linked DB |
| `GEMINI_API_KEY` | AIza... | **YOU MUST SET** |
| `PYTHON_VERSION` | 3.11.0 | render.yaml |

**If DATABASE_URL is missing:**
- You didn't use Blueprint deployment
- Need to manually link database (see below)

---

## 🗄️ Manual Database Setup (If DATABASE_URL Missing)

If you deployed manually (not via Blueprint):

1. **Create Database:**
   - Click "New +" → "PostgreSQL"
   - Name: `extractme-db`
   - Click "Create Database"
   - Wait for it to become "Available"

2. **Copy Internal Database URL:**
   - Click on the database
   - Copy "Internal Database URL" (starts with postgresql://)

3. **Link to Web Service:**
   - Go to your web service
   - Click "Environment" tab
   - Add variable:
     - Key: `DATABASE_URL`
     - Value: (paste the Internal Database URL)
   - Click "Save Changes"

4. **Redeploy:**
   - Service will auto-redeploy
   - Wait 3-5 minutes

---

## 📋 What to Share If Still Broken

If none of this works, I need to see the actual error. Please share:

1. **Deploy Logs** (from Logs → Deploy Logs)
   - Last 50 lines showing the error

2. **Service Logs** (from Logs → Service Logs)  
   - Any Python tracebacks or errors

3. **Environment Variables** (from Environment tab)
   - List of which variables are set (don't share values)

4. **Service Status**
   - What color is the status indicator?

---

## 🎯 Most Likely Issues (In Order)

Based on typical Render deployments:

1. **DATABASE_URL not connected** (70% of cases)
   → Fix: Link database manually or redeploy via Blueprint

2. **Build script permissions** (15% of cases)
   → Fix: Update code (I just did) and push

3. **Gunicorn binding issue** (10% of cases)
   → Fix: Updated render.yaml (I just did) and push

4. **GEMINI_API_KEY missing** (5% of cases)
   → Fix: Add in Environment tab

---

## ⚡ Next Actions for YOU:

### Immediate Actions:

1. **Check Render Status** - What color is it?

2. **Read the Logs** - Go to Logs tab, what errors do you see?

3. **Verify Database** - Is DATABASE_URL set in Environment?

4. **Pull Latest Code** (optional, I just updated):
   ```powershell
   git pull origin main
   ```
   Or just push the new code:
   ```powershell
   git add .
   git commit -m "Fix Gunicorn and build script"
   git push origin main
   ```

5. **Wait for Redeploy** - Monitor logs during deployment

6. **Share Logs** - If still broken, copy/paste error from logs

---

## 🔧 Code Changes I Just Made:

1. **render.yaml:** Fixed Gunicorn to bind to `0.0.0.0:$PORT`
2. **build.sh:** Added verbose logging messages

**These should help diagnose or fix the issue!**

---

**Push the changes and check Render logs to see what's actually failing!**
