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
        files = request.FILES.getlist('image')
        
        if not files:
            messages.error(request, 'No files selected.')
        elif len(files) > 5:
            messages.error(request, 'Maximum 5 files allowed per upload.')
        else:
            success_count = 0
            error_count = 0
            last_upload_id = None
            
            for file in files:
                # Create a mutable copy of POST data to validate each file individually if needed,
                # but we simplest way is to manually instantiate the form/model or just validation.
                # However, to reuse Form validation (file extension, size), we instantiate the form.
                
                # Note: 'image' field in form expects a single file. 
                # We can construct a dict for files for each iteration.
                form = MarksheetUploadForm(data=request.POST, files={'image': file})
                
                if form.is_valid():
                    try:
                        # Save upload
                        upload = form.save()
                        last_upload_id = upload.id
                        
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
                            success_count += 1
                            
                        except ValueError as e:
                            upload.status = 'failed'
                            upload.error_message = str(e)
                            upload.save()
                            error_count += 1
                            print(f"Processing error for {file.name}: {e}")
                            
                        except Exception as e:
                            upload.status = 'failed'
                            upload.error_message = str(e)
                            upload.save()
                            error_count += 1
                            print(f"Processing failed for {file.name}: {traceback.format_exc()}")
                            
                    except Exception as e:
                        error_count += 1
                        print(f"Upload failed for {file.name}: {e}")
                else:
                    error_count += 1
                    for error in form.errors.values():
                        messages.error(request, f"Error in {file.name}: {error}")

            if success_count > 0:
                messages.success(request, f'Successfully processed {success_count} marksheet(s).')
            
            if error_count > 0:
                messages.warning(request, f'Failed to process {error_count} marksheet(s). Check Recent Uploads for details.')
            
            # If only one file was uploaded and it succeeded, redirect to it directly for better UX
            if len(files) == 1 and success_count == 1 and last_upload_id:
                return redirect('view_results', upload_id=last_upload_id)
            
            # Otherwise redirect back to upload page (to see the list)
            return redirect('upload_marksheet')
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
