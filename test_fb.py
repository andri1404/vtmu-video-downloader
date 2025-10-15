import yt_dlp

url = "https://www.facebook.com/share/r/1CKkXG7M8i/"

ydl_opts = {
    'quiet': False,
    'no_warnings': False,
    'http_headers': {
        'User-Agent': 'facebookexternalhit/1.1',
    },
}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        print(f"\nSUCCESS! Title: {info.get('title')}")
except Exception as e:
    print(f"\nERROR: {e}")
