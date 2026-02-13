const fileInput = document.getElementById('fileInput');
const uploadBox = document.getElementById('uploadBox');
const fileInfo = document.getElementById('fileInfo');
const progressSection = document.getElementById('progressSection');
const resultsSection = document.getElementById('resultsSection');
const errorMessage = document.getElementById('errorMessage');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const downloadBtn = document.getElementById('downloadBtn');

let currentSessionId = null;

// Drag and drop handlers
uploadBox.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadBox.classList.add('dragover');
});

uploadBox.addEventListener('dragleave', () => {
    uploadBox.classList.remove('dragover');
});

uploadBox.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadBox.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

uploadBox.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

function handleFile(file) {
    // Validate file type
    const validTypes = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                       'application/vnd.ms-excel'];
    const validExtensions = ['.xlsx', '.xls'];
    
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!validExtensions.includes(fileExtension)) {
        showError('Please upload a valid Excel file (.xlsx or .xls)');
        return;
    }

    // Show file info
    fileInfo.textContent = `Selected: ${file.name} (${formatFileSize(file.size)})`;
    
    // Hide previous results/errors
    resultsSection.style.display = 'none';
    errorMessage.style.display = 'none';
    
    // Upload file
    uploadFile(file);
}

function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    // Show progress
    progressSection.style.display = 'block';
    progressFill.style.width = '0%';
    progressText.textContent = 'Uploading and processing...';

    // Simulate progress (since we can't track actual progress easily)
    let progress = 0;
    const progressInterval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress > 90) progress = 90;
        progressFill.style.width = progress + '%';
    }, 200);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        clearInterval(progressInterval);
        progressFill.style.width = '100%';
        progressText.textContent = 'Complete!';

        setTimeout(() => {
            if (data.success) {
                showResults(data);
            } else {
                showError(data.error || 'An error occurred while processing the file');
            }
            progressSection.style.display = 'none';
        }, 500);
    })
    .catch(error => {
        clearInterval(progressInterval);
        progressSection.style.display = 'none';
        showError('Network error: ' + error.message);
    });
}

function showResults(data) {
    document.getElementById('totalRows').textContent = data.total_rows || 0;
    document.getElementById('successfulCount').textContent = data.successful || 0;
    document.getElementById('failedCount').textContent = data.failed || 0;

    // Extract session ID from download URL
    const match = data.zip_url.match(/\/download\/([^\/]+)/);
    if (match) {
        currentSessionId = match[1];
    }

    // Show errors if any
    if (data.errors && data.errors.length > 0) {
        const errorList = document.getElementById('errorList');
        const errorItems = document.getElementById('errorItems');
        errorItems.innerHTML = '';
        data.errors.forEach(error => {
            const li = document.createElement('li');
            li.textContent = error;
            errorItems.appendChild(li);
        });
        errorList.style.display = 'block';
    } else {
        document.getElementById('errorList').style.display = 'none';
    }

    resultsSection.style.display = 'block';
    errorMessage.style.display = 'none';
}

function showError(message) {
    document.getElementById('errorText').textContent = message;
    errorMessage.style.display = 'block';
    resultsSection.style.display = 'none';
    progressSection.style.display = 'none';
}

downloadBtn.addEventListener('click', () => {
    if (currentSessionId) {
        window.location.href = `/download/${currentSessionId}/zip`;
    }
});

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}
