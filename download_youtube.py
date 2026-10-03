#!/usr/bin/env python3
"""
🎥 YOUTUBE VIDEO DOWNLOADER
Lädt Videos von YouTube herunter und konvertiert sie zu MP4 (H.264)

INSTALLATION:
  pip install yt-dlp

USAGE:
  python3 download_youtube.py <youtube_url>
  python3 download_youtube.py <youtube_url> <output_filename>
  python3 download_youtube.py <youtube_url> <output_filename> --720p
  python3 download_youtube.py <youtube_url> --playlist

BEISPIELE:
  # Standard - beste verfügbare Qualität
  python3 download_youtube.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  
  # Mit custom Namen
  python3 download_youtube.py "https://www.youtube.com/watch?v=..." "my_training_video"
  
  # 720p (empfohlen für Mobile)
  python3 download_youtube.py "https://www.youtube.com/watch?v=..." "video" --720p
  
  # Playlist runterladen
  python3 download_youtube.py "https://www.youtube.com/playlist?list=..." --playlist
"""

import os
import sys
import subprocess
from pathlib import Path


def check_dependencies():
    """Prüfe ob yt-dlp und ffmpeg installiert sind"""
    deps = {
        'yt-dlp': 'YouTube Downloader',
        'ffmpeg': 'Video Converter'
    }
    
    missing = []
    for cmd, name in deps.items():
        result = subprocess.run(['which', cmd], capture_output=True)
        if result.returncode != 0:
            missing.append(f"{name} ({cmd})")
    
    if missing:
        print("❌ FEHLER: Folgende Programme fehlen:")
        for item in missing:
            print(f"   • {item}")
        print()
        print("📦 Installation:")
        print("   Ubuntu/Debian: sudo apt install ffmpeg")
        print("   macOS: brew install ffmpeg")
        print("   Python: pip install yt-dlp")
        sys.exit(1)


def download_youtube(url, output_name=None, quality='best', playlist=False):
    """
    Lädt YouTube-Video herunter und konvertiert zu MP4 (H.264)
    
    Args:
        url: YouTube-URL
        output_name: Custom Output-Name (ohne Erweiterung)
        quality: 'best', '720p', '1080p', etc.
        playlist: True für Playlist-Download
    """
    
    # Validate URL
    if not ('youtube.com' in url or 'youtu.be' in url):
        print("❌ Fehler: Keine gültige YouTube-URL!")
        print(f"   Gegeben: {url}")
        sys.exit(1)
    
    # Output directory
    output_dir = 'src/data/videos'
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate output path
    if output_name:
        # Sanitize filename
        safe_name = ''.join(c if c.isalnum() or c == '_' else '_' for c in output_name).lower()
        output_path = os.path.join(output_dir, f"{safe_name}.mp4")
    else:
        output_path = os.path.join(output_dir, "%(title)s.mp4")
    
    print("🎥 YOUTUBE VIDEO DOWNLOADER")
    print("="*60)
    print(f"📍 URL: {url}")
    print(f"💾 Output: {output_path}")
    print(f"🎬 Qualität: {quality}")
    if playlist:
        print("📋 Modus: PLAYLIST")
    print()
    
    # Quality mapping for yt-dlp
    quality_formats = {
        '1080p': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        '720p': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        '480p': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
        'best': 'bestvideo+bestaudio/best'
    }
    
    format_str = quality_formats.get(quality, quality_formats['best'])
    
    # yt-dlp command
    cmd = [
        'yt-dlp',
        '-f', format_str,
        '-o', output_path,
        '--postprocessor-args', 'ffmpeg:-c:v libx264 -crf 23 -preset medium',  # H.264 encoding
        '-S', 'res,fps',  # Sort by resolution and fps
    ]
    
    # Playlist support
    if playlist:
        cmd.append('--yes-playlist')
    else:
        cmd.append('--no-playlist')
    
    cmd.append(url)
    
    # Print command
    print("🔨 Starte Download...")
    print()
    
    try:
        result = subprocess.run(cmd, check=True)
        
        if result.returncode == 0:
            print()
            print("="*60)
            print("✅ ERFOLGREICH HERUNTERGELADEN!")
            print("="*60)
            print(f"📁 Speichert in: {output_dir}/")
            print()
            
            # List files in output dir
            try:
                files = sorted([f for f in os.listdir(output_dir) if f.endswith('.mp4')])
                if files:
                    print("📹 Neueste Videos:")
                    for f in files[-3:]:
                        path = os.path.join(output_dir, f)
                        size_mb = os.path.getsize(path) / 1024 / 1024
                        print(f"   • {f} ({size_mb:.1f} MB)")
            except:
                pass
            
            print()
            print("💡 Nächste Schritte:")
            print("   1. Öffne Admin Panel: http://localhost:5001/admin")
            print("   2. Gehe zu 🎥 Videos Tab")
            print("   3. Wähle die Übung")
            print("   4. Klicke 'Upload & Generate Poster'")
            print("   5. Wähle das gerade heruntergeladene Video")
            print()
            
            return True
    
    except subprocess.CalledProcessError as e:
        print()
        print("❌ DOWNLOAD FEHLER!")
        print(f"Error Code: {e.returncode}")
        print()
        print("💡 Tipps:")
        print("   • Prüfe die YouTube-URL")
        print("   • Manche Videos sind regional gesperrt")
        print("   • Prüfe deine Internet-Verbindung")
        print("   • yt-dlp aktualisieren: pip install --upgrade yt-dlp")
        return False
    
    except FileNotFoundError as e:
        print()
        print("❌ Programm nicht gefunden!")
        print(f"Error: {e}")
        sys.exit(1)
    
    except Exception as e:
        print()
        print("❌ UNERWARTETER FEHLER!")
        print(f"Error: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    # Parse arguments
    url = sys.argv[1]
    output_name = None
    quality = 'best'
    playlist = False
    
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg == '--playlist':
            playlist = True
        elif arg in ['--720p', '--720']:
            quality = '720p'
        elif arg in ['--1080p', '--1080']:
            quality = '1080p'
        elif arg in ['--480p', '--480']:
            quality = '480p'
        elif arg == '--best':
            quality = 'best'
        elif not arg.startswith('--'):
            if not output_name:
                output_name = arg
        
        i += 1
    
    # Check dependencies
    print("🔍 Prüfe Abhängigkeiten...")
    check_dependencies()
    print("✅ Alle Abhängigkeiten vorhanden")
    print()
    
    # Download
    success = download_youtube(url, output_name, quality, playlist)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
