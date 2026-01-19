// Upload functionality
document.addEventListener('DOMContentLoaded', function () {
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('marksheet-upload');
    const fileInfo = document.getElementById('file-info');
    const fileName = document.getElementById('file-name');
    const removeFileBtn = document.getElementById('remove-file');
    const imagePreview = document.getElementById('image-preview');
    const previewImg = document.getElementById('preview-img');
    const uploadForm = document.getElementById('upload-form');
    const submitBtn = document.getElementById('submit-btn');
    const processingIndicator = document.getElementById('processing-indicator');

    if (!uploadArea || !fileInput) return;

    // Drag and drop events
    uploadArea.addEventListener('dragover', function (e) {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', function (e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', function (e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            handleFileSelect(files[0]);
        }
    });

    // File input change
    fileInput.addEventListener('change', function (e) {
        if (this.files.length > 0) {
            handleFileSelect(this.files[0]);
        }
    });

    // Remove file button
    if (removeFileBtn) {
        removeFileBtn.addEventListener('click', function () {
            fileInput.value = '';
            fileInfo.style.display = 'none';
            imagePreview.style.display = 'none';
        });
    }

    // Handle file selection
    function handleFileSelect(file) {
        // Validate file type
        const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/bmp', 'image/tiff'];
        if (!validTypes.includes(file.type)) {
            alert('Please select a valid image file (JPEG, PNG, BMP, or TIFF)');
            fileInput.value = '';
            return;
        }

        // Validate file size (10MB max)
        if (file.size > 10 * 1024 * 1024) {
            alert('File size must be less than 10MB');
            fileInput.value = '';
            return;
        }

        // Show file info
        fileName.textContent = file.name;
        fileInfo.style.display = 'inline-block';

        // Show image preview
        const reader = new FileReader();
        reader.onload = function (e) {
            previewImg.src = e.target.result;
            imagePreview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }

    // Form submission
    if (uploadForm) {
        uploadForm.addEventListener('submit', function (e) {
            if (!fileInput.files || fileInput.files.length === 0) {
                e.preventDefault();
                alert('Please select a marksheet image to upload');
                return;
            }

            // Show processing indicator
            submitBtn.disabled = true;
            processingIndicator.style.display = 'block';
        });
    }
});
