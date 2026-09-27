#!/usr/bin/env python3
"""
🎬 WebM zu MP4 Konvertierung
Konvertiert alle WebM-Videos zu MP4 für bessere Kompatibilität (iPhone, etc.)
"""

import subprocess
from pathlib import Path

def convert_to_mp4(input_file, output_file):
    """Konvertiert WebM zu MP4"""
    try:
        cmd = [
            'ffmpeg',
            '-i', str(input_file),
            '-c:v', 'libx264',      # H.264 Video Codec
            '-preset', 'medium',    # Kompression Level
            '-crf', '23',           # Qualität (23 = gut, kleiner = besser aber größer)
            '-c:a', 'aac',          # AAC Audio
            '-b:a', '128k',         # Audio Bitrate
            '-y',                   # Überschreibe
            str(output_file)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False

def main():
    """Konvertiere alle WebM zu MP4"""
    videos_dir = Path('src/data/videos')
    
    # Finde alle WebM-Dateien (außer BallMastery)
    webm_files = [f for f in videos_dir.glob('*.webm') if f.name != 'BallMastery.webm']
    
    if not webm_files:
        print("❌ Keine WebM-Dateien gefunden!")
        return
    
    print("\n🎬 WEBM ZU MP4 KONVERTIERUNG")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"📊 Dateien: {len(webm_files)}\n")
    
    converted_count = 0
    for i, webm_file in enumerate(sorted(webm_files), 1):
        mp4_file = webm_file.parent / webm_file.stem.replace('.webm', '.mp4')
        
        print(f"#{i:2d} {webm_file.name:50s}", end=" ", flush=True)
        
        if convert_to_mp4(str(webm_file), str(mp4_file)):
            file_size = mp4_file.stat().st_size / (1024 * 1024)
            print(f"✅ ({file_size:.1f} MB)")
            converted_count += 1
            # Lösche original WebM
            webm_file.unlink()
        else:
            print("❌")
    
    print("\n" + "━" * 80)
    print(f"✅ Fertig! {converted_count}/{len(webm_files)} Videos konvertiert")
    print(f"   Alte WebM-Dateien gelöscht")
    print("\n💡 Nächste Schritte:")
    print("   1. python3 update-video-extensions.py")
    print("   2. build.sh")
    print("   3. git add -A && git commit && git push")

if __name__ == '__main__':
    main()
