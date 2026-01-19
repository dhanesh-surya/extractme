# Render.com Deployment Checklist

Use this checklist to ensure a smooth deployment to Render.com.

## Pre-Deployment

- [ ] Code is tested and working locally
- [ ] All changes committed to Git
- [ ] `.env` file is NOT committed (it's in `.gitignore`)
- [ ] Requirements.txt is up to date
- [ ] Database migrations are created and tested

## Git Repository

- [ ] Code pushed to GitHub/GitLab/Bitbucket
- [ ] Repository is accessible
- [ ] Main branch is up to date

## Render.com Setup

### Option A: Blueprint Deployment (Recommended)

- [ ] Logged into Render.com dashboard
- [ ] Created new Blueprint
- [ ] Connected repository
- [ ] Blueprint detected `render.yaml`
- [ ] Services created automatically:
  - [ ] Web Service: extractme
  - [ ] Database: extractme-db

### Option B: Manual Setup

- [ ] Created PostgreSQL database (extractme-db)
- [ ] Copied Internal Database URL
- [ ] Created Web Service (extractme)
- [ ] Connected repository
- [ ] Set build command: `./build.sh`
- [ ] Set start command: `gunicorn marksheet_project.wsgi:application`

## Environment Variables

Configure these in Render dashboard → Your Service → Environment tab:

- [ ] `SECRET_KEY` - Auto-generated or custom secure key
- [ ] `DEBUG` - Set to `False`
- [ ] `DATABASE_URL` - Auto-linked from database
- [ ] `RENDER` - Set to `true`
- [ ] `RENDER_EXTERNAL_HOSTNAME` - Auto-set by Render
- [ ] `GEMINI_API_KEY` - Your Google Gemini API key ⚠️ REQUIRED
- [ ] `ALLOWED_HOSTS` - Your Render URL (optional, auto-detected)

## First Deployment

- [ ] Deployment initiated
- [ ] Build logs show no errors
- [ ] Build completed successfully
- [ ] Service is "Live" (green status)

## Post-Deployment Verification

- [ ] Application URL accessible (https://your-app.onrender.com)
- [ ] Home page loads correctly
- [ ] Static files loading (CSS/JS working)
- [ ] No 502/500 errors

## Create Admin User

- [ ] Opened Shell in Render dashboard
- [ ] Ran: `python manage.py createsuperuser`
- [ ] Created admin credentials
- [ ] Admin panel accessible at /admin

## Test Core Functionality

- [ ] Upload page loads
- [ ] File upload works
- [ ] Image processing works (Gemini API responding)
- [ ] Results page displays correctly
- [ ] CSV download works
- [ ] Admin panel functional

## Common Issues Resolution

If deployment fails, check:

- [ ] Build logs for dependency errors
- [ ] All required packages in requirements.txt
- [ ] Environment variables are set correctly
- [ ] Database is connected and active
- [ ] GEMINI_API_KEY is valid

## Production Best Practices

- [ ] Monitor application logs regularly
- [ ] Set up error tracking (Sentry, etc.)
- [ ] Plan for database backups
- [ ] Consider upgrading from free tier for:
  - No spin-down delays
  - Better performance
  - Database backups
- [ ] Set up custom domain (if needed)
- [ ] Configure SSL (auto-provided by Render)

## Maintenance

- [ ] Document deployment process for team
- [ ] Set up staging environment (optional)
- [ ] Plan for data migration if needed
- [ ] Monitor service health in Render dashboard

## Emergency Rollback

If issues occur:
- [ ] Know how to access Render dashboard → Events
- [ ] Can identify last working deployment
- [ ] Can rollback to previous version

---

**Deployment Date**: _______________
**Deployed By**: _______________
**App URL**: https://_______________
**Database**: extractme-db
**Service**: extractme

**Notes**:
_____________________________________________
_____________________________________________
_____________________________________________
