#!/usr/bin/env python3
"""YouTube Video Downloader - yt-dlp Wrapper"""

import os
import sys
import subprocess

def download(url, output_name=None):
    """Download video from YouTube using yt-dlp"""
    
    output_dir = 'src/data/videos'
    os.makedirs(output_dir, exist_ok=True)
    
    # Output path
    if output_name:
        output_path = os.path.join(output_dir, f"{output_name}.mp4")
    else:
        output_path = os.path.join(output_dir, "%(title)s.mp4")
    
    # yt-dlp command
    cmd = [
        'yt-dlp',
        '-o', output_path,
        url
    ]
    
    print(f"📥 Download: {url}")
    print(f"💾 Save to: {output_path}\n")
    
    subprocess.run(cmd, check=True)
    print("\n✅ Done!")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 download_youtube.py <youtube_url> [output_name]")
        print("\nExample:")
        print("  python3 download_youtube.py 'https://www.youtube.com/watch?v=...'")
        print("  python3 download_youtube.py 'https://www.youtube.com/watch?v=...' 'my_video'")
        sys.exit(1)
    
    url = sys.argv[1]
    output_name = sys.argv[2] if len(sys.argv) > 2 else None
    
    download(url, output_name)
