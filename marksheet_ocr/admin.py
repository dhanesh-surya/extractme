from django.contrib import admin
from .models import MarksheetUpload, Student, Subject, Mark


@admin.register(MarksheetUpload)
class MarksheetUploadAdmin(admin.ModelAdmin):
    list_display = ['id', 'uploaded_at', 'status']
    list_filter = ['status', 'uploaded_at']
    readonly_fields = ['uploaded_at']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['roll_number', 'name', 'father_name', 'upload', 'get_percentage', 'get_result_status']
    list_filter = ['upload']
    search_fields = ['roll_number', 'name', 'father_name']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']
    search_fields = ['code', 'name']


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'theory_ese', 'theory_internal', 'practical_marks', 'practical_internal', 'get_total_marks']
    list_filter = ['subject']
    search_fields = ['student__roll_number', 'student__name', 'subject__name']
