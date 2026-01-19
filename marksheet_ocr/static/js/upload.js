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
            fileInput.files = files; // Assign dropped files to input
            handleFilesSelect(files);
        }
    });

    // File input change
    fileInput.addEventListener('change', function (e) {
        if (this.files.length > 0) {
            handleFilesSelect(this.files);
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

    // Handle files selection
    function handleFilesSelect(files) {
        // Validate file count
        if (files.length > 5) {
            alert('Maximum 5 files allowed per upload.');
            fileInput.value = '';
            fileInfo.style.display = 'none';
            imagePreview.style.display = 'none';
            return;
        }

        const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/bmp', 'image/tiff'];
        let validFiles = true;
        let fileNames = [];

        // Validate each file
        for (let i = 0; i < files.length; i++) {
            const file = files[i];

            if (!validTypes.includes(file.type)) {
                alert(`File "${file.name}" is not a valid image. Please select JPEG, PNG, BMP, or TIFF.`);
                validFiles = false;
                break;
            }

            if (file.size > 10 * 1024 * 1024) {
                alert(`File "${file.name}" exceeds 10MB limit.`);
                validFiles = false;
                break;
            }

            fileNames.push(file.name);
        }

        if (!validFiles) {
            fileInput.value = '';
            return;
        }

        // Show file info
        if (files.length === 1) {
            fileName.textContent = files[0].name;
            // Show image preview for single file
            const reader = new FileReader();
            reader.onload = function (e) {
                previewImg.src = e.target.result;
                imagePreview.style.display = 'block';
            };
            reader.readAsDataURL(files[0]);
        } else {
            fileName.textContent = `${files.length} files selected: ${fileNames.join(', ')}`;
            // Hide preview for multiple files to save space
            imagePreview.style.display = 'none';
        }

        fileInfo.style.display = 'inline-block';
    }

    // Form submission
    if (uploadForm) {
        uploadForm.addEventListener('submit', function (e) {
            if (!fileInput.files || fileInput.files.length === 0) {
                e.preventDefault();
                alert('Please select marksheet image(s) to upload');
                return;
            }

            // Show processing indicator
            submitBtn.disabled = true;
            processingIndicator.style.display = 'block';
        });
    }
});
