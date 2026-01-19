# Render.com Deployment Guide

## Prerequisites
- A Render.com account (sign up at https://render.com)
- Your code pushed to a Git repository (GitHub, GitLab, or Bitbucket)

## Deployment Options

### Option 1: Using render.yaml Blueprint (Recommended)

1. **Push your code to Git**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push
   ```

2. **Deploy on Render**
   - Go to https://dashboard.render.com
   - Click "New +" → "Blueprint"
   - Connect your repository
   - Render will automatically detect `render.yaml` and create:
     - Web Service (extractme)
     - PostgreSQL Database (extractme-db)

3. **Set Environment Variables**
   - Navigate to your web service in Render dashboard
   - Go to "Environment" tab
   - Add/update:
     - `GEMINI_API_KEY` - Your Google Gemini API key
     - `SECRET_KEY` - Auto-generated (already set)
     - `DEBUG` - Set to `False` (already set)
     - `DATABASE_URL` - Auto-linked to database (already set)

### Option 2: Manual Setup

1. **Create PostgreSQL Database**
   - In Render dashboard, click "New +" → "PostgreSQL"
   - Name: `extractme-db`
   - Plan: Free
   - Click "Create Database"
   - Copy the "Internal Database URL"

2. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect your repository
   - Configure:
     - **Name**: extractme
     - **Runtime**: Python 3
     - **Build Command**: `./build.sh`
     - **Start Command**: `gunicorn marksheet_project.wsgi:application`
     - **Plan**: Free

3. **Add Environment Variables**
   - `DATABASE_URL` - Paste the Internal Database URL from step 1
   - `SECRET_KEY` - Generate a secure random string
   - `DEBUG` - Set to `False`
   - `RENDER` - Set to `true`
   - `GEMINI_API_KEY` - Your Google Gemini API key
   - `ALLOWED_HOSTS` - Your Render URL (e.g., `extractme-4o5m.onrender.com`)

4. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy your application

## Post-Deployment

### Create Superuser
Once deployed, you'll need to create an admin user:

1. Open the Shell in Render dashboard (under "Shell" tab)
2. Run:
   ```bash
   python manage.py createsuperuser
   ```
3. Follow the prompts

### Access Your Application
- **Main App**: https://your-app-name.onrender.com
- **Admin Panel**: https://your-app-name.onrender.com/admin

## Important Notes

### Free Tier Limitations
- **Spin Down**: Free services spin down after 15 minutes of inactivity
- **First Request**: Takes 50+ seconds as service spins up
- **Database**: 1 GB storage limit
- **Uptime**: Not guaranteed 24/7

### Static Files
- Handled by WhiteNoise middleware
- Automatically collected during build (`collectstatic`)
- Compressed and cached for performance

### Media Files
- **Warning**: Media files are stored on ephemeral disk
- Files are deleted on redeploy or service restart
- For production, use cloud storage (AWS S3, Cloudinary, etc.)

### Database Backups
- Render provides automatic backups for paid plans
- Free tier: Export data manually via Render dashboard

## Troubleshooting

### 502 Bad Gateway
- Check build logs for errors
- Ensure all dependencies in `requirements.txt`
- Verify `DATABASE_URL` is set correctly
- Check that migrations ran successfully

### Application Errors
- Check application logs in Render dashboard
- Ensure `DEBUG=False` in production
- Verify environment variables are set

### Static Files Not Loading
- Check build logs for `collectstatic` output
- Verify WhiteNoise is in `MIDDLEWARE` (already configured)
- Check `STATIC_ROOT` and `STATIC_URL` settings

### Database Connection Issues
- Verify `DATABASE_URL` environment variable
- Check database is active in Render dashboard
- Ensure `psycopg2-binary` is in requirements.txt

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | - | PostgreSQL connection string (auto-provided by Render) |
| `SECRET_KEY` | Yes | - | Django secret key (generate random string) |
| `DEBUG` | No | False | Debug mode (should be False in production) |
| `RENDER` | No | - | Set to `true` to enable Render-specific settings |
| `GEMINI_API_KEY` | Yes | - | Google Gemini API key for OCR functionality |
| `ALLOWED_HOSTS` | No | localhost,127.0.0.1 | Comma-separated list of allowed hosts |

## Monitoring

### View Logs
1. Go to Render dashboard
2. Select your service
3. Click "Logs" tab
4. Real-time logs will stream

### Metrics
- View request metrics in "Metrics" tab
- Monitor response times
- Track memory usage

## Updating Your Application

### Automatic Deployment
- By default, Render auto-deploys on Git push to main branch
- Check "Auto-Deploy" setting in service settings

### Manual Deployment
1. Push changes to Git
2. In Render dashboard, click "Manual Deploy" → "Deploy latest commit"

### Rolling Back
1. Go to "Events" tab
2. Find previous successful deploy
3. Click "Rollback to this version"

## Cost Optimization

### Free Tier Best Practices
- Use spinning down for development/staging
- Upgrade to paid plan for production (no spin down)
- Monitor database size (1 GB limit on free tier)
- Consider background jobs carefully (separate service)

## Security Checklist

- [x] `DEBUG=False` in production
- [x] Strong `SECRET_KEY` generated
- [x] `ALLOWED_HOSTS` configured properly
- [x] Database connection via `DATABASE_URL`
- [x] Environment variables not in version control
- [ ] Regular security updates (`pip list --outdated`)
- [ ] Monitor Render security advisories

## Support

- **Render Docs**: https://render.com/docs
- **Django Deployment**: https://docs.djangoproject.com/en/stable/howto/deployment/
- **Community**: https://community.render.com

---

**Last Updated**: January 2026
