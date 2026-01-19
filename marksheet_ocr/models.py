from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import os


class MarksheetUpload(models.Model):
    """Model to store uploaded marksheet images"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    image = models.ImageField(upload_to='marksheets/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"Marksheet {self.id} - {self.status}"


class Student(models.Model):
    """Model to store student information"""
    upload = models.ForeignKey(MarksheetUpload, on_delete=models.CASCADE, related_name='students')
    roll_number = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    father_name = models.CharField(max_length=200, blank=True)
    mother_name = models.CharField(max_length=200, blank=True)
    enrollment_number = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['roll_number']
    
    def __str__(self):
        return f"{self.roll_number} - {self.name}"
    
    def get_total_marks(self):
        """Calculate total marks across all subjects"""
        total = 0
        for mark in self.marks.all():
            total += mark.get_total_marks()
        return total
    
    def get_percentage(self):
        """Calculate percentage"""
        marks = self.marks.all()
        if not marks:
            return 0
        
        total_obtained = self.get_total_marks()
        total_maximum = sum(mark.get_maximum_marks() for mark in marks)
        
        if total_maximum == 0:
            return 0
        
        return round((total_obtained / total_maximum) * 100, 2)
    
    def get_result_status(self):
        """Determine pass/fail status"""
        marks = self.marks.all()
        if not marks:
            return 'N/A'
        
        # Check if any subject has failing marks
        for mark in marks:
            if mark.is_failed():
                return 'FAIL'
        
        percentage = self.get_percentage()
        if percentage >= 75:
            return 'PASS FIRST'
        elif percentage >= 60:
            return 'PASS SECOND'
        elif percentage >= 45:
            return 'PASS THIRD'
        elif percentage >= 33:
            return 'PASS'
        else:
            return 'FAIL'


class Subject(models.Model):
    """Model to store subject information"""
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    
    class Meta:
        unique_together = ['code', 'name']
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Mark(models.Model):
    """Model to store marks for each subject"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    
    # Theory marks
    theory_ese = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True,
        help_text="Theory External Semester Examination marks"
    )
    theory_internal = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True,
        help_text="Theory Internal marks"
    )
    
    # Practical marks
    practical_marks = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True,
        help_text="Practical examination marks"
    )
    practical_internal = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True,
        help_text="Practical Internal marks"
    )
    
    class Meta:
        unique_together = ['student', 'subject']
    
    def __str__(self):
        return f"{self.student.roll_number} - {self.subject.code}"
    
    def get_theory_total(self):
        """Calculate total theory marks"""
        theory_ese = self.theory_ese or 0
        theory_internal = self.theory_internal or 0
        return theory_ese + theory_internal
    
    def get_practical_total(self):
        """Calculate total practical marks"""
        practical = self.practical_marks or 0
        practical_internal = self.practical_internal or 0
        return practical + practical_internal
    
    def get_total_marks(self):
        """Calculate total marks for this subject"""
        return self.get_theory_total() + self.get_practical_total()
    
    def get_maximum_marks(self):
        """Get maximum possible marks (assuming 100 for each component)"""
        max_marks = 0
        if self.theory_ese is not None or self.theory_internal is not None:
            max_marks += 100  # Theory total
        if self.practical_marks is not None or self.practical_internal is not None:
            max_marks += 100  # Practical total
        return max_marks
    
    def is_failed(self):
        """Check if student failed in this subject"""
        # Minimum passing marks is typically 33% in each component
        if self.theory_ese is not None and self.theory_ese < 33:
            return True
        if self.practical_marks is not None and self.practical_marks < 33:
            return True
        return False
