#!/usr/bin/env python3
"""
🎬 BATCH VIDEO SCHNEIDEN
Schneidet ein langes Video in mehrere Übungs-Videos basierend auf Zeitstempeln
aus exercises.json
"""

import subprocess
import json
import sys
from pathlib import Path

def get_video_duration(video_path):
    """Ermittelt Videolänge in Sekunden"""
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1:noprint_wrappers=1', video_path],
            capture_output=True,
            text=True
        )
        return float(result.stdout.strip())
    except Exception as e:
        print(f"❌ Fehler bei ffprobe: {e}")
        return None

def cut_video_segment(input_file, output_file, start_time, end_time):
    """Schneidet ein Video-Segment"""
    try:
        cmd = [
            'ffmpeg',
            '-i', str(input_file),
            '-ss', str(start_time),
            '-to', str(end_time),
            '-c:v', 'libvpx-vp9',  # VP9 codec für WebM
            '-b:v', '500k',         # Bitrate
            '-c:a', 'libopus',      # Audio codec
            '-b:a', '128k',         # Audio bitrate
            '-y',                   # Überschreibe
            str(output_file)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False

def main():
    """Hauptprogramm"""
    # Pfade
    input_video = Path('src/data/videos/BallMastery.webm')
    exercises_file = Path('src/data/exercises.json')
    output_dir = Path('src/data/videos')
    
    # Prüfe ob Input existiert
    if not input_video.exists():
        print(f"❌ {input_video} nicht gefunden!")
        return
    
    if not exercises_file.exists():
        print(f"❌ {exercises_file} nicht gefunden!")
        return
    
    # Laden exercises.json
    with open(exercises_file) as f:
        data = json.load(f)
    
    # Sammle Coerver-Übungen mit Zeitstempeln
    coerver_exercises = []
    for ex_id, exercise in data['exercises'].items():
        if exercise['category'] == 'warmup_coerver':
            # Extrahiere Zeitstempel aus videoLink.url falls vorhanden
            if 'videoLink' in exercise and exercise['videoLink']:
                url = exercise['videoLink'].get('url', '')
                if '&t=' in url:
                    timestamp_str = url.split('&t=')[1].split('&')[0].replace('s', '')
                    try:
                        timestamp = float(timestamp_str)
                        coerver_exercises.append({
                            'id': ex_id,
                            'name': exercise['name'],
                            'timestamp': timestamp,
                            'order': exercise.get('order', 999)
                        })
                    except ValueError:
                        pass
    
    # Sortiere nach Zeitstempel (nicht nach order!)
    coerver_exercises.sort(key=lambda x: x['timestamp'])
    
    if not coerver_exercises:
        print("❌ Keine Coerver-Übungen mit Zeitstempeln gefunden!")
        return
    
    print("\n🎬 BATCH VIDEO-SCHNEIDEN")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"📁 Input:      {input_video}")
    print(f"📁 Output Dir: {output_dir}")
    print(f"📊 Übungen:    {len(coerver_exercises)}")
    
    # Prüfe Videolänge
    duration = get_video_duration(str(input_video))
    if duration:
        print(f"⏱️  Länge:      {duration:.1f}s ({duration/60:.1f} min)")
    else:
        print("⚠️  Konnte Länge nicht ermitteln")
        return
    
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    # Schneide Videos
    cut_count = 0
    for i, exercise in enumerate(coerver_exercises):
        # Start-Zeit = aktuelle Übung
        start_time = exercise['timestamp']
        
        # End-Zeit = nächste Übung (oder Ende des Videos)
        if i + 1 < len(coerver_exercises):
            end_time = coerver_exercises[i + 1]['timestamp']
        else:
            end_time = duration
        
        # Erstelle Dateinamen
        safe_name = exercise['name'].lower().replace(' ', '_').replace('(', '').replace(')', '').replace('–', '')
        output_file = output_dir / f"{safe_name}.webm"
        
        segment_duration = end_time - start_time
        print(f"#{i+1:2d} {exercise['name']:40s} [{start_time:6.1f}s → {end_time:6.1f}s] ({segment_duration:5.1f}s)", end=" ")
        
        if cut_video_segment(str(input_video), str(output_file), start_time, end_time):
            file_size = output_file.stat().st_size / (1024 * 1024)
            print(f"✅ ({file_size:.1f} MB)")
            cut_count += 1
        else:
            print("❌")
    
    print("\n" + "━" * 80)
    print(f"✅ Fertig! {cut_count}/{len(coerver_exercises)} Videos geschnitten")
    print(f"   Videos liegen in: {output_dir}")
    print("\n💡 Nächste Schritte:")
    print("   1. exercises.json updaten mit lokalen Video-URLs")
    print("   2. build.sh ausführen")
    print("   3. Deployen!")

if __name__ == '__main__':
    main()
