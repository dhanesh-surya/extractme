from django import forms
from .models import MarksheetUpload


class MarksheetUploadForm(forms.ModelForm):
    """Form for uploading marksheet images"""
    
    class Meta:
        model = MarksheetUpload
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'id': 'marksheet-upload',
                'multiple': True
            })
        }
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        
        if image:
            # Validate file size (max 10MB)
            if image.size > 10 * 1024 * 1024:
                raise forms.ValidationError('Image file size must be less than 10MB')
            
            # Validate file type
            valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
            file_extension = image.name.lower().split('.')[-1]
            if f'.{file_extension}' not in valid_extensions:
                raise forms.ValidationError(
                    f'Invalid file type. Allowed types: {", ".join(valid_extensions)}'
                )
        
        return image
