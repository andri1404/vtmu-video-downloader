from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp
import os
import uuid
from pathlib import Path
import json
import subprocess
import sys
from datetime import datetime, timedelta
import logging
import time
from collections import defaultdict
from functools import wraps

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ============================================
# ANTI-SCRAPING & RATE LIMITING
# ============================================

# Track requests per IP
request_tracker = defaultdict(list)
blocked_ips = set()

# Rate limiting configuration
RATE_LIMIT_WINDOW = 60  # seconds
MAX_REQUESTS_PER_WINDOW = 10  # max requests per IP in window
MAX_REQUESTS_PER_HOUR = 50  # max requests per IP per hour
DOWNLOAD_LIMIT_PER_HOUR = 20  # max downloads per IP per hour
BLOCK_DURATION = 300  # 5 minutes block for abusers

def get_client_ip():
    """Get real client IP even behind proxy"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    return request.remote_addr

def is_suspicious_request():
    """Detect suspicious bot/scraper behavior"""
    user_agent = request.headers.get('User-Agent', '').lower()

    # Common bot signatures
    bot_signatures = [
        'bot', 'crawler', 'spider', 'scraper', 'wget', 'curl',
        'python-requests', 'java', 'perl', 'go-http-client'
    ]

    # Check if it's a known bot (but allow legitimate ones)
    for signature in bot_signatures:
        if signature in user_agent:
            # Allow some legitimate bots but log them
            if signature not in ['googlebot', 'bingbot']:
                logger.warning(f"Suspicious user agent detected: {user_agent}")
                return True

    # Check for missing common headers
    if not request.headers.get('Accept-Language'):
        return True

    return False

def rate_limit_decorator(max_per_window=MAX_REQUESTS_PER_WINDOW):
    """Rate limiting decorator"""
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            ip = get_client_ip()
            current_time = time.time()

            # Check if IP is blocked
            if ip in blocked_ips:
                logger.warning(f"Blocked IP attempted access: {ip}")
                return jsonify({
                    'error': 'Terlalu banyak permintaan. Silakan coba lagi nanti.',
                    'retry_after': BLOCK_DURATION
                }), 429

            # Clean old requests (older than window)
            request_tracker[ip] = [
                req_time for req_time in request_tracker[ip]
                if current_time - req_time < RATE_LIMIT_WINDOW
            ]

            # Check rate limit
            if len(request_tracker[ip]) >= max_per_window:
                logger.warning(f"Rate limit exceeded for IP: {ip}")
                # Block IP temporarily
                blocked_ips.add(ip)
                # Schedule unblock after BLOCK_DURATION
                return jsonify({
                    'error': 'Terlalu banyak permintaan. Anda telah diblokir sementara.',
                    'retry_after': BLOCK_DURATION
                }), 429

            # Check hourly limit
            hourly_requests = [
                req_time for req_time in request_tracker[ip]
                if current_time - req_time < 3600
            ]
            if len(hourly_requests) >= MAX_REQUESTS_PER_HOUR:
                logger.warning(f"Hourly limit exceeded for IP: {ip}")
                return jsonify({
                    'error': 'Batas permintaan per jam tercapai. Silakan coba lagi nanti.',
                    'retry_after': 3600
                }), 429

            # Check for suspicious behavior
            if is_suspicious_request():
                logger.warning(f"Suspicious request from IP: {ip}")
                return jsonify({
                    'error': 'Request tidak valid. Gunakan browser normal.'
                }), 403

            # Add current request
            request_tracker[ip].append(current_time)

            return f(*args, **kwargs)
        return wrapped
    return decorator

# Cleanup blocked IPs periodically
def cleanup_blocked_ips():
    """This should be called periodically to unblock IPs"""
    current_time = time.time()
    # In production, you'd use a proper scheduler
    # For now, we'll just clear all blocks after some time
    global blocked_ips
    if len(blocked_ips) > 100:  # Prevent memory issues
        blocked_ips.clear()

# Security headers
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'

    # Strict Content Security Policy
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:;"

    # HSTS - Force HTTPS (uncomment when using HTTPS)
    # response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

    # Limited CORS - only for specific origins in production
    response.headers['Access-Control-Allow-Origin'] = '*'  # Change to specific domain in production
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Max-Age'] = '3600'

    return response

# Folder untuk menyimpan download sementara
DOWNLOAD_FOLDER = 'downloads'
Path(DOWNLOAD_FOLDER).mkdir(exist_ok=True)

# Download limits removed - unlimited download
# MAX_FILE_SIZE = None  # No limit
# DOWNLOAD_TIMEOUT = None  # No timeout

# Input validation helpers
def is_valid_url(url):
    """Validate URL to prevent injection attacks"""
    if not url or not isinstance(url, str):
        return False
    # Check URL length
    if len(url) > 2048:
        return False
    # Check if URL starts with http/https
    if not url.startswith(('http://', 'https://')):
        return False
    # Basic sanitization - remove potential harmful characters
    dangerous_chars = ['<', '>', '"', "'", ';', '(', ')', '{', '}']
    if any(char in url for char in dangerous_chars):
        return False
    return True

def sanitize_filename(filename):
    """Sanitize filename to prevent path traversal"""
    # Remove path separators and null bytes
    filename = filename.replace('/', '').replace('\\', '').replace('\0', '')
    # Remove potentially dangerous characters
    dangerous_chars = ['..', '<', '>', '"', '|', '?', '*']
    for char in dangerous_chars:
        filename = filename.replace(char, '')
    return filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/how-to-use')
def how_to_use():
    """Halaman Cara Pakai"""
    return render_template('how-to-use.html')

@app.route('/faq')
def faq():
    """Halaman FAQ"""
    return render_template('faq.html')

@app.route('/downloading')
def downloading_page():
    """Halaman khusus download"""
    return render_template('download.html')

@app.route('/api/get-info', methods=['POST'])
def get_video_info():
    """Mendapatkan informasi video tanpa download"""
    try:
        # Log request for monitoring
        ip = get_client_ip()
        logger.info(f"get-info request from IP: {ip}")

        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({'error': 'URL tidak boleh kosong'}), 400

        # Validate URL for security
        if not is_valid_url(url):
            return jsonify({'error': 'URL tidak valid atau mengandung karakter berbahaya'}), 400

        # Block Facebook URLs (not supported currently)
        if 'facebook.com' in url or 'fb.watch' in url or 'fb.com' in url:
            return jsonify({'error': 'Maaf, Facebook sementara tidak didukung. Silakan gunakan platform lain seperti Instagram, TikTok, atau YouTube.'}), 400

        # Handle TikTok photo/slideshow URLs - convert to video format
        if 'tiktok.com' in url and '/photo/' in url:
            # Remove query parameters
            if '?' in url:
                url = url.split('?')[0]
            # Convert /photo/ to /video/ format
            url = url.replace('/photo/', '/video/')

        # Determine platform for specific handling
        platform = 'unknown'
        if 'instagram.com' in url:
            platform = 'instagram'
        elif 'tiktok.com' in url:
            platform = 'tiktok'
        elif 'youtube.com' in url or 'youtu.be' in url:
            platform = 'youtube'

        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'ignoreerrors': False,
            'no_color': True,
            # Force IPv4
            'source_address': '0.0.0.0',
            # Enhanced headers
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
            },
            # Platform-specific configurations
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web', 'ios'],
                    'skip': ['hls', 'dash'],
                },
                'tiktok': {
                    'api_hostname': 'api16-normal-c-useast1a.tiktokv.com',
                    'app_version': '34.1.2',
                    'manifest_app_version': '341',
                    'webpage_download': True,
                },
                'instagram': {
                    'api': 'graphql',  # Use GraphQL API
                },
            },
            # Retry and timeout settings
            'retries': 15,
            'fragment_retries': 15,
            'socket_timeout': 30,
            'nocheckcertificate': True,
            'prefer_insecure': False,
        }

        # Add platform-specific Referer
        if platform == 'instagram':
            ydl_opts['http_headers']['Referer'] = 'https://www.instagram.com/'
            ydl_opts['http_headers']['X-IG-App-ID'] = '936619743392459'

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            # Check if info is valid
            if not info:
                return jsonify({'error': 'Tidak dapat mengambil informasi video. URL mungkin tidak valid atau tidak didukung.'}), 400

            # Format informasi video
            video_info = {
                'title': info.get('title', 'Unknown'),
                'thumbnail': info.get('thumbnail', '') or info.get('thumbnails', [{}])[0].get('url', ''),
                'duration': info.get('duration', 0),
                'uploader': info.get('uploader', info.get('uploader_id', 'Unknown')),
                'view_count': info.get('view_count', 0) or info.get('like_count', 0),
                'platform': info.get('extractor', 'Unknown'),
                'formats': []
            }

            # Ambil format yang tersedia untuk estimasi ukuran
            available_formats = info.get('formats', [])
            duration = info.get('duration', 0)

            # Format selection yang universal untuk semua platform
            video_info['formats'] = [
                {
                    'quality': 'Best Quality',
                    'ext': 'mp4',
                    'filesize': 0,
                    'format_id': 'bv*+ba/b',
                    'description': 'Kualitas terbaik'
                },
                {
                    'quality': 'HD 720p',
                    'ext': 'mp4',
                    'filesize': 0,
                    'format_id': 'bv*[height<=720]+ba/b[height<=720]/bv*[height<=720]/b',
                    'description': '720p HD'
                },
                {
                    'quality': 'SD 480p',
                    'ext': 'mp4',
                    'filesize': 0,
                    'format_id': 'bv*[height<=480]+ba/b[height<=480]/bv*[height<=480]/b',
                    'description': '480p SD'
                },
                {
                    'quality': 'Low 360p',
                    'ext': 'mp4',
                    'filesize': 0,
                    'format_id': 'bv*[height<=360]+ba/b[height<=360]/bv*[height<=360]/b',
                    'description': '360p'
                },
                {
                    'quality': 'Audio Only (MP3)',
                    'ext': 'mp3',
                    'filesize': 0,
                    'format_id': 'bestaudio',
                    'description': 'MP3 Audio'
                }
            ]

            return jsonify(video_info)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/download', methods=['POST'])
def download_video():
    """Download video dengan kualitas yang dipilih"""
    try:
        # Log request for monitoring
        ip = get_client_ip()
        logger.info(f"download request from IP: {ip}")

        data = request.get_json()
        url = data.get('url')
        quality = data.get('quality', 'Best Quality')
        format_id = data.get('format_id', 'best')

        if not url:
            return jsonify({'error': 'URL tidak boleh kosong'}), 400

        # Validate URL for security
        if not is_valid_url(url):
            return jsonify({'error': 'URL tidak valid atau mengandung karakter berbahaya'}), 400

        # Block Facebook URLs (not supported currently)
        if 'facebook.com' in url or 'fb.watch' in url or 'fb.com' in url:
            return jsonify({'error': 'Maaf, Facebook sementara tidak didukung. Silakan gunakan platform lain seperti Instagram, TikTok, atau YouTube.'}), 400

        # Handle TikTok photo/slideshow URLs - convert to video format
        original_url = url
        if 'tiktok.com' in url and '/photo/' in url:
            # Remove query parameters
            if '?' in url:
                url = url.split('?')[0]
            # Convert /photo/ to /video/ format
            url = url.replace('/photo/', '/video/')

        # Determine platform for specific handling
        platform = 'unknown'
        if 'instagram.com' in url:
            platform = 'instagram'
        elif 'tiktok.com' in url:
            platform = 'tiktok'
        elif 'youtube.com' in url or 'youtu.be' in url:
            platform = 'youtube'

        # Generate unique filename - limit panjang nama
        unique_id = str(uuid.uuid4())[:8]

        # Gunakan template sederhana untuk menghindari nama file terlalu panjang
        output_template = os.path.join(DOWNLOAD_FOLDER, f'{unique_id}.%(ext)s')

        ydl_opts = {
            'format': format_id,
            'outtmpl': output_template,
            'quiet': True,
            'no_warnings': True,
            'ignoreerrors': False,
            'merge_output_format': 'mp4',
            'postprocessor_args': ['-ar', '44100'],
            # Force IPv4
            'source_address': '0.0.0.0',
            # Anti-403 measures - Enhanced
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'Cache-Control': 'max-age=0',
            },
            # Restrict filename untuk avoid nama terlalu panjang
            'restrictfilenames': True,
            # Platform-specific fixes
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web', 'ios'],
                    'skip': ['hls', 'dash']
                },
                'tiktok': {
                    'api_hostname': 'api16-normal-c-useast1a.tiktokv.com',
                    'app_version': '34.1.2',
                    'manifest_app_version': '341',
                    'webpage_download': True,
                },
                'instagram': {
                    'api': 'graphql',
                },
            },
            # Retry options
            'retries': 15,
            'fragment_retries': 15,
            'socket_timeout': 30,
            'skip_unavailable_fragments': True,
            # Additional options
            'nocheckcertificate': True,
            'prefer_insecure': False,
            'geo_bypass': True,
            'age_limit': None,
        }

        # Add platform-specific headers
        if platform == 'instagram':
            ydl_opts['http_headers']['Referer'] = 'https://www.instagram.com/'
            ydl_opts['http_headers']['X-IG-App-ID'] = '936619743392459'

        # Sesuaikan format berdasarkan pilihan
        if quality == 'Audio Only (MP3)':
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        else:
            # Untuk video, gunakan format ID yang sudah ada fallback
            ydl_opts['format'] = format_id
            # Untuk TikTok slideshow/foto, convert ke video
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=True)
            except Exception as extract_error:
                # Handle TikTok slideshow/photo downloads specifically
                if 'tiktok' in url.lower():
                    # Try to find downloaded files in folder
                    downloaded_files = [f for f in os.listdir(DOWNLOAD_FOLDER) if f.startswith(unique_id)]
                    if downloaded_files:
                        filename = os.path.join(DOWNLOAD_FOLDER, downloaded_files[0])
                        actual_size = os.path.getsize(filename) if os.path.exists(filename) else 0

                        return jsonify({
                            'success': True,
                            'filename': os.path.basename(filename),
                            'download_url': f'/download/{os.path.basename(filename)}',
                            'filesize': actual_size
                        })

                return jsonify({'error': f'Gagal mendownload: {str(extract_error)}'}), 400

            # Check if download was successful
            if not info:
                # Even if info is None, check if file was downloaded
                downloaded_files = [f for f in os.listdir(DOWNLOAD_FOLDER) if f.startswith(unique_id)]
                if downloaded_files:
                    filename = os.path.join(DOWNLOAD_FOLDER, downloaded_files[0])
                    actual_size = os.path.getsize(filename) if os.path.exists(filename) else 0

                    return jsonify({
                        'success': True,
                        'filename': os.path.basename(filename),
                        'download_url': f'/download/{os.path.basename(filename)}',
                        'filesize': actual_size
                    })
                else:
                    return jsonify({'error': 'Gagal mendownload video. URL mungkin tidak valid atau tidak didukung.'}), 400

            filename = ydl.prepare_filename(info)

            # Jika audio, file extension berubah jadi .mp3
            if quality == 'Audio Only (MP3)':
                filename = filename.rsplit('.', 1)[0] + '.mp3'

            # Get actual file size
            actual_size = 0
            if os.path.exists(filename):
                actual_size = os.path.getsize(filename)

        return jsonify({
            'success': True,
            'filename': os.path.basename(filename),
            'download_url': f'/download/{os.path.basename(filename)}',
            'filesize': actual_size
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/download/<filename>')
def serve_file(filename):
    """Serve downloaded file"""
    try:
        # Sanitize filename to prevent path traversal attacks
        filename = sanitize_filename(filename)

        # Ensure file is in downloads folder
        file_path = os.path.join(DOWNLOAD_FOLDER, filename)

        # Prevent directory traversal
        if not os.path.abspath(file_path).startswith(os.path.abspath(DOWNLOAD_FOLDER)):
            return jsonify({'error': 'Akses ditolak'}), 403

        # Check if file exists
        if not os.path.exists(file_path):
            return jsonify({'error': 'File tidak ditemukan'}), 404

        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': 'File tidak ditemukan'}), 404

@app.route('/api/supported-sites')
def supported_sites():
    """Daftar platform yang didukung"""
    sites = [
        'YouTube', 'TikTok', 'Instagram', 'Twitter/X',
        'Reddit', 'Vimeo', 'Dailymotion', 'Twitch', 'SoundCloud',
        'Bilibili', 'VK', 'LinkedIn', 'Pinterest', 'Snapchat'
    ]
    return jsonify({'sites': sites})

# ============================================
# MAINTENANCE & MONITORING APIs
# ============================================

@app.route('/api/health')
def health_check():
    """Health check endpoint untuk monitoring"""
    try:
        # Get yt-dlp version
        ytdlp_version = yt_dlp.version.__version__

        # Check Python version
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

        # Check disk space (downloads folder)
        download_folder_size = sum(
            os.path.getsize(os.path.join(DOWNLOAD_FOLDER, f))
            for f in os.listdir(DOWNLOAD_FOLDER)
            if os.path.isfile(os.path.join(DOWNLOAD_FOLDER, f))
        ) if os.path.exists(DOWNLOAD_FOLDER) else 0

        health_data = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': {
                'app': '1.0.0',
                'python': python_version,
                'ytdlp': ytdlp_version,
                'flask': '3.0.0'
            },
            'system': {
                'download_folder_size_mb': round(download_folder_size / (1024 * 1024), 2),
                'download_folder_files': len(os.listdir(DOWNLOAD_FOLDER)) if os.path.exists(DOWNLOAD_FOLDER) else 0
            },
            'uptime': 'running'
        }

        logger.info("Health check successful")
        return jsonify(health_data)

    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/update-ytdlp', methods=['POST'])
def update_ytdlp():
    """Update yt-dlp ke versi terbaru (untuk maintenance)"""
    try:
        logger.info("Starting yt-dlp update...")

        # Get current version
        old_version = yt_dlp.version.__version__

        # Update yt-dlp using pip
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '--upgrade', 'yt-dlp'],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            # Reload yt_dlp module to get new version
            import importlib
            importlib.reload(yt_dlp)
            new_version = yt_dlp.version.__version__

            logger.info(f"yt-dlp updated from {old_version} to {new_version}")

            return jsonify({
                'success': True,
                'message': 'yt-dlp updated successfully',
                'old_version': old_version,
                'new_version': new_version,
                'timestamp': datetime.now().isoformat()
            })
        else:
            logger.error(f"yt-dlp update failed: {result.stderr}")
            return jsonify({
                'success': False,
                'error': result.stderr,
                'timestamp': datetime.now().isoformat()
            }), 500

    except subprocess.TimeoutExpired:
        logger.error("yt-dlp update timeout")
        return jsonify({
            'success': False,
            'error': 'Update timeout (exceeded 60 seconds)',
            'timestamp': datetime.now().isoformat()
        }), 408

    except Exception as e:
        logger.error(f"yt-dlp update error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/cleanup-downloads', methods=['POST'])
def cleanup_downloads():
    """Cleanup downloads folder (remove old files)"""
    try:
        logger.info("Starting downloads cleanup...")

        if not os.path.exists(DOWNLOAD_FOLDER):
            return jsonify({
                'success': True,
                'message': 'Downloads folder does not exist',
                'files_deleted': 0
            })

        files = os.listdir(DOWNLOAD_FOLDER)
        deleted_count = 0
        total_size_freed = 0

        for filename in files:
            file_path = os.path.join(DOWNLOAD_FOLDER, filename)
            if os.path.isfile(file_path):
                file_size = os.path.getsize(file_path)
                os.remove(file_path)
                deleted_count += 1
                total_size_freed += file_size

        logger.info(f"Cleanup complete: {deleted_count} files deleted, {total_size_freed} bytes freed")

        return jsonify({
            'success': True,
            'message': 'Cleanup successful',
            'files_deleted': deleted_count,
            'space_freed_mb': round(total_size_freed / (1024 * 1024), 2),
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Cleanup error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/logs')
def get_logs():
    """Get recent application logs"""
    try:
        log_file = 'app.log'

        if not os.path.exists(log_file):
            return jsonify({
                'logs': [],
                'message': 'No logs available'
            })

        # Read last 100 lines
        with open(log_file, 'r') as f:
            lines = f.readlines()
            recent_logs = lines[-100:]  # Last 100 lines

        return jsonify({
            'logs': recent_logs,
            'total_lines': len(lines),
            'showing': len(recent_logs),
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Error reading logs: {str(e)}")
        return jsonify({
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

# ============================================
# CONTENT MANAGEMENT SYSTEM APIs
# ============================================

CONFIG_FOLDER = 'config'
Path(CONFIG_FOLDER).mkdir(exist_ok=True)

def load_config(config_file):
    """Helper function to load JSON config"""
    try:
        config_path = os.path.join(CONFIG_FOLDER, config_file)
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    except Exception as e:
        logger.error(f"Error loading config {config_file}: {str(e)}")
        return None

def save_config(config_file, data):
    """Helper function to save JSON config"""
    try:
        config_path = os.path.join(CONFIG_FOLDER, config_file)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"Error saving config {config_file}: {str(e)}")
        return False

@app.route('/api/cms/config', methods=['GET'])
def get_website_config():
    """Get current website configuration"""
    try:
        config = load_config('website_config.json')
        if config:
            return jsonify({
                'success': True,
                'config': config,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Configuration not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/cms/config', methods=['POST'])
def update_website_config():
    """Update website configuration (branding, theme, features)"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        # Validate data structure
        current_config = load_config('website_config.json')

        # Merge with current config
        if current_config:
            # Update only provided fields
            if 'branding' in data:
                current_config['branding'].update(data['branding'])
            if 'theme' in data:
                current_config['theme'].update(data['theme'])
            if 'features' in data:
                current_config['features'] = data['features']
            if 'supported_platforms' in data:
                current_config['supported_platforms'] = data['supported_platforms']
        else:
            current_config = data

        # Save updated config
        if save_config('website_config.json', current_config):
            logger.info("Website configuration updated successfully")
            return jsonify({
                'success': True,
                'message': 'Configuration updated successfully',
                'config': current_config,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to save configuration'
            }), 500

    except Exception as e:
        logger.error(f"Error updating config: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/cms/faq', methods=['GET'])
def get_faq_content():
    """Get FAQ content"""
    try:
        faq_content = load_config('faq_content.json')
        if faq_content:
            return jsonify({
                'success': True,
                'content': faq_content,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'error': 'FAQ content not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/cms/faq', methods=['POST'])
def update_faq_content():
    """Update FAQ content"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        # Validate structure
        if 'faq_items' in data and isinstance(data['faq_items'], list):
            if save_config('faq_content.json', data):
                logger.info("FAQ content updated successfully")
                return jsonify({
                    'success': True,
                    'message': 'FAQ content updated successfully',
                    'timestamp': datetime.now().isoformat()
                })

        return jsonify({
            'success': False,
            'error': 'Invalid data structure'
        }), 400

    except Exception as e:
        logger.error(f"Error updating FAQ: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/cms/howto', methods=['GET'])
def get_howto_content():
    """Get How-to-Use content"""
    try:
        howto_content = load_config('howto_content.json')
        if howto_content:
            return jsonify({
                'success': True,
                'content': howto_content,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'error': 'How-to content not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/cms/howto', methods=['POST'])
def update_howto_content():
    """Update How-to-Use content"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        # Validate structure
        if 'tutorial_steps' in data and isinstance(data['tutorial_steps'], list):
            if save_config('howto_content.json', data):
                logger.info("How-to content updated successfully")
                return jsonify({
                    'success': True,
                    'message': 'How-to content updated successfully',
                    'timestamp': datetime.now().isoformat()
                })

        return jsonify({
            'success': False,
            'error': 'Invalid data structure'
        }), 400

    except Exception as e:
        logger.error(f"Error updating How-to: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/cms/theme', methods=['POST'])
def update_theme():
    """Update theme colors only"""
    try:
        data = request.get_json()

        if not data or 'theme' not in data:
            return jsonify({'success': False, 'error': 'No theme data provided'}), 400

        config = load_config('website_config.json')
        if config:
            config['theme'].update(data['theme'])

            if save_config('website_config.json', config):
                logger.info("Theme updated successfully")
                return jsonify({
                    'success': True,
                    'message': 'Theme updated successfully',
                    'theme': config['theme'],
                    'timestamp': datetime.now().isoformat()
                })

        return jsonify({
            'success': False,
            'error': 'Failed to update theme'
        }), 500

    except Exception as e:
        logger.error(f"Error updating theme: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
