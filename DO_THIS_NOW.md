# ⚡ URGENT: What to Do Right Now

## 🚨 Your app is getting 502 error on homepage

**This means: App is crashing on startup**

---

## ✅ I Just Fixed 2 Critical Issues:

1. **Gunicorn Port Binding** - Wasn't binding to correct port
2. **Build Script** - Added verbose logging

**Commit:** `b675d0c`
**Status:** Pushed to GitHub ✅

---

## 🎯 What YOU Need to Do NOW:

### ⏰ Action 1: Check Render Dashboard (2 minutes)

1. Open: https://dashboard.render.com
2. Click your **"extractme"** service
3. Look at the status indicator (top of page)

**What color is it?**

- 🟢 **Green "Live"** → Go to Action 2
- 🔴 **Red "Deploy Failed"** → Go to Action 3
- 🟡 **Yellow "Building"** → Wait 3 minutes, then check again
- ⚪ **Gray "Suspended"** → Go to Action 4

---

### 🟢 Action 2: If Status is GREEN "Live"

The service is running but misconfigured.

**Check Logs:**
1. Click **"Logs"** tab
2. Click **"Service Logs"**
3. Scroll to bottom
4. Look for ERROR messages

**Common Errors & Fixes:**

**See this error?**
```
DisallowedHost at / Invalid HTTP_HOST header
```
**Fix:** I updated the code, wait for redeploy (should be happening now)

**See this error?**
```
FATAL: database "extractme" does not exist
or
could not connect to server
```
**Fix:** DATABASE_URL not set
→ Go to "Environment" tab
→ Check if `DATABASE_URL` exists
→ If missing, see **Action 5** below

**See this error?**
```
GEMINI_API_KEY not set
```
**Fix:** Add in Environment tab:
- Key: `GEMINI_API_KEY`
- Value: Your API key from https://makersuite.google.com/app/apikey

---

### 🔴 Action 3: If Status is RED "Deploy Failed"

The build process failed.

**Check Build Logs:**
1. Click **"Logs"** tab  
2. Click **"Deploy Logs"**
3. Scroll to where it says "ERROR" or "failed"

**Common Build Errors:**

**See this?**
```
ERROR: Could not find a version that satisfies
```
**Meaning:** requirements.txt has wrong package versions
**Fix:** Should be fixed in latest code (wait for current deploy)

**See this?**
```
./build.sh: Permission denied
```
**Meaning:** Build script not executable
**Fix:** New code fixes this (wait for deploy)

**See this?**
```
No web process running
```
**Meaning:** Gunicorn didn't start
**Fix:** I updated gunicorn command (wait for deploy)

---

### 🟡 Action 4: If Status is GRAY "Suspended"

Free tier service went to sleep.

**Fix:**
1. Click "Manual Deploy" button
2. Select "Deploy latest commit"
3. Wait 3-5 minutes

---

### 🗄️ Action 5: If DATABASE_URL is Missing

You didn't deploy via Blueprint, need to connect database manually.

**Steps:**

1. **Check if database exists:**
   - In Render dashboard, look in left sidebar
   - Do you see "extractme-db" listed?

2. **If DATABASE exists:**
   - Click on "extractme-db"
   - Copy "Internal Database URL"
   - Go to your web service
   - Click "Environment" tab
   - Click "Add Environment Variable"
   - Key: `DATABASE_URL`
   - Value: (paste the URL you copied)
   - Click "Save"

3. **If DATABASE does NOT exist:**
   - Click "New +" → "PostgreSQL"
   - Name: `extractme-db`  
   - Region: Same as your web service
   - Plan: Free
   - Click "Create Database"
   - Wait 2 minutes
   - Then follow step 2 above

---

## 🔍 What to Tell Me If Still Broken

If none of this works, I need to see the actual error.

**Copy and paste:**

1. **Service Status:** (Green/Red/Yellow/Gray)

2. **Last 20 lines from Service Logs:**
   (Go to Logs → Service Logs → Copy last 20 lines)

3. **Environment Variables List:**
   (Go to Environment → Tell me which ones are present)
   - DATABASE_URL: Yes/No
   - GEMINI_API_KEY: Yes/No
   - SECRET_KEY: Yes/No

---

## ⏱️ Timeline

- **Code pushed:** January 19, 2026, 20:03 IST
- **Commit:** b675d0c
- **Deploy should complete:** Within 5 minutes
- **Expected:** Issue should be fixed

---

## 📞 Quick Reference

**Render Dashboard:** https://dashboard.render.com
**Your App URL:** https://extractme-4o5m.onrender.com
**Get Gemini Key:** https://makersuite.google.com/app/apikey

---

**Check Render dashboard NOW and follow the actions based on what you see!** 🚀

The latest code should fix the Gunicorn binding issue, but you may need to set up DATABASE_URL if you deployed manually.
