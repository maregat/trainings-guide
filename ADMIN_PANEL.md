# 🎬 Trainings-Guide Admin Panel

Dieses Admin-Panel erlaubt es, Videos direkt zu den Übungen hochzuladen und mit exercises.json zu verlinken.

## Features

- 🔐 **Passwort-Geschützt** - Nur autorisierte Benutzer
- 📹 **Drag & Drop** - Video einfach hochladen
- 👁️ **Live Preview** - Video vor dem Upload anschauen
- 🎯 **1-Klick Upload** - Video wird automatisch mit Übung verlinkt
- 🗑️ **Delete** - Alte Videos löschen
- 💾 **Auto-Save** - exercises.json wird sofort aktualisiert

## Installation

### 1. Python-Pakete installieren

```bash
cd /home/mare/Nextcloud/Fussball/trainings-guide
pip install Flask Werkzeug
```

Oder besser mit venv:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Passwort ändern (WICHTIG!)

In `server.py` Zeile ~25:

```python
ADMIN_PASSWORD = 'admin123'  # Change this!
```

Ändere `admin123` auf ein sicheres Passwort!

## Starten

```bash
cd /home/mare/Nextcloud/Fussball/trainings-guide
source venv/bin/activate
python server.py
```

Dann öffnen: **http://localhost:5001**

## 🎥 YouTube Videos herunterladen

Ein Python-Skript (`download_youtube.py`) macht es super einfach, Videos direkt von YouTube herunterzuladen!

### Installation (einmalig)

```bash
pip install yt-dlp
sudo apt install ffmpeg  # Ubuntu/Debian
# oder
brew install ffmpeg     # macOS
```

### Verwendung

**Standard - beste verfügbare Qualität:**

```bash
python3 download_youtube.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

**Mit Custom-Name:**

```bash
python3 download_youtube.py "https://www.youtube.com/watch?v=..." "mein_video"
```

**720p-Qualität (empfohlen für Mobile):**

```bash
python3 download_youtube.py "https://www.youtube.com/watch?v=..." "video" --720p
```

**Playlist herunterladen:**

```bash
python3 download_youtube.py "https://www.youtube.com/playlist?list=..." --playlist
```

### Qualitäts-Optionen

```bash
--best    # Beste verfügbare (Standard)
--1080p   # Full HD
--720p    # HD (empfohlen)
--480p    # SD (klein)
```

### Beispiel: Kompletter Workflow

```bash
# 1. Video von YouTube herunterladen
python3 download_youtube.py "https://www.youtube.com/watch?v=coerver123" "coerver_drill" --720p

# 2. Admin Panel öffnen
python server.py

# 3. Browser: http://localhost:5001/admin
# - Login
# - Videos Tab
# - Übung wählen: "Coerver Basis 1"
# - Video ziehen/hochladen: coerver_drill.mp4
# - Button "Upload & Generate Poster"
# - ✅ Fertig!

# 4. Deploy zur Live-App
# - Im Admin Panel: 🚀 Deploy Live Button
# - Oder manuell:
bash build.sh
git add -A && git commit -m "Add: Coerver Drill Video"
git push origin main
```

### Output

Videos werden automatisch zu `src/data/videos/` gespeichert:

```
src/data/videos/
├── coerver_drill.mp4          ← Heruntergeladenes Video
├── coerver_drill_cut.mp4      ← Zugeschnittene Version (mit cut_video.py)
├── sole_taps.mp4
└── ...
```

### Features

✅ **Automatische Konvertierung** zu MP4 + H.264 (iPhone-kompatibel)  
✅ **Quality-Select** - Wähle beste Qualität für deine Bandbreite  
✅ **Playlist-Support** - Lade ganze Playlisten herunter  
✅ **Dependency-Check** - Prüft auf ffmpeg & yt-dlp  
✅ **Error-Handling** - Klare Fehlermeldungen  

### Fehlerbehandlung

**"yt-dlp: command not found"**
```bash
pip install yt-dlp
```

**"ffmpeg: command not found"**
```bash
# Ubuntu/Debian:
sudo apt install ffmpeg

# macOS:
brew install ffmpeg
```

**"Video ist regional gesperrt"**
- Video kann nicht heruntergeladen werden
- Nutze VPN falls erlaubt, oder finde alternatives Video

**yt-dlp aktualisieren:**
```bash
pip install --upgrade yt-dlp
```

## Verwendung

1. 🔐 **Login** - Passwort eingeben
2. 📋 **Übung wählen** - Dropdown auswählen
3. 📹 **Video ziehen** - In die Upload-Zone droppen
4. 👁️ **Preview** - Video kontrollieren
5. ✂️ **Upload** - Button klicken
6. ✅ **Fertig!** - Video ist jetzt mit der Übung verlinkt

## Workflow

**Schneller Workflow mit Video-Cutter App:**

1. Video-Cutter App (`http://localhost:5000`):

   - Video hochladen
   - Übung schneiden (z.B. "Sole Taps" von 14s-24s)
   - Download → `sole_taps_cut.mp4`
2. Admin Panel (`http://localhost:5001`):

   - "Sole Taps" Übung auswählen
   - `sole_taps_cut.mp4` hochladen
   - Fertig!
3. Build & Deploy:

   ```bash
   bash build.sh
   git add -A && git commit -m "Update: sole_taps video"
   git push origin main
   ```

## Dateiformat

Videos werden so gespeichert:

```
src/data/videos/{exercise_id}.mp4
```

Beispiele:

- `sole_taps.mp4`
- `football_dance.webm`
- `step_over.avi`

## Sicherheit

⚠️ **Wichtig**: Das Admin-Panel ist nur mit Passwort geschützt!

- ✅ Passwort in `server.py` ändern
- ✅ Nicht auf Public-Server deployen ohne HTTPS
- ✅ Für Production: Environment-Variable nutzen

```python
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')
```

## Troubleshooting

**"Passwort falsch"**

- Überprüfe Passwort in `server.py`
- Server neu starten

**"Video wird nicht gespeichert"**

- `src/data/videos/` existiert?
- Schreibberechtigung prüfen: `chmod 755 src/data/videos/`

**"exercises.json wird nicht aktualisiert"**

- Überprüfe JSON-Syntax
- Übungs-ID muss in exercises.json existieren

## Nächste Schritte

1. Alle Videos hochladen
2. `build.sh` ausführen
3. `git push` zum Deployen
4. Auf https://maregat.github.io/trainings-guide/ testen

---

**Alternativ:** Nutze die Video-Cutter App zum Schneiden + dieses Admin-Panel zum Hochladen = perfekter Workflow! 🚀
