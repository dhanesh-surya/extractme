# Deployment Architecture

## Local Development Environment

```
┌─────────────────────────────────────────┐
│     Your Computer (Windows)              │
│                                          │
│  ┌──────────────────────────────────┐   │
│  │  Django Development Server       │   │
│  │  http://localhost:8000           │   │
│  └──────────────────────────────────┘   │
│               │                          │
│               ▼                          │
│  ┌──────────────────────────────────┐   │
│  │  SQLite Database                 │   │
│  │  db.sqlite3                      │   │
│  └──────────────────────────────────┘   │
│               │                          │
│               ▼                          │
│  ┌──────────────────────────────────┐   │
│  │  Static Files                    │   │
│  │  (Served by Django)              │   │
│  └──────────────────────────────────┘   │
│               │                          │
│               ▼                          │
│  ┌──────────────────────────────────┐   │
│  │  Media Files (uploads)           │   │
│  │  /media/                         │   │
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

## Production Environment (Render.com)

```
┌───────────────────────────────────────────────────────────────┐
│                    Render.com Cloud                            │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │              Web Service: extractme                       │ │
│  │        https://extractme-xxxx.onrender.com                │ │
│  │                                                            │ │
│  │  ┌──────────────────────────────────────────────────┐    │ │
│  │  │  Gunicorn (WSGI Server)                          │    │ │
│  │  │  - Workers: Multiple processes                   │    │ │
│  │  │  - Handles HTTP requests                         │    │ │
│  │  └──────────────────────────────────────────────────┘    │ │
│  │               │                                            │ │
│  │               ▼                                            │ │
│  │  ┌──────────────────────────────────────────────────┐    │ │
│  │  │  Django Application                              │    │ │
│  │  │  - Views, Models, Templates                      │    │ │
│  │  │  - Business Logic                                │    │ │
│  │  │  - OCR Processing (Gemini AI)                    │    │ │
│  │  └──────────────────────────────────────────────────┘    │ │
│  │               │                                            │ │
│  │               ▼                                            │ │
│  │  ┌──────────────────────────────────────────────────┐    │ │
│  │  │  WhiteNoise Middleware                           │    │ │
│  │  │  - Serves static files                           │    │ │
│  │  │  - Compression & caching                         │    │ │
│  │  └──────────────────────────────────────────────────┘    │ │
│  └──────────────────────────────────────────────────────────┘ │
│               │                                                │
│               ▼                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │         PostgreSQL Database: extractme-db                 │ │
│  │         - Persistent data storage                         │ │
│  │         - User accounts, marksheets, students, marks      │ │
│  │         - Automatic backups (paid plans)                  │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │         Ephemeral Disk Storage                            │ │
│  │         - Media files (uploaded images)                   │ │
│  │         ⚠️  Cleared on redeploy/restart                   │ │
│  └──────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────┘
               │
               ▼
┌───────────────────────────────────────────────────────────────┐
│                External Services                               │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │         Google Gemini Vision API                          │ │
│  │         - OCR text extraction                             │ │
│  │         - Marksheet data parsing                          │ │
│  └──────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────┘
```

## Request Flow

```
User Browser
    │
    │ HTTPS Request
    │
    ▼
┌─────────────────────┐
│  Render.com CDN/LB  │  ← SSL/TLS termination
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  Gunicorn Server    │
└─────────────────────┘
    │
    ├─── Static Files? ──► WhiteNoise ──► Return CSS/JS/Images
    │
    ├─── Upload Image? ──► Django Views ──► Save to Disk
    │                          │
    │                          ▼
    │                     Gemini API ──► Extract Data
    │                          │
    │                          ▼
    │                    PostgreSQL ──► Save Data
    │                          │
    │                          ▼
    │                   Render Template ──► Return HTML
    │
    └─── Download CSV? ──► Generate CSV ──► Return File
```

## Environment Variables Flow

```
┌─────────────────────┐
│  Render Dashboard   │
│  Environment Tab    │
└─────────────────────┘
         │
         │ Sets Environment Variables:
         │ - SECRET_KEY
         │ - DEBUG=False
         │ - DATABASE_URL (auto from DB)
         │ - GEMINI_API_KEY
         │ - RENDER=true
         │ - RENDER_EXTERNAL_HOSTNAME
         │
         ▼
┌─────────────────────┐
│  Django Settings    │
│  settings.py        │
└─────────────────────┘
         │
         │ Reads via os.getenv()
         │
         ▼
┌─────────────────────┐
│  Application Config │
│  - Database conn    │
│  - Debug mode       │
│  - Allowed hosts    │
│  - API keys         │
└─────────────────────┘
```

## Build Process

```
1. Git Push
   │
   ▼
2. Render Detects Change
   │
   ▼
3. Pull Latest Code
   │
   ▼
4. Run build.sh
   │
   ├─► pip install -r requirements.txt
   │   ├─ Django
   │   ├─ Pillow
   │   ├─ psycopg2-binary
   │   ├─ gunicorn
   │   ├─ whitenoise
   │   └─ ... other deps
   │
   ├─► python manage.py migrate
   │   └─ Create/update database tables
   │
   └─► python manage.py collectstatic
       └─ Gather all static files
   │
   ▼
5. Start Application
   │
   └─► gunicorn marksheet_project.wsgi:application
       └─ Application is Live!
```

## Deployment Options Comparison

### Option 1: Blueprint (Recommended)
```
render.yaml
    │
    └─► Render Dashboard
            │
            ├─► Auto-creates Web Service
            ├─► Auto-creates Database
            ├─► Auto-links DATABASE_URL
            └─► One-click deploy
```

### Option 2: Manual
```
Render Dashboard
    │
    ├─► Manually create Database
    │   └─► Copy DATABASE_URL
    │
    └─► Manually create Web Service
        ├─► Set build command
        ├─► Set start command
        ├─► Paste DATABASE_URL
        └─► Set other env vars
```

## Data Flow: File Upload to Results

```
1. User uploads marksheet image
         │
         ▼
2. Django Form Validation
         │
         ▼
3. Save to Media folder (ephemeral)
         │
         ▼
4. Send to Gemini Vision API
         │
         ▼
5. Receive JSON response
         │
         ▼
6. Parse and validate data
         │
         ▼
7. Create Django models:
   ├─► Student
   ├─► Subjects
   └─► Marks
         │
         ▼
8. Save to PostgreSQL
         │
         ▼
9. Render results template
         │
         ▼
10. Display to user
    ├─► View results
    └─► Download CSV
```

## Database Schema (Simplified)

```
┌──────────────────┐
│  MarksheetUpload │
├──────────────────┤
│ id               │
│ image            │
│ uploaded_at      │
│ status           │
└──────────────────┘
         │
         │ 1:N
         ▼
┌──────────────────┐      ┌──────────────────┐
│     Student      │──┐   │     Subject      │
├──────────────────┤  │   ├──────────────────┤
│ id               │  │   │ id               │
│ roll_number      │  │   │ code             │
│ name             │  │   │ name             │
│ father_name      │  │   └──────────────────┘
│ upload_id (FK)   │  │            │
└──────────────────┘  │            │
         │            │            │
         │            │            │
         │ N          │ M          │ N
         └────────────┼────────────┘
                      │
                      ▼
              ┌──────────────────┐
              │       Mark       │
              ├──────────────────┤
              │ id               │
              │ student_id (FK)  │
              │ subject_id (FK)  │
              │ theory_ese       │
              │ theory_internal  │
              │ practical        │
              │ practical_int    │
              └──────────────────┘
```

## Security Layers

```
┌─────────────────────────────────────┐
│  Render.com Infrastructure          │
│  - DDoS protection                  │
│  - Auto SSL/TLS                     │
│  - Network isolation                │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│  Application Security               │
│  - DEBUG=False (no error details)   │
│  - ALLOWED_HOSTS restriction        │
│  - CSRF protection                  │
│  - SQL injection protection (ORM)   │
│  - XSS protection (template engine) │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│  Data Security                      │
│  - Environment variables (secrets)  │
│  - Database encryption at rest      │
│  - Secure connections (SSL)         │
└─────────────────────────────────────┘
```

---

**This architecture provides:**
✅ Scalability (can upgrade Render plan)
✅ Security (multiple layers)
✅ Reliability (Render's infrastructure)
✅ Simplicity (minimal configuration)
✅ Cost-effective (free tier available)
