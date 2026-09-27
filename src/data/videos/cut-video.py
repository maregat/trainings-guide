#!/usr/bin/env python3
"""
🎬 Video Schneidetool
Schneidet ein Video von Start- bis End-Zeit mit ffmpeg
"""

import subprocess
import sys
from pathlib import Path

def get_video_duration(video_path):
    """Ermittelt die Länge eines Videos in Sekunden"""
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', 
             '-of', 'default=noprint_wrappers=1:nokey=1:noprint_wrappers=1', video_path],
            capture_output=True,
            text=True
        )
        return float(result.stdout.strip())
    except Exception as e:
        print(f"❌ Fehler beim Abrufen der Videolänge: {e}")
        return None

def cut_video(input_file, output_file, start_time, end_time, format_output=None):
    """
    Schneidet ein Video
    
    Args:
        input_file: Pfad zum Original-Video
        output_file: Pfad zum Output-Video
        start_time: Start-Zeit in Sekunden (z.B. 5.5 für 5,5 Sekunden)
        end_time: End-Zeit in Sekunden
        format_output: Output-Format (mp4, webm, etc.) - optional
    """
    input_path = Path(input_file)
    output_path = Path(output_file)
    
    if not input_path.exists():
        print(f"❌ Input-Datei nicht gefunden: {input_file}")
        return False
    
    # Bestimme Output-Format
    if format_output is None:
        format_output = output_path.suffix.lower().lstrip('.')
    
    # Duration berechnen
    duration = end_time - start_time
    
    print(f"\n🎬 VIDEO-SCHNEIDEN")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"📁 Input:      {input_file}")
    print(f"📁 Output:     {output_file}")
    print(f"⏱️  Start:      {start_time}s")
    print(f"⏱️  End:        {end_time}s")
    print(f"⏱️  Duration:   {duration}s ({duration/60:.1f} min)")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    try:
        # ffmpeg Befehl
        cmd = [
            'ffmpeg',
            '-i', str(input_path),
            '-ss', str(start_time),
            '-to', str(end_time),
            '-c', 'copy',  # Schnell: Stream kopieren ohne neu zu kodieren
            '-y',  # Überschreibe Output-Datei
            str(output_path)
        ]
        
        print("⏳ Schneiden läuft...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            output_size = output_path.stat().st_size / (1024 * 1024)  # MB
            print(f"✅ Video erfolgreich geschnitten!")
            print(f"📊 Output-Größe: {output_size:.1f} MB")
            print(f"💾 Gespeichert: {output_path}")
            return True
        else:
            print(f"❌ Fehler beim Schneiden:")
            print(result.stderr)
            return False
            
    except FileNotFoundError:
        print("❌ ffmpeg nicht gefunden!")
        print("   Bitte installieren: apt install ffmpeg")
        return False
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False

def interactive_mode():
    """Interaktives Modus - Benutzer gibt Werte ein"""
    print("\n🎬 VIDEO-SCHNEIDETOOL (Interaktiv)")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    # Input-Datei
    input_file = input("📁 Input-Video Pfad: ").strip()
    if not Path(input_file).exists():
        print(f"❌ Datei nicht gefunden: {input_file}")
        return
    
    # Zeige Videolänge
    duration = get_video_duration(input_file)
    if duration:
        print(f"   ✅ Videolänge: {duration:.1f}s ({duration/60:.1f} min)")
    else:
        return
    
    # Start-Zeit
    while True:
        try:
            start = float(input(f"\n⏱️  Start-Zeit (0-{duration:.1f}s): ").strip())
            if 0 <= start < duration:
                break
            print(f"❌ Wert muss zwischen 0 und {duration:.1f} liegen")
        except ValueError:
            print("❌ Ungültige Eingabe - bitte Zahl eingeben (z.B. 5.5)")
    
    # End-Zeit
    while True:
        try:
            end = float(input(f"⏱️  End-Zeit ({start:.1f}-{duration:.1f}s): ").strip())
            if start < end <= duration:
                break
            print(f"❌ Wert muss zwischen {start} und {duration:.1f} liegen")
        except ValueError:
            print("❌ Ungültige Eingabe - bitte Zahl eingeben")
    
    # Output-Datei
    input_path = Path(input_file)
    suggested_output = input_path.parent / f"cut_{input_path.name}"
    output_file = input(f"\n💾 Output Pfad [{suggested_output}]: ").strip()
    if not output_file:
        output_file = str(suggested_output)
    
    # Schneiden
    cut_video(input_file, output_file, start, end)

def main():
    """Hauptprogramm"""
    if len(sys.argv) < 4:
        print(__doc__)
        print("\n📋 VERWENDUNG:")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("\n1️⃣  COMMAND-LINE Modus:")
        print("   python3 cut-video.py <input.mp4> <output.mp4> <start_sek> <end_sek>")
        print("\n   Beispiel:")
        print("   python3 cut-video.py input.mp4 output.mp4 5.5 45.2")
        print("   → Schneidet Video von 5,5s bis 45,2s")
        
        print("\n2️⃣  INTERAKTIV Modus:")
        print("   python3 cut-video.py")
        print("   → Fragt nach Eingaben")
        
        print("\n📋 REQUIREMENTS:")
        print("   - ffmpeg installiert: apt install ffmpeg")
        print("   - ffprobe (Teil von ffmpeg)")
        
        interactive_mode()
        return
    
    # Command-Line Modus
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        start_time = float(sys.argv[3])
        end_time = float(sys.argv[4])
    except (ValueError, IndexError):
        print("❌ Start- und End-Zeit müssen Zahlen sein!")
        print("   Beispiel: python3 cut-video.py input.mp4 output.mp4 5.5 45.2")
        return
    
    cut_video(input_file, output_file, start_time, end_time)

if __name__ == '__main__':
    main()
