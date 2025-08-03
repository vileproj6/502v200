// ARQV30 Enhanced v2.0 - File Upload Manager
// Handles intelligent file uploads and processing

class FileUploadManager {
    constructor() {
        this.uploadedFiles = [];
        this.maxFileSize = 16 * 1024 * 1024; // 16MB
        this.allowedTypes = [
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'text/csv',
            'text/plain',
            'application/json'
        ];
        
        this.init();
    }
    
    init() {
        this.setupUploadArea();
        this.setupFileInput();
        console.log('📎 File Upload Manager inicializado');
    }
    
    setupUploadArea() {
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        
        if (!uploadArea || !fileInput) return;
        
        // Drag and drop events
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        
        uploadArea.addEventListener('dragleave', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            
            const files = Array.from(e.dataTransfer.files);
            this.handleFiles(files);
        });
        
        // Click to upload
        uploadArea.addEventListener('click', () => {
            fileInput.click();
        });
    }
    
    setupFileInput() {
        const fileInput = document.getElementById('fileInput');
        if (!fileInput) return;
        
        fileInput.addEventListener('change', (e) => {
            const files = Array.from(e.target.files);
            this.handleFiles(files);
        });
    }
    
    handleFiles(files) {
        files.forEach(file => {
            if (this.validateFile(file)) {
                this.uploadFile(file);
            }
        });
    }
    
    validateFile(file) {
        // Check file size
        if (file.size > this.maxFileSize) {
            this.showError(`Arquivo muito grande: ${file.name} (máximo 16MB)`);
            return false;
        }
        
        // Check file type
        if (!this.allowedTypes.includes(file.type)) {
            this.showError(`Tipo de arquivo não suportado: ${file.name}`);
            return false;
        }
        
        // Check if already uploaded
        if (this.uploadedFiles.some(f => f.name === file.name && f.size === file.size)) {
            this.showError(`Arquivo já foi enviado: ${file.name}`);
            return false;
        }
        
        return true;
    }
    
    async uploadFile(file) {
        const fileId = this.generateFileId();
        const fileInfo = {
            id: fileId,
            name: file.name,
            size: file.size,
            type: file.type,
            status: 'uploading',
            progress: 0
        };
        
        this.uploadedFiles.push(fileInfo);
        this.renderFileItem(fileInfo);
        
        try {
            // Create FormData
            const formData = new FormData();
            formData.append('file', file);
            formData.append('session_id', this.getSessionId());
            
            // Upload with progress
            const result = await this.uploadWithProgress(formData, fileId);
            
            if (result.success) {
                fileInfo.status = 'completed';
                fileInfo.progress = 100;
                fileInfo.processed_content = result.content_preview;
                fileInfo.content_type = result.content_type;
                
                this.updateFileItem(fileInfo);
                this.showSuccess(`Arquivo processado: ${file.name}`);
                
                console.log('✅ Arquivo processado:', result);
            } else {
                throw new Error(result.error || 'Erro no processamento');
            }
            
        } catch (error) {
            console.error('Erro no upload:', error);
            fileInfo.status = 'error';
            fileInfo.error = error.message;
            this.updateFileItem(fileInfo);
            this.showError(`Erro ao processar ${file.name}: ${error.message}`);
        }
    }
    
    async uploadWithProgress(formData, fileId) {
        return new Promise((resolve, reject) => {
            const xhr = new XMLHttpRequest();
            
            // Progress tracking
            xhr.upload.addEventListener('progress', (e) => {
                if (e.lengthComputable) {
                    const progress = (e.loaded / e.total) * 100;
                    this.updateFileProgress(fileId, progress);
                }
            });
            
            // Response handling
            xhr.addEventListener('load', () => {
                try {
                    const result = JSON.parse(xhr.responseText);
                    if (xhr.status === 200) {
                        resolve(result);
                    } else {
                        reject(new Error(result.error || `HTTP ${xhr.status}`));
                    }
                } catch (e) {
                    reject(new Error('Resposta inválida do servidor'));
                }
            });
            
            xhr.addEventListener('error', () => {
                reject(new Error('Erro de rede'));
            });
            
            // Send request
            xhr.open('POST', '/api/upload');
            xhr.send(formData);
        });
    }
    
    renderFileItem(fileInfo) {
        const container = document.getElementById('uploadedFiles');
        if (!container) return;
        
        const fileElement = document.createElement('div');
        fileElement.className = 'file-item';
        fileElement.id = `file-${fileInfo.id}`;
        
        this.updateFileItemHTML(fileElement, fileInfo);
        container.appendChild(fileElement);
    }
    
    updateFileItem(fileInfo) {
        const fileElement = document.getElementById(`file-${fileInfo.id}`);
        if (fileElement) {
            this.updateFileItemHTML(fileElement, fileInfo);
        }
    }
    
    updateFileItemHTML(element, fileInfo) {
        const statusIcon = this.getStatusIcon(fileInfo.status);
        const statusColor = this.getStatusColor(fileInfo.status);
        
        element.innerHTML = `
            <div class="file-info">
                <i class="${statusIcon}" style="color: ${statusColor}"></i>
                <div>
                    <div class="file-name">${fileInfo.name}</div>
                    <div class="file-size">${this.formatFileSize(fileInfo.size)}</div>
                    ${fileInfo.content_type ? `<div class="file-type">Tipo: ${fileInfo.content_type}</div>` : ''}
                </div>
            </div>
            <div class="file-actions">
                <div class="file-status" style="color: ${statusColor}">
                    ${this.getStatusText(fileInfo.status)}
                </div>
                ${fileInfo.status === 'uploading' ? `
                    <div class="file-progress">
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${fileInfo.progress}%"></div>
                        </div>
                    </div>
                ` : ''}
                ${fileInfo.error ? `<div class="file-error">${fileInfo.error}</div>` : ''}
                <button class="file-remove" onclick="uploadManager.removeFile('${fileInfo.id}')" 
                        ${fileInfo.status === 'uploading' ? 'disabled' : ''}>
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
    }
    
    updateFileProgress(fileId, progress) {
        const fileInfo = this.uploadedFiles.find(f => f.id === fileId);
        if (fileInfo) {
            fileInfo.progress = progress;
            
            const progressFill = document.querySelector(`#file-${fileId} .progress-fill`);
            if (progressFill) {
                progressFill.style.width = `${progress}%`;
            }
        }
    }
    
    removeFile(fileId) {
        // Remove from array
        this.uploadedFiles = this.uploadedFiles.filter(f => f.id !== fileId);
        
        // Remove from DOM
        const fileElement = document.getElementById(`file-${fileId}`);
        if (fileElement) {
            fileElement.remove();
        }
        
        console.log('🗑️ Arquivo removido:', fileId);
    }
    
    getUploadedFiles() {
        return this.uploadedFiles.filter(f => f.status === 'completed');
    }
    
    getSessionId() {
        let sessionId = localStorage.getItem('arqv30_session_id');
        if (!sessionId) {
            sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('arqv30_session_id', sessionId);
        }
        return sessionId;
    }
    
    generateFileId() {
        return 'file_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    getStatusIcon(status) {
        const icons = {
            'uploading': 'fas fa-spinner fa-spin',
            'completed': 'fas fa-check-circle',
            'error': 'fas fa-exclamation-circle'
        };
        return icons[status] || 'fas fa-file';
    }
    
    getStatusColor(status) {
        const colors = {
            'uploading': '#ffd700',
            'completed': '#06ffa5',
            'error': '#ff6b6b'
        };
        return colors[status] || '#b8bcc8';
    }
    
    getStatusText(status) {
        const texts = {
            'uploading': 'Processando...',
            'completed': 'Concluído',
            'error': 'Erro'
        };
        return texts[status] || 'Desconhecido';
    }
    
    showError(message) {
        if (window.app) {
            window.app.showAlert(message, 'error');
        } else {
            console.error(message);
        }
    }
    
    showSuccess(message) {
        if (window.app) {
            window.app.showAlert(message, 'success');
        } else {
            console.log(message);
        }
    }
    
    // Get processed content for analysis
    getProcessedContent() {
        const completedFiles = this.getUploadedFiles();
        
        if (completedFiles.length === 0) {
            return null;
        }
        
        return {
            files_count: completedFiles.length,
            files_info: completedFiles.map(f => ({
                name: f.name,
                type: f.content_type,
                size: f.size,
                content_preview: f.processed_content
            })),
            combined_content: completedFiles
                .map(f => f.processed_content)
                .filter(content => content)
                .join('\n\n--- ARQUIVO SEPARADOR ---\n\n')
        };
    }
    
    // Clear all files
    clearAllFiles() {
        this.uploadedFiles = [];
        const container = document.getElementById('uploadedFiles');
        if (container) {
            container.innerHTML = '';
        }
        console.log('🧹 Todos os arquivos removidos');
    }
}

// Initialize upload manager
document.addEventListener('DOMContentLoaded', () => {
    window.uploadManager = new FileUploadManager();
});