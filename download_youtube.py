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
    
    # yt-dlp command with quality optimization
    cmd = [
        'yt-dlp',
        '--socket-timeout', '30',
        '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # Best video + audio combo, fallback to best mp4
        '-o', output_path,
        url
    ]
    
    print(f"📥 Download: {url}")
    print(f"💾 Save to: {output_path}")
    print(f"🎬 Quality: Best available (video + audio)\n")
    
    try:
        subprocess.run(cmd, check=True)
        print("\n✅ Done!")
    except subprocess.CalledProcessError as e:
        # Fallback: if best quality fails, try Android client
        print(f"\n⚠️  High-quality format failed, trying with Android client...")
        cmd_fallback = [
            'yt-dlp',
            '--socket-timeout', '30',
            '--extractor-args', 'youtube:player_client=android',
            '-f', 'best',
            '-o', output_path,
            url
        ]
        try:
            subprocess.run(cmd_fallback, check=True)
            print("✅ Downloaded with Android client (may be lower quality)")
        except subprocess.CalledProcessError as e2:
            print(f"\n❌ Download failed with error code {e2.returncode}")
            print("Possible issues:")
            print("  • Video may be age-restricted or private")
            print("  • Video may be blocked in your region")
            print("  • YouTube may be blocking yt-dlp access")
            print("\nTry:")
            print("  1. Update yt-dlp: pip install --upgrade yt-dlp")
            print("  2. Try downloading directly in browser")
            sys.exit(1)

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
