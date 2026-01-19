from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .models import MarksheetUpload, Student, Subject, Mark
from .forms import MarksheetUploadForm
from .services.ai_extractor import AIExtractor
from .services.csv_exporter import CSVExporter
import traceback


def upload_marksheet(request):
    """Handle marksheet upload and display upload form"""
    if request.method == 'POST':
        form = MarksheetUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Save upload
                upload = form.save()
                
                # Process image with AI
                upload.status = 'processing'
                upload.save()
                
                try:
                    # Extract data using AI
                    extractor = AIExtractor()
                    students_data = extractor.extract_marksheet_data(upload.image.path)
                    
                    # Save extracted data to database
                    for student_data in students_data:
                        # Validate data
                        if not extractor.validate_student_data(student_data):
                            continue
                        
                        # Create student
                        student = Student.objects.create(
                            upload=upload,
                            roll_number=student_data.get('roll_number', ''),
                            name=student_data.get('name', ''),
                            father_name=student_data.get('father_name', ''),
                            mother_name=student_data.get('mother_name', ''),
                            enrollment_number=student_data.get('enrollment_number', '')
                        )
                        
                        # Create subjects and marks
                        for subject_data in student_data.get('subjects', []):
                            # Get or create subject
                            subject, created = Subject.objects.get_or_create(
                                code=subject_data.get('code', ''),
                                name=subject_data.get('name', '')
                            )
                            
                            # Create mark
                            Mark.objects.create(
                                student=student,
                                subject=subject,
                                theory_ese=subject_data.get('theory_ese'),
                                theory_internal=subject_data.get('theory_internal'),
                                practical_marks=subject_data.get('practical'),
                                practical_internal=subject_data.get('practical_internal')
                            )
                    
                    # Mark as completed
                    upload.status = 'completed'
                    upload.save()
                    
                    messages.success(request, 'Marksheet processed successfully!')
                    return redirect('view_results', upload_id=upload.id)
                    
                except ValueError as e:
                    upload.status = 'failed'
                    upload.error_message = str(e)
                    upload.save()
                    messages.error(request, f'Error: {str(e)}')
                    
                except Exception as e:
                    upload.status = 'failed'
                    upload.error_message = str(e)
                    upload.save()
                    messages.error(request, f'Processing failed: {str(e)}')
                    print(traceback.format_exc())
                    
            except Exception as e:
                messages.error(request, f'Upload failed: {str(e)}')
                print(traceback.format_exc())
    else:
        form = MarksheetUploadForm()
    
    # Get recent uploads
    recent_uploads = MarksheetUpload.objects.all()[:10]
    
    return render(request, 'marksheet_ocr/upload.html', {
        'form': form,
        'recent_uploads': recent_uploads
    })


def view_results(request, upload_id):
    """Display extracted results"""
    upload = get_object_or_404(MarksheetUpload, id=upload_id)
    students = upload.students.all().prefetch_related('marks__subject')
    
    return render(request, 'marksheet_ocr/results.html', {
        'upload': upload,
        'students': students
    })


def download_csv(request, upload_id):
    """Download results as CSV"""
    upload = get_object_or_404(MarksheetUpload, id=upload_id)
    students = upload.students.all().prefetch_related('marks__subject')
    
    # Export to CSV
    exporter = CSVExporter()
    csv_data = exporter.export_students_to_csv(students)
    
    # Create response
    filename = f"marksheet_summary_{upload_id}.csv"
    response = HttpResponse(csv_data.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


def download_detailed_csv(request, upload_id):
    """Download detailed results as CSV (one row per subject)"""
    upload = get_object_or_404(MarksheetUpload, id=upload_id)
    students = upload.students.all().prefetch_related('marks__subject')
    
    # Export to CSV
    exporter = CSVExporter()
    csv_data = exporter.export_detailed_csv(students)
    
    # Create response
    filename = f"marksheet_detailed_{upload_id}.csv"
    response = HttpResponse(csv_data.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


def download_excel(request, upload_id):
    """Download results as Excel"""
    upload = get_object_or_404(MarksheetUpload, id=upload_id)
    students = upload.students.all().prefetch_related('marks__subject')
    
    # Export to Excel
    exporter = CSVExporter()
    excel_data = exporter.export_students_to_excel(students)
    
    # Create response
    filename = f"marksheet_summary_{upload_id}.xlsx"
    response = HttpResponse(
        excel_data.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


def download_detailed_excel(request, upload_id):
    """Download detailed results as Excel (one row per subject)"""
    upload = get_object_or_404(MarksheetUpload, id=upload_id)
    students = upload.students.all().prefetch_related('marks__subject')
    
    # Export to Excel
    exporter = CSVExporter()
    excel_data = exporter.export_detailed_excel(students)
    
    # Create response
    filename = f"marksheet_detailed_{upload_id}.xlsx"
    response = HttpResponse(
        excel_data.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response
