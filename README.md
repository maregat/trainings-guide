# 🎬 Trainings-Guide – Fußball Übungen

Interaktive **Progressive Web App (PWA)** für Fußball-Trainingsübungen mit Video-Support.

**Features:**
- 📱 **Offline-fähig** – Funktioniert ohne Internet (PWA mit Service Worker)
- 🎬 **Video-Übungen** – MP4-Videos lokal gehostet + YouTube/Vimeo-Einbindung
- 📊 **58 Übungen** – 9 Kategorien (ACL-Prävention, Coerver Fundamentals, etc.)
- 🎯 **Strukturiert** – Warm-Up, Ballkontrolle, Technische Skills, Taktik
- ⏱️ **Details** – Zeit, Setup, Ausrüstung, Fehleranalyse, Progressionen
- 🔐 **Admin Panel** – Videos direkt hochladen & mit Übungen verlinken

---

## 🚀 Starten

### Local Development

```bash
cd trainings-guide

# Admin-Panel starten (Port 5001)
source venv/bin/activate
python server.py
```

Dann öffnen: **http://localhost:5001/admin**

### Live auf GitHub Pages

https://maregat.github.io/trainings-guide/

---

## 📁 Struktur

```
trainings-guide/
  ├── src/
  │   ├── index.html                  # PWA Shell
  │   ├── app.js                      # SPA Logic (23KB)
  │   ├── sw.js                       # Service Worker v7 (Offline)
  │   ├── styles.css                  # Responsive Design
  │   ├── types.ts                    # TypeScript Typen
  │   └── data/
  │       ├── exercises.json          # 58 Übungen mit Metadaten
  │       └── videos/
  │           ├── *.mp4               # 23 lokal gehostete Videos
  │           └── *.jpg               # Video-Poster (Thumbnails)
  ├── templates/
  │   └── admin.html                  # Admin-Panel (Password-geschützt)
  ├── docs/                           # GitHub Pages (auto-deployed)
  ├── server.py                       # Flask Backend (Upload, API)
  ├── build.sh                        # Deploy-Automation (src/ → docs/)
  ├── venv/                           # Python Virtual Environment
  └── README.md                       # Diese Datei
```

---

## 🎬 Workflow: Videos Hochladen

### Empfohlener Workflow

1. Video mit **lossless-cut** schneiden
2. Admin-Panel öffnen: `http://localhost:5001/admin`
3. Passwort: `admin123` (in `server.py` ändern!)
4. Übung auswählen → Video hochladen → ✂️ Upload
5. Fertig! Video + Poster werden automatisch erstellt

### Alternative: Manuell mit build.sh

```bash
# 1. Video zu src/data/videos/{exercise_id}.mp4 kopieren
cp video.mp4 src/data/videos/new_exercise.mp4

# 2. exercises.json manuell aktualisieren
# (oder Admin-Panel nutzen)

# 3. Deployen
bash build.sh
git add -A && git commit -m "Update: new exercise"
git push origin main
```

---

## 📊 exercises.json Format

```json
{
  "exercises": {
    "sole_taps": {
      "name": "Sole Taps",
      "category": "warmup_coerver",
      "duration": 5,
      "videoLink": {
        "url": "./data/videos/sole_taps.mp4",
        "title": "Sole Taps"
      },
      "poster": "./data/videos/sole_taps.jpg",
      "setup": {
        "solo": true,
        "equipment": ["ball"],
        "space": "5x5m"
      },
      "coaching": "Berühre den Ball mit der Sohle, schnelle Füße...",
      "progressions": ["Mit zweitem Ball", "Rückwärts"]
    }
  }
}
```

---

## 🔐 Admin-Panel Setup

### Passwort ändern (WICHTIG!)

In `server.py` (Zeile ~18):

```python
ADMIN_PASSWORD = 'dein_sicheres_passwort_hier'  # Change me!
```

### Abhängigkeiten

```bash
pip install Flask Werkzeug
```

Oder mit venv:

```bash
python3 -m venv venv
source venv/bin/activate
pip install Flask Werkzeug
```

### API-Endpoints

- `GET /api/exercises` – Alle Übungen abrufen
- `POST /api/upload` – Video hochladen & verlinken
- `POST /api/delete/{exercise_id}` – Video & Poster löschen

---

## 📱 Auf iPhone installieren

1. Safari öffnen: https://maregat.github.io/trainings-guide/
2. Teilen-Button → "Zum Home-Bildschirm"
3. Icon nennen: "Trainings-Guide"
4. ✅ App ist jetzt wie eine native App nutzbar!

**Features auf iPhone:**
- ✅ Offline nutzbar (Downloads gecacht)
- ✅ Videos bleiben in App (kein Fullscreen-Zwang)
- ✅ Schnelle Warmladezeit

---

## 🔄 Deployment

### GitHub Pages (automatisch)

```bash
cd trainings-guide
bash build.sh                    # src/ → docs/ kopieren
git add -A
git commit -m "Update: neue Videos"
git push origin main
```

Live in ~30 Sekunden auf:
https://maregat.github.io/trainings-guide/

### Service Worker Cache-Invalidation

Der Service Worker (v7) cache:
- **Network-First**: `app.js`, `styles.css`, `index.html`, `exercises.json`
- **Cache-First**: Videos, Bilder, Poster

**Cache löschen bei Updates:**
1. `sw.js` Version hochzählen: `const CACHE_NAME = 'trainings-guide-v8'`
2. `build.sh && git push`
3. Alte Versionen werden automatisch gelöscht

---

## 🛠️ Technologie-Stack

| Teil | Tech |
|------|------|
| Frontend | Vanilla JavaScript (SPA) |
| Offline | Service Worker + PWA |
| Video-Hosting | Lokal (MP4) + YouTube/Vimeo |
| Admin-Backend | Flask (Python) |
| Poster-Gen | ffmpeg (automatisch) |
| Deploy | GitHub Pages |
| Dateiformat | JSON |

---

## ⚙️ Konfiguration

### Service Worker Version (Cache-Busting)

In `src/sw.js` (Zeile ~3):

```javascript
const CACHE_NAME = 'trainings-guide-v7';  // Increment to clear cache
```

### Video-Upload Limit

In `server.py` (Zeile ~22):

```python
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 * 1024  # 2GB
```

### Poster-Generierung

In `server.py` → `generate_poster()`:

```python
# Extrahiert Bild bei 0.5s mit ffmpeg
cmd = ['ffmpeg', '-i', video_path, '-ss', '0.5', '-vframes', '1', '-q:v', '2', output]
```

---

## 🐛 Troubleshooting

### Video wird nicht angezeigt
- Prüfen: `exercises.json` hat `videoLink.url` gesetzt?
- Browser-Cache löschen (oder Service Worker Version bumpen)

### Admin-Panel zeigt "Invalid password"
- Passwort in `server.py` überprüfen
- Server neu starten: `python server.py`

### exercises.json wird nicht aktualisiert
- Schreibberechtigung prüfen: `chmod 755 src/data/videos/`
- JSON-Syntax prüfen: `python -m json.tool src/data/exercises.json`

### Video wird hochgeladen aber nicht verlinkt
- ffmpeg installiert? `which ffmpeg`
- Übungs-ID existiert in exercises.json?

### Poster wird nicht generiert
- ffmpeg muss installiert sein
- Speicherplatz im `src/data/videos/` verfügbar?

---

## 📚 Tools & Ressourcen

- **Video-Schneiden**: [lossless-cut](https://github.com/mifi/lossless-cut) – Schnell, verlustfrei
- **PWA Dokumentation**: https://web.dev/progressive-web-apps/
- **Service Worker**: https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API
- **FFmpeg Poster**: `ffmpeg -i video.mp4 -ss 0.5 -vframes 1 -q:v 2 poster.jpg`

---

## 📋 Checklist: Neue Übung hinzufügen

- [ ] Video mit lossless-cut schneiden (~5-15 Sekunden)
- [ ] In exercises.json Basis-Struktur hinzufügen (oder Admin-Panel nutzen)
- [ ] Admin-Panel: Übung wählen → Video hochladen
- [ ] ✨ Poster wird automatisch erstellt
- [ ] `build.sh && git push` zum Deployen
- [ ] Testen auf https://maregat.github.io/trainings-guide/
- [ ] Auf iPhone Safari testen

---

**Entwickelt für modernes Fußball-Training 🎯⚽**
