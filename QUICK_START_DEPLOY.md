# Quick Start: Deploy to Render.com

## ✅ What Has Been Done

All necessary files and configurations have been prepared for Render.com deployment:

1. **Settings Updated** - Django settings now support both development and production
2. **Dependencies Added** - PostgreSQL drivers and database URL parser included
3. **Configuration Files Created**:
   - `render.yaml` - Automated deployment blueprint
   - `runtime.txt` - Python version specification
   - `.gitignore` - Protects sensitive files
   - `.env.example` - Environment variable template
4. **Documentation Created**:
   - `RENDER_DEPLOYMENT.md` - Complete deployment guide
   - `DEPLOYMENT_CHECKLIST.md` - Step-by-step checklist
   - `DEPLOYMENT_CHANGES.md` - Summary of all changes

## 🚀 Next Steps (YOU Need to Do These)

### Step 1: Verify Local Setup Still Works

```powershell
# Install new dependencies
pip install -r requirements.txt

# Test the app locally (optional)
python manage.py runserver
```

Visit http://localhost:8000 to verify everything still works.

### Step 2: Commit and Push to Git

```powershell
# Add all changes
git add .

# Commit
git commit -m "Prepare for Render.com deployment with PostgreSQL support"

# Push to your repository
git push origin main
```

**Note:** Make sure you have a Git repository set up (GitHub, GitLab, or Bitbucket).

### Step 3: Deploy on Render.com

#### Option A: Blueprint Deployment (Easiest) ⭐

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Blueprint"**
3. Connect your Git repository
4. Render will auto-detect `render.yaml` and create:
   - Web Service: `extractme`
   - PostgreSQL Database: `extractme-db`
5. Click **"Apply"**

#### Option B: Manual Deployment

See `RENDER_DEPLOYMENT.md` for detailed manual setup instructions.

### Step 4: Set Environment Variables

After deployment starts, you need to set one critical variable:

1. Go to your web service on Render dashboard
2. Click **"Environment"** tab
3. Add:
   - **Key:** `GEMINI_API_KEY`
   - **Value:** Your actual Google Gemini API key

**Other variables are auto-configured:**
- `SECRET_KEY` - Auto-generated
- `DEBUG` - Set to False
- `DATABASE_URL` - Auto-linked from database
- `RENDER` - Auto-set
- `RENDER_EXTERNAL_HOSTNAME` - Auto-set

### Step 5: Wait for Deployment

Monitor the deployment in the **"Logs"** tab. It should:
1. ✅ Install dependencies
2. ✅ Run database migrations
3. ✅ Collect static files
4. ✅ Start Gunicorn server
5. ✅ Show "Live" status (green)

### Step 6: Create Admin User

Once deployed:

1. Open the **"Shell"** tab in Render dashboard
2. Run:
   ```bash
   python manage.py createsuperuser
   ```
3. Follow the prompts to create username/password

### Step 7: Access Your App

Your app will be available at:
- **Main App:** `https://extractme-xxxx.onrender.com`
- **Admin Panel:** `https://extractme-xxxx.onrender.com/admin`

(Replace `xxxx` with your actual Render subdomain)

## 📋 Important Notes

### Free Tier Behavior
- **Spin Down:** After 15 minutes of inactivity, the service sleeps
- **Spin Up:** First request after sleep takes 50+ seconds to respond
- **This is normal** for free tier services

### Get Your GEMINI_API_KEY
If you don't have one:
1. Visit https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Click "Create API Key"
4. Copy the key
5. Add it to Render environment variables

## 🆘 Troubleshooting

### Build Fails
- Check **Logs** tab for specific error
- Most common: Missing environment variables
- Ensure `GEMINI_API_KEY` is set

### 502 Bad Gateway
- Service might be spinning up (wait 60 seconds)
- Check if `DATABASE_URL` is connected
- Verify build completed successfully

### Static Files Not Loading
- Should auto-work with WhiteNoise
- Check build logs for `collectstatic` output
- May need to hard refresh browser (Ctrl+Shift+R)

### Database Connection Errors
- Ensure database is created and linked
- Check `DATABASE_URL` environment variable exists
- Verify database status is "Available"

## 📚 Full Documentation

For complete details, see:
- **`RENDER_DEPLOYMENT.md`** - Comprehensive deployment guide
- **`DEPLOYMENT_CHECKLIST.md`** - Step-by-step checklist
- **`DEPLOYMENT_CHANGES.md`** - Technical changes summary

## ⚡ Quick Reference Commands

### Local Development
```powershell
python manage.py runserver
```

### Check for Issues
```powershell
python manage.py check
python manage.py migrate --plan
```

### Collect Static (Test)
```powershell
python manage.py collectstatic --no-input
```

## 🎯 Success Checklist

- [ ] Code pushed to Git
- [ ] Render Blueprint created
- [ ] Service deployed (status: Live)
- [ ] `GEMINI_API_KEY` set in environment
- [ ] Superuser created
- [ ] App accessible at Render URL
- [ ] File upload works
- [ ] OCR processing works
- [ ] Admin panel accessible

---

**Ready to deploy!** Follow the steps above and you'll be live on Render.com in minutes! 🚀
