#!/usr/bin/env python3
"""
Generate video posters (thumbnails) from the first frame of MP4 files.
Uses ffmpeg to extract and compress thumbnails efficiently.
"""

import os
import subprocess
import sys

VIDEO_DIR = './src/data/videos'

def generate_posters():
    """Extract first frame from each MP4 file as poster image."""
    if not os.path.exists(VIDEO_DIR):
        print(f"❌ Video directory not found: {VIDEO_DIR}")
        return False
    
    mp4_files = [f for f in os.listdir(VIDEO_DIR) if f.endswith('.mp4')]
    
    if not mp4_files:
        print("❌ No MP4 files found in video directory")
        return False
    
    print(f"🎬 Generating posters for {len(mp4_files)} videos...\n")
    
    success_count = 0
    for video_file in sorted(mp4_files):
        video_path = os.path.join(VIDEO_DIR, video_file)
        poster_path = os.path.join(VIDEO_DIR, video_file.replace('.mp4', '.jpg'))
        
        # Skip if poster already exists
        if os.path.exists(poster_path):
            print(f"⏭️  {video_file:45s} → already exists")
            success_count += 1
            continue
        
        # Extract first frame at 1 second (or 0.5 second if video is short)
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-ss', '0.5',           # Start at 0.5 seconds
            '-vframes', '1',        # Extract 1 frame
            '-q:v', '2',            # Quality: 2 (best)
            '-y',                   # Overwrite without asking
            poster_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                size_kb = os.path.getsize(poster_path) / 1024
                print(f"✅ {video_file:45s} → {size_kb:6.1f} KB")
                success_count += 1
            else:
                print(f"❌ {video_file:45s} → ffmpeg error")
                if os.path.exists(poster_path):
                    os.remove(poster_path)
        except subprocess.TimeoutExpired:
            print(f"❌ {video_file:45s} → timeout")
            if os.path.exists(poster_path):
                os.remove(poster_path)
        except Exception as e:
            print(f"❌ {video_file:45s} → {str(e)}")
    
    print(f"\n✨ Generated {success_count}/{len(mp4_files)} posters!")
    return success_count == len(mp4_files)

if __name__ == '__main__':
    success = generate_posters()
    sys.exit(0 if success else 1)
