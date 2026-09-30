#!/usr/bin/env python3
"""
🎬 VIDEOSCHNEIDEN - EINFACH & PRÄZISE
Schneidet Videos auf Millisekunde genau mit ffmpeg.
Verwendet -c:v copy -c:a copy (KEINE Neucodierung = ultraschnell!)

USAGE:
  python3 cut_video.py <input.mp4> <start> <end> [output.mp4]
  
BEISPIELE:
  # Sekunden (einfach)
  python3 cut_video.py video.mp4 12.5 45.3
  
  # Millisekunden (präzise)
  python3 cut_video.py video.mp4 12500 45300 ms
  
  # HH:MM:SS Format
  python3 cut_video.py video.mp4 00:00:12.500 00:00:45.300
  
  # Mit Output-Datei
  python3 cut_video.py video.mp4 10 50 output_clip.mp4
  
  # Mehrere Clips aus einer Datei (Batch)
  python3 cut_video.py batch video.mp4 "12.5-45.3, 60-90, 120.5-150.750"
"""

import os
import sys
import subprocess
import re
from pathlib import Path


def parse_time(time_str, unit="seconds"):
    """
    Parse verschiedene Zeitformate zu Sekunden (mit Millisekunden-Präzision)
    
    Formate:
    - "12.5" = 12.5 Sekunden
    - "12500" mit unit="ms" = 12.5 Sekunden
    - "00:00:12.500" = 12.5 Sekunden (HH:MM:SS.mmm)
    """
    
    time_str = str(time_str).strip()
    
    # Millisekunden
    if unit == "ms":
        return float(time_str) / 1000.0
    
    # HH:MM:SS.mmm Format
    if ":" in time_str:
        parts = time_str.split(":")
        if len(parts) == 3:  # HH:MM:SS
            try:
                hours = int(parts[0])
                minutes = int(parts[1])
                seconds = float(parts[2])
                total_seconds = hours * 3600 + minutes * 60 + seconds
                return total_seconds
            except ValueError:
                raise ValueError(f"❌ Ungültiges Zeit-Format: {time_str}")
    
    # Sekunden (mit Dezimal für ms)
    try:
        return float(time_str)
    except ValueError:
        raise ValueError(f"❌ Ungültiges Zeit-Format: {time_str}")


def seconds_to_ffmpeg_format(seconds):
    """Konvertiert Sekunden zu ffmpeg Format: HH:MM:SS.mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"


def cut_video(input_file, start_time, end_time, output_file=None, time_unit="seconds"):
    """
    Schneidet Video mit ffmpeg (ultraschnell!)
    
    Args:
        input_file: Pfad zum Input-Video
        start_time: Startzeit (Sekunden, Millisekunden oder HH:MM:SS.mmm)
        end_time: Endzeit
        output_file: Output-Datei (auto-generiert wenn None)
        time_unit: "seconds" oder "ms"
    """
    
    # Validierung
    if not os.path.exists(input_file):
        print(f"❌ Fehler: Datei nicht gefunden: {input_file}")
        return False
    
    # Zeiten parsen
    try:
        start_sec = parse_time(start_time, time_unit)
        end_sec = parse_time(end_time, time_unit)
    except ValueError as e:
        print(f"❌ {e}")
        return False
    
    # Validierung
    if start_sec < 0:
        print(f"❌ Startzeit kann nicht negativ sein: {start_sec}s")
        return False
    
    if end_sec <= start_sec:
        print(f"❌ Endzeit muss nach Startzeit liegen! ({start_sec}s → {end_sec}s)")
        return False
    
    duration = end_sec - start_sec
    
    # Output-Datei generieren wenn nicht angegeben
    if output_file is None:
        input_path = Path(input_file)
        output_file = input_path.stem + f"_cut_{start_sec:.3f}_{end_sec:.3f}.mp4"
    
    # ffmpeg Format
    start_fmt = seconds_to_ffmpeg_format(start_sec)
    end_fmt = seconds_to_ffmpeg_format(end_sec)
    
    # ffmpeg Command (KEINE Neucodierung = Sekunden statt Stunden!)
    cmd = [
        "ffmpeg",
        "-i", input_file,
        "-ss", start_fmt,           # Startzeit
        "-to", end_fmt,              # Endzeit (nicht -t duration!)
        "-c:v", "copy",              # VIDEO: keine Neucodierung
        "-c:a", "copy",              # AUDIO: keine Neucodierung
        "-y",                        # Überschreibe ohne Fragen
        output_file
    ]
    
    # Zeige Befehl
    print(f"🎬 Schneiden: {input_file}")
    print(f"   📍 Start: {start_fmt} ({start_sec:.3f}s)")
    print(f"   📍 Ende:  {end_fmt} ({end_sec:.3f}s)")
    print(f"   ⏱️  Länge: {duration:.3f}s")
    print(f"   💾 Output: {output_file}")
    print(f"   ⚡ Modus: COPY (ultraschnell, keine Neucodierung!)")
    print()
    
    # Ausführen
    try:
        result = subprocess.run(cmd, check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        print(f"✅ ERFOLG! Video gespeichert: {output_file}")
        
        # Dateigröße anzeigen
        if os.path.exists(output_file):
            size_mb = os.path.getsize(output_file) / 1024 / 1024
            print(f"   📦 Größe: {size_mb:.2f} MB")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ ffmpeg Fehler!")
        print(e.stderr.decode())
        return False
    except FileNotFoundError:
        print("❌ ffmpeg nicht gefunden! Installiere: sudo apt install ffmpeg")
        return False


def batch_cut(input_file, clips_str, time_unit="seconds"):
    """
    Schneidet mehrere Clips auf einmal.
    
    Format: "start1-end1, start2-end2, start3-end3, ..."
    Beispiel: "12.5-45.3, 60-90, 120.5-150.750"
    """
    
    clips = []
    for clip in clips_str.split(","):
        clip = clip.strip()
        if "-" not in clip:
            print(f"⚠️  Skipping ungültiger Clip: {clip}")
            continue
        
        parts = clip.split("-")
        if len(parts) != 2:
            print(f"⚠️  Skipping ungültiger Clip: {clip}")
            continue
        
        clips.append((parts[0].strip(), parts[1].strip()))
    
    if not clips:
        print("❌ Keine gültigen Clips gefunden!")
        return False
    
    print(f"🎬 Batch-Schneiden: {len(clips)} Clips")
    print()
    
    success_count = 0
    for i, (start, end) in enumerate(clips, 1):
        input_path = Path(input_file)
        output = input_path.stem + f"_clip{i:02d}.mp4"
        
        print(f"[{i}/{len(clips)}] ", end="")
        if cut_video(input_file, start, end, output, time_unit):
            success_count += 1
        print()
    
    print(f"\n✅ {success_count}/{len(clips)} Clips erfolgreich geschnitten!")
    return success_count == len(clips)


def main():
    """CLI Interface"""
    
    if len(sys.argv) < 4:
        print(__doc__)
        print("\n" + "="*70)
        print("FEHLER: Zu wenig Argumente!")
        print("="*70)
        sys.exit(1)
    
    # Argumente
    if sys.argv[1] == "batch":
        # Batch-Modus: batch <input> <clips>
        if len(sys.argv) < 4:
            print("❌ batch mode braucht: batch <input.mp4> \"clip1, clip2, ...\"")
            sys.exit(1)
        
        input_file = sys.argv[2]
        clips_str = sys.argv[3]
        time_unit = sys.argv[4] if len(sys.argv) > 4 else "seconds"
        
        batch_cut(input_file, clips_str, time_unit)
    
    else:
        # Normal-Modus: <input> <start> <end> [output] [unit]
        input_file = sys.argv[1]
        start_time = sys.argv[2]
        end_time = sys.argv[3]
        
        output_file = None
        time_unit = "seconds"
        
        # Argumente parsen
        if len(sys.argv) > 4:
            arg4 = sys.argv[4]
            
            # Wenn es "ms" oder "milliseconds" ist → time_unit
            if arg4.lower() in ["ms", "milliseconds", "millis"]:
                time_unit = "ms"
            else:
                # Sonst → output file
                output_file = arg4
                
                # Und noch ein 5. Argument könnte time_unit sein
                if len(sys.argv) > 5:
                    if sys.argv[5].lower() in ["ms", "milliseconds", "millis"]:
                        time_unit = "ms"
        
        cut_video(input_file, start_time, end_time, output_file, time_unit)


if __name__ == "__main__":
    main()
