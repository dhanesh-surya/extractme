# 🚀 DEPLOYMENT INSTRUCTIONS

I have applied the necessary fixes to resolve the 502 Error. You now need to deploy these changes to Render.

## 1. Commit and Push Changes

Run the following commands in your terminal to push the fixes to your repository:

```powershell
git add marksheet_ocr/services/ai_extractor.py render.yaml
git commit -m "Fix 502 error: Add image resizing and increase server timeout"
git push origin main
```

*(Note: Replace `main` with `master` if that is your branch name)*

## 2. Verify Render Environment

While the deployment is running, verify your Render configuration:

1. Go to **Render Dashboard** -> **extractme-1** -> **Environment**
2. Ensure `GEMINI_API_KEY` is present and valid.
   - If it is missing or has a placeholder value, click "Edit" and paste your real API key (starts with `AIza...`).
   - You can get a key from [Google AI Studio](https://aistudio.google.com/app/apikey).

## 3. Monitor Deployment

1. Go to **Render Dashboard** -> **extractme-1** -> **Events**
2. Wait for the "Deploy" event to finish.

## 4. Test the Fix

1. Open https://extractme-1.onrender.com
2. Upload a marksheet image.
3. Click **Process**.
4. It should now work!

---

## ℹ️ What Was Fixed?

1. **Timeout Issue**: Increased server timeout from 30 seconds to **300 seconds** (5 minutes) to allow AI processing time.
2. **Memory Issue**: Added **smart image resizing** to shrink large images (max 1024px) before sending to AI, preventing crashes.
3. **Resource Control**: Limited server to **1 worker** to prevent running out of RAM on the free tier.

These changes directly address the 502 Bad Gateway error.
