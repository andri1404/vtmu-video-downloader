// DOM Elements
const videoUrlInput = document.getElementById('videoUrl');
const getInfoBtn = document.getElementById('getInfoBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const errorMessage = document.getElementById('errorMessage');
const videoInfo = document.getElementById('videoInfo');
const videoThumbnail = document.getElementById('videoThumbnail');
const videoTitle = document.getElementById('videoTitle');
const videoUploader = document.getElementById('videoUploader');
const videoViews = document.getElementById('videoViews');
const videoDuration = document.getElementById('videoDuration');
const videoPlatform = document.getElementById('videoPlatform');
const formatList = document.getElementById('formatList');
const downloadProgress = document.getElementById('downloadProgress');

let currentVideoUrl = '';

// Event Listeners
getInfoBtn.addEventListener('click', getVideoInfo);
videoUrlInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        getVideoInfo();
    }
});

// Get Video Info with Auto-Retry
async function getVideoInfo() {
    const url = videoUrlInput.value.trim();

    if (!url) {
        showToast('Masukkan URL video terlebih dahulu!', 'warning');
        videoUrlInput.focus();
        return;
    }

    // Validate URL format
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
        showToast('URL tidak valid! Pastikan URL dimulai dengan http:// atau https://', 'error');
        return;
    }

    currentVideoUrl = url;
    hideError();
    hideVideoInfo();

    // Show loading skeleton
    showLoadingSkeleton();

    let retryCount = 0;
    const maxRetries = 2;

    async function attemptFetch() {
        try {
            const response = await fetch('/api/get-info', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Gagal mendapatkan informasi video');
            }

            hideLoadingSkeleton();
            displayVideoInfo(data);
            showToast('Informasi video berhasil dimuat!', 'success');

        } catch (error) {
            retryCount++;

            if (retryCount < maxRetries) {
                showToast(`Gagal mengambil info, mencoba lagi (${retryCount}/${maxRetries})...`, 'warning');
                await new Promise(resolve => setTimeout(resolve, 1500));
                return await attemptFetch();
            } else {
                hideLoadingSkeleton();
                showError(error.message);
                showToast(error.message, 'error');
            }
        }
    }

    await attemptFetch();
}

// Display Video Info
function displayVideoInfo(data) {
    // Set thumbnail and details
    videoThumbnail.src = data.thumbnail;
    videoTitle.textContent = data.title;
    videoUploader.textContent = data.uploader;
    videoPlatform.textContent = data.platform;

    // Clear previous formats
    formatList.innerHTML = '';

    // Add format options with enhanced styling
    data.formats.forEach((format, index) => {
        const formatItem = document.createElement('div');
        formatItem.className = 'format-item';

        // Determine quality type for styling and icons
        let qualityType = 'low';
        let icon = '📱'; // Default mobile icon for low quality
        let showBadge = false;

        if (format.quality.toLowerCase().includes('best')) {
            qualityType = 'best';
            icon = '👑';
            showBadge = true; // Show RECOMMENDED badge
        } else if (format.quality.toLowerCase().includes('720')) {
            qualityType = 'hd';
            icon = '🎬';
        } else if (format.quality.toLowerCase().includes('480')) {
            qualityType = 'sd';
            icon = '📺';
        } else if (format.quality.toLowerCase().includes('360')) {
            qualityType = 'low';
            icon = '📱';
        } else if (format.quality.toLowerCase().includes('audio') || format.quality.toLowerCase().includes('mp3')) {
            qualityType = 'audio';
            icon = '🎵';
        }

        // Set data attribute for CSS styling
        formatItem.setAttribute('data-quality', qualityType);

        // Store format data in data attributes
        formatItem.setAttribute('data-format-quality', format.quality);
        formatItem.setAttribute('data-format-id', format.format_id);

        // Create HTML with badge, icon, quality label, and filesize
        formatItem.innerHTML = `
            ${showBadge ? '<div class="format-badge">RECOMMENDED</div>' : ''}
            <div class="format-icon-wrapper">
                <div class="format-icon">${icon}</div>
            </div>
            <div class="format-quality">${format.quality}</div>
            ${format.filesize ? `<div class="format-filesize">${formatFileSize(format.filesize)}</div>` : '<div class="format-filesize">Size: Auto</div>'}
            <button class="btn btn-download" data-action="download">
                <i class="fas fa-download"></i>
                <span>Download</span>
            </button>
        `;

        // Add click event to download button
        const downloadBtn = formatItem.querySelector('.btn-download');
        downloadBtn.addEventListener('click', function(e) {
            e.stopPropagation(); // Prevent card selection
            const quality = formatItem.getAttribute('data-format-quality');
            const formatId = formatItem.getAttribute('data-format-id');
            downloadVideo(quality, formatId, e);
        });

        // Add click event to select card
        formatItem.addEventListener('click', function(e) {
            // Don't select if clicking the download button
            if (e.target.closest('.btn-download')) return;

            // Remove selected class from all cards
            document.querySelectorAll('.format-item').forEach(item => {
                item.classList.remove('selected');
            });

            // Add selected class to clicked card
            this.classList.add('selected');
        });

        formatList.appendChild(formatItem);
    });

    showVideoInfo();
}

// Download Video with Auto-Retry and Better Error Handling
async function downloadVideo(quality, format_id, event) {
    const button = event.target.closest('button');
    const originalHTML = button.innerHTML;

    // Disable button during download
    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Memproses...';

    // Show toast notification
    showToast('Memulai download...', 'info');

    // Store data in sessionStorage for download page
    const downloadData = {
        url: currentVideoUrl,
        quality: quality,
        format_id: format_id,
        video_title: videoTitle.textContent,
        thumbnail: videoThumbnail.src
    };

    sessionStorage.setItem('downloadData', JSON.stringify(downloadData));

    // Redirect to download page
    showToast('Redirecting ke halaman download...', 'success');
    setTimeout(() => {
        window.location.href = '/downloading';
    }, 500);
}

// Show Detailed Error with Suggestions
function showDetailedError(errorMsg, quality) {
    const suggestions = [];

    // Analyze error and provide suggestions
    if (errorMsg.includes('403') || errorMsg.includes('forbidden')) {
        suggestions.push('Video ini mungkin dilindungi atau tidak bisa didownload');
        suggestions.push('Coba gunakan kualitas yang lebih rendah');
        suggestions.push('Coba copy URL lagi dari browser');
    } else if (errorMsg.includes('404') || errorMsg.includes('not found')) {
        suggestions.push('URL video mungkin sudah expired atau dihapus');
        suggestions.push('Coba refresh halaman dan paste URL lagi');
    } else if (errorMsg.includes('timeout')) {
        suggestions.push('Koneksi terlalu lambat');
        suggestions.push('Coba gunakan kualitas yang lebih rendah');
        suggestions.push('Periksa koneksi internet Anda');
    } else {
        suggestions.push('Coba gunakan format atau kualitas yang berbeda');
        suggestions.push('Pastikan URL video valid dan masih aktif');
        suggestions.push('Refresh halaman dan coba lagi');
    }

    // Create error modal
    const modal = document.createElement('div');
    modal.className = 'error-modal';
    modal.innerHTML = `
        <div class="error-modal-content">
            <div class="error-modal-header">
                <i class="fas fa-exclamation-triangle"></i>
                <h3>Download Gagal</h3>
            </div>
            <div class="error-modal-body">
                <p class="error-message-text">${errorMsg}</p>
                <div class="error-suggestions">
                    <h4>Saran:</h4>
                    <ul>
                        ${suggestions.map(s => `<li><i class="fas fa-lightbulb"></i> ${s}</li>`).join('')}
                    </ul>
                </div>
            </div>
            <div class="error-modal-footer">
                <button class="btn btn-primary" onclick="this.closest('.error-modal').remove()">
                    <i class="fas fa-check"></i> Mengerti
                </button>
            </div>
        </div>
    `;

    document.body.appendChild(modal);

    // Auto-remove after 10 seconds
    setTimeout(() => {
        if (document.body.contains(modal)) {
            modal.remove();
        }
    }, 10000);
}

// Toast Notification System
function showToast(message, type = 'info') {
    // Remove existing toasts of same type
    const existingToasts = document.querySelectorAll(`.toast.${type}`);
    existingToasts.forEach(toast => toast.remove());

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;

    const icons = {
        success: 'fa-check-circle',
        error: 'fa-exclamation-circle',
        warning: 'fa-exclamation-triangle',
        info: 'fa-info-circle'
    };

    toast.innerHTML = `
        <i class="fas ${icons[type]}"></i>
        <span>${message}</span>
    `;

    document.body.appendChild(toast);

    // Animate in
    setTimeout(() => toast.classList.add('show'), 100);

    // Auto-remove after 5 seconds (10 seconds for errors)
    const duration = type === 'error' ? 10000 : 5000;
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

// Helper Functions
function showLoading() {
    loadingSpinner.classList.remove('hidden');
}

function hideLoading() {
    loadingSpinner.classList.add('hidden');
}

function showLoadingSkeleton() {
    // Hide error and video info
    hideError();
    hideVideoInfo();

    // Create loading skeleton
    const skeleton = document.createElement('div');
    skeleton.id = 'loadingSkeleton';
    skeleton.className = 'loading-skeleton';
    skeleton.innerHTML = `
        <div class="skeleton-header">
            <div class="skeleton-thumbnail"></div>
            <div class="skeleton-details">
                <div class="skeleton-line skeleton-title"></div>
                <div class="skeleton-line skeleton-text"></div>
                <div class="skeleton-line skeleton-text short"></div>
            </div>
        </div>
        <div class="skeleton-formats">
            <div class="skeleton-format-item"></div>
            <div class="skeleton-format-item"></div>
            <div class="skeleton-format-item"></div>
            <div class="skeleton-format-item"></div>
        </div>
        <div class="skeleton-loading-text">
            <i class="fas fa-spinner fa-spin"></i>
            Mengambil informasi video...
        </div>
    `;

    // Insert after download section
    const downloadSection = document.querySelector('.download-section');
    downloadSection.after(skeleton);
}

function hideLoadingSkeleton() {
    const skeleton = document.getElementById('loadingSkeleton');
    if (skeleton) {
        skeleton.remove();
    }
}

function showError(message, type = 'error') {
    errorMessage.textContent = message;
    errorMessage.classList.remove('hidden');
    if (type === 'success') {
        errorMessage.style.background = 'rgba(16, 185, 129, 0.1)';
        errorMessage.style.borderColor = '#10b981';
        errorMessage.style.color = '#10b981';
    } else {
        errorMessage.style.background = 'rgba(239, 68, 68, 0.1)';
        errorMessage.style.borderColor = '#ef4444';
        errorMessage.style.color = '#ef4444';
    }
}

function hideError() {
    errorMessage.classList.add('hidden');
}

function showVideoInfo() {
    videoInfo.classList.remove('hidden');
}

function hideVideoInfo() {
    videoInfo.classList.add('hidden');
}

function showDownloadProgress() {
    downloadProgress.classList.remove('hidden');
}

function hideDownloadProgress() {
    downloadProgress.classList.add('hidden');
}

function formatNumber(num) {
    if (!num) return '0';
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    }
    if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

function formatDuration(seconds) {
    if (!seconds) return '0:00';
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;

    if (hours > 0) {
        return `${hours}:${minutes.toString().padStart(2, '0')}:${secs
            .toString()
            .padStart(2, '0')}`;
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
}

function formatFileSize(bytes) {
    if (!bytes) return 'Unknown';
    if (bytes >= 1073741824) {
        return (bytes / 1073741824).toFixed(2) + ' GB';
    }
    if (bytes >= 1048576) {
        return (bytes / 1048576).toFixed(2) + ' MB';
    }
    if (bytes >= 1024) {
        return (bytes / 1024).toFixed(2) + ' KB';
    }
    return bytes + ' B';
}

// Auto-focus on load
window.addEventListener('load', () => {
    videoUrlInput.focus();
});

// Navbar toggle for mobile
const navToggle = document.getElementById('navToggle');
const navMenu = document.getElementById('navMenu');

if (navToggle) {
    navToggle.addEventListener('click', () => {
        navToggle.classList.toggle('active');
        navMenu.classList.toggle('active');
    });

    // Close menu when clicking nav link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            navToggle.classList.remove('active');
            navMenu.classList.remove('active');
        });
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
            navToggle.classList.remove('active');
            navMenu.classList.remove('active');
        }
    });
}
