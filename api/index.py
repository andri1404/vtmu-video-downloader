from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp
import os
import uuid
from pathlib import Path
import json
import sys
from datetime import datetime
import time
from collections import defaultdict
from functools import wraps

app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static')

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

# Use /tmp for serverless environment (Vercel)
DOWNLOAD_FOLDER = '/tmp/downloads'
Path(DOWNLOAD_FOLDER).mkdir(exist_ok=True)

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
                # Block IP temporarily
                blocked_ips.add(ip)
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
                return jsonify({
                    'error': 'Batas permintaan per jam tercapai. Silakan coba lagi nanti.',
                    'retry_after': 3600
                }), 429

            # Check for suspicious behavior
            if is_suspicious_request():
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

    # Limited CORS
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Max-Age'] = '3600'

    return response

# Input validation helpers
def is_valid_url(url):
    """Validate URL to prevent injection attacks"""
    if not url or not isinstance(url, str):
        return False
    if len(url) > 2048:
        return False
    if not url.startswith(('http://', 'https://')):
        return False
    dangerous_chars = ['<', '>', '"', "'", ';', '(', ')', '{', '}']
    if any(char in url for char in dangerous_chars):
        return False
    return True

def sanitize_filename(filename):
    """Sanitize filename to prevent path traversal"""
    filename = filename.replace('/', '').replace('\\', '').replace('\0', '')
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
@rate_limit_decorator()
def get_video_info():
    """Mendapatkan informasi video tanpa download"""
    try:
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

        # Handle TikTok photo/slideshow URLs
        if 'tiktok.com' in url and '/photo/' in url:
            if '?' in url:
                url = url.split('?')[0]
            url = url.replace('/photo/', '/video/')

        # Determine platform
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
            'source_address': '0.0.0.0',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
            },
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
                    'api': 'graphql',
                },
            },
            'retries': 15,
            'fragment_retries': 15,
            'socket_timeout': 30,
            'nocheckcertificate': True,
        }

        if platform == 'instagram':
            ydl_opts['http_headers']['Referer'] = 'https://www.instagram.com/'
            ydl_opts['http_headers']['X-IG-App-ID'] = '936619743392459'

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            if not info:
                return jsonify({'error': 'Tidak dapat mengambil informasi video. URL mungkin tidak valid atau tidak didukung.'}), 400

            video_info = {
                'title': info.get('title', 'Unknown'),
                'thumbnail': info.get('thumbnail', '') or info.get('thumbnails', [{}])[0].get('url', ''),
                'duration': info.get('duration', 0),
                'uploader': info.get('uploader', info.get('uploader_id', 'Unknown')),
                'view_count': info.get('view_count', 0) or info.get('like_count', 0),
                'platform': info.get('extractor', 'Unknown'),
                'formats': [
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
            }

            return jsonify(video_info)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/download', methods=['POST'])
@rate_limit_decorator()
def download_video():
    """Download video dengan kualitas yang dipilih"""
    try:
        data = request.get_json()
        url = data.get('url')
        quality = data.get('quality', 'Best Quality')
        format_id = data.get('format_id', 'best')

        if not url:
            return jsonify({'error': 'URL tidak boleh kosong'}), 400

        if not is_valid_url(url):
            return jsonify({'error': 'URL tidak valid atau mengandung karakter berbahaya'}), 400

        if 'facebook.com' in url or 'fb.watch' in url or 'fb.com' in url:
            return jsonify({'error': 'Maaf, Facebook sementara tidak didukung. Silakan gunakan platform lain seperti Instagram, TikTok, atau YouTube.'}), 400

        # Handle TikTok photo/slideshow URLs
        if 'tiktok.com' in url and '/photo/' in url:
            if '?' in url:
                url = url.split('?')[0]
            url = url.replace('/photo/', '/video/')

        # Determine platform
        platform = 'unknown'
        if 'instagram.com' in url:
            platform = 'instagram'
        elif 'tiktok.com' in url:
            platform = 'tiktok'
        elif 'youtube.com' in url or 'youtu.be' in url:
            platform = 'youtube'

        # Generate unique filename
        unique_id = str(uuid.uuid4())[:8]
        output_template = os.path.join(DOWNLOAD_FOLDER, f'{unique_id}.%(ext)s')

        ydl_opts = {
            'format': format_id,
            'outtmpl': output_template,
            'quiet': True,
            'no_warnings': True,
            'ignoreerrors': False,
            'merge_output_format': 'mp4',
            'postprocessor_args': ['-ar', '44100'],
            'source_address': '0.0.0.0',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
            },
            'restrictfilenames': True,
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
            'retries': 15,
            'fragment_retries': 15,
            'socket_timeout': 30,
            'skip_unavailable_fragments': True,
            'nocheckcertificate': True,
            'geo_bypass': True,
        }

        if platform == 'instagram':
            ydl_opts['http_headers']['Referer'] = 'https://www.instagram.com/'
            ydl_opts['http_headers']['X-IG-App-ID'] = '936619743392459'

        # Adjust format based on quality
        if quality == 'Audio Only (MP3)':
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        else:
            ydl_opts['format'] = format_id
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=True)
            except Exception as extract_error:
                # Try to find downloaded files
                if 'tiktok' in url.lower():
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

            # If audio, file extension changes to .mp3
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
        filename = sanitize_filename(filename)
        file_path = os.path.join(DOWNLOAD_FOLDER, filename)

        # Prevent directory traversal
        if not os.path.abspath(file_path).startswith(os.path.abspath(DOWNLOAD_FOLDER)):
            return jsonify({'error': 'Akses ditolak'}), 403

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

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    try:
        ytdlp_version = yt_dlp.version.__version__
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

        health_data = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': {
                'app': '1.0.0',
                'python': python_version,
                'ytdlp': ytdlp_version,
                'flask': '3.0.0'
            },
            'environment': 'serverless'
        }

        return jsonify(health_data)

    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

# Vercel serverless handler
def handler(request):
    return app(request)
