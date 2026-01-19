# Marksheet OCR Web Application

A powerful Django web application that extracts student data from marksheet images using AI-powered OCR technology and exports to CSV format.

## Features

✨ **AI-Powered Extraction**: Uses Google Gemini Vision API for accurate text extraction
📊 **Subject-wise Marks**: Extracts Theory (ESE + Internal) and Practical (Practical + Internal) marks
🎯 **Auto Calculation**: Automatically calculates totals, percentages, and pass/fail status
📥 **CSV Export**: Download extracted data in two formats:
   - Summary CSV (one row per student with all subjects)
   - Detailed CSV (one row per student per subject)
🎨 **Modern UI**: Beautiful glassmorphism design with smooth animations
📱 **Responsive**: Works perfectly on all devices

## Tech Stack

- **Backend**: Django 5.0
- **AI/OCR**: Google Gemini Vision API
- **Data Processing**: Pandas, OpenCV, Pillow
- **Frontend**: Bootstrap 5, Vanilla JavaScript
- **Database**: SQLite (can be changed to PostgreSQL/MySQL)

## Installation

### 1. Clone or Navigate to Project
```bash
cd d:\exapp
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Edit the `.env` file and add your Google Gemini API key:
```
GEMINI_API_KEY=your-actual-api-key-here
```

**Get your API key**: https://makersuite.google.com/app/apikey

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

### 7. Access the Application
- **Main App**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/

## Usage

### Upload Marksheet

1. Navigate to http://localhost:8000/
2. Drag and drop your marksheet image or click to browse
3. Click "Process Marksheet"
4. Wait for AI to extract the data (usually takes 5-15 seconds)

### View Results

After processing, you'll see:
- Student information (Roll Number, Name, Father's Name)
- Subject-wise marks breakdown
- Total marks and percentage
- Pass/Fail status with division

### Download CSV

Two export options:
1. **Download CSV**: Summary format with all subjects in columns
2. **Detailed CSV**: One row per student per subject

## CSV Format

### Summary CSV
```
Roll Number, Student Name, Father Name, Subject 1, Subject 1 Marks, ..., Total Marks, Percentage, Result
```

### Detailed CSV
```
Roll Number, Student Name, Father Name, Subject Code, Subject Name, Theory ESE, Theory Internal, Theory Total, Practical, Practical Internal, Practical Total, Subject Total, Status
```

## Project Structure

```
exapp/
├── marksheet_project/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── marksheet_ocr/              # Main application
│   ├── models.py               # Database models
│   ├── views.py                # View functions
│   ├── forms.py                # Upload form
│   ├── admin.py                # Admin configuration
│   ├── services/               # Business logic
│   │   ├── ai_extractor.py     # Gemini AI integration
│   │   └── csv_exporter.py     # CSV generation
│   ├── templates/              # HTML templates
│   └── static/                 # CSS and JavaScript
├── media/                      # Uploaded images
├── requirements.txt
├── .env
└── manage.py
```

## Models

### MarksheetUpload
Stores uploaded marksheet images and processing status.

### Student
Student information including roll number, name, father's name, etc.

### Subject
Subject details with code and name.

### Mark
Individual marks for each student-subject combination:
- Theory ESE (External Semester Examination)
- Theory Internal
- Practical marks
- Practical Internal

## API Key Setup

1. Visit https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key
5. Paste it in the `.env` file:
   ```
   GEMINI_API_KEY=your-copied-api-key-here
   ```

## Troubleshooting

### "GEMINI_API_KEY not set" Error
Make sure you've added your API key to the `.env` file.

### Image Upload Fails
- Check file size (max 10MB)
- Ensure file format is JPEG, PNG, BMP, or TIFF
- Verify media folder has write permissions

### No Students Extracted
- Ensure the marksheet image is clear and readable
- Try uploading a higher resolution image
- Check the admin panel for error messages

## Development

### Run Tests
```bash
python manage.py test
```

### Collect Static Files (for production)
```bash
python manage.py collectstatic
```

### Create New Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - feel free to use this project for educational or commercial purposes.

## Credits

- **AI**: Google Gemini Vision API
- **Framework**: Django
- **UI**: Bootstrap 5
- **Icons**: Font Awesome

---

**Made with ❤️ using Django and AI**
