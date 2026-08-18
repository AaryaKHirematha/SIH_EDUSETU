import sys
sys.path.append('d:\SIH\gate1_venv\lib\site-packages')
import tempfile
import yt_dlp
import os

def duration_filter(info, *, incomplete):
    duration = info.get('duration')
    if duration and duration > 900:
        raise ValueError('DURATION_LIMIT_EXCEEDED')
    return None

ydl_opts = {
    'outtmpl': 'D:/SIH/runtime/media/video_%(id)s.%(ext)s',
    'format': 'worstvideo[ext=mp4]+bestaudio[ext=m4a]/best',
    'max_filesize': 50 * 1024 * 1024,
    'match_filter': duration_filter,
    'quiet': True,
    'no_warnings': True,
}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info('https://www.youtube.com/watch?v=jNQXAC9IVRw', download=True)
        print(f'SUCCESS: {ydl.prepare_filename(info_dict)}')
except Exception as e:
    print(f'ERROR: {e}')
