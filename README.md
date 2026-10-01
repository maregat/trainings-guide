# 🎬 Trainings-Guide – Fußball Übungen

Interaktive **Progressive Web App (PWA)** für Fußball-Trainingsübungen mit Video-Support und Admin-Panel.

**Features:**

- 📱 **Offline-fähig** – Funktioniert ohne Internet (PWA mit Service Worker v7)
- 🎬 **Video-Übungen** – MP4-Videos lokal gehostet + YouTube/Vimeo-Einbindung
- 📊 **58 Übungen** – 9 Kategorien (ACL-Prävention, Coerver Fundamentals, etc.)
- 🎯 **Strukturiert** – Warm-Up, Ballkontrolle, Technische Skills, Taktik
- ⏱️ **Details** – Name, Kategorie, Beschreibung, Dauer, Video, Poster
- 🔐 **Admin Panel** – Vollständiges CRUD für Übungen + Video-Upload mit Auto-Poster
- 🔍 **Kategorie-Filter** – Übungen nach Kategorie filtern

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

## 🎬 Admin-Panel: Übungen verwalten

### Starten

```bash
cd trainings-guide
./venv/bin/python3 server.py
```

Dann öffnen: **http://localhost:5001/admin**

**Login-Daten:**

- 🔐 Passwort: `admin123` (in `server.py` Zeile 20 ändern!)

### Features

#### 📋 Exercises Tab

- ✏️ **Edit** – Übung bearbeiten (Name, Kategorie, Beschreibung, Dauer)
- ➕ **Add** – Neue Übung mit eindeutiger ID erstellen
- 🗑️ **Delete** – Übung + Video + Poster löschen
- 🔍 **Filter** – Übungen nach Kategorie filtern + Reset-Button

#### 🎥 Videos Tab

- 📹 **Select Exercise** – Dropdown mit allen 58 Übungen
- 💾 **Upload Video** – Drag & Drop oder Dateiauswahl
- ✂️ **Auto-Poster** – JPG-Thumbnail wird automatisch generiert
- 📊 **Status** – Dateiname und Größe anzeigen

---

## 🎬 Workflow: Videos Hochladen

### Mit Admin-Panel (empfohlen)

1. Admin-Panel öffnen: `http://localhost:5001/admin`
2. Passwort eingeben
3. **Tab "Exercises"** – Übungen nach Bedarf bearbeiten
4. **Tab "Videos"** – Übung auswählen → Video hochladen
5. ✅ Fertig! Video + Poster + exercises.json werden automatisch aktualisiert

### Mit build.sh (manuell)

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

## 📊 exercises.json Format (Simplifiziert)

Die neue Struktur fokussiert auf **essenzielle Felder nur**:

```json
{
  "categories": {
    "warmup_coerver": {
      "name": "🎯 Coerver Fundamentals",
      "description": "Ball-Fundamentals und Fußballtechnik",
      "order": 1,
      "phase": "warmup"
    }
  },
  "exercises": [
    {
      "id": "sole_taps",
      "name": "Sole Taps",
      "category": "warmup_coerver",
      "description": "Berühre den Ball mit der Sohle. Schnelle, rhythmische Bewegungen.",
      "duration": "5 min",
      "videoLink": {
        "url": "./data/videos/sole_taps.mp4",
        "title": "Sole Taps"
      },
      "poster": "./data/videos/sole_taps.jpg"
    }
  ]
}
```

**Felder pro Übung (7):**

1. `id` – Eindeutige ID (z.B. "sole_taps")
2. `name` – Übungs-Name
3. `category` – Kategorie-ID (z.B. "warmup_coerver")
4. `description` – Kurzbeschreibung
5. `duration` – Dauer (z.B. "5 min")
6. `videoLink` – Video-Objekt mit URL + Titel
7. `poster` – Thumbnail-Pfad (auto-generiert beim Upload)

---

## � Backend API (server.py)

Port: **5001** (Nur lokal, nicht auf GitHub Pages)

### Alle Übungen laden

```
GET /api/exercises
Response: { "categories": {...}, "exercises": [...] }
```

### Einzelne Übung laden (zum Bearbeiten)

```
GET /api/exercises/{exercise_id}
Response: { "exercise": {...} }
```

### Neue Übung erstellen

```
POST /api/exercises
Body: {
  "password": "admin123",
  "id": "neue_ubung",
  "name": "Neue Übung",
  "category": "warmup_coerver",
  "description": "Beschreibung",
  "duration": "5 min"
}
Response: { "exercise": {...}, "success": true }
```

### Übung aktualisieren

```
PUT /api/exercises/{exercise_id}
Body: {
  "password": "admin123",
  "name": "Neuer Name",
  "category": "acl_prevention",
  "description": "Neue Beschreibung",
  "duration": "10 min"
}
Response: { "exercise": {...}, "success": true }
```

### Übung löschen (+ Video + Poster)

```
DELETE /api/exercises/{exercise_id}
Body: { "password": "admin123" }
Response: { "success": true, "deleted": true }
```

### Video hochladen & Poster generieren

```
POST /api/upload
Body: (multipart/form-data)
  - file: <video.mp4>
  - exercise_id: "sole_taps"
  - password: "admin123"
Response: {
  "success": true,
  "url": "./data/videos/sole_taps.mp4",
  "poster": "./data/videos/sole_taps.jpg",
  "size_mb": 2.5
}
```

---

## 🔐 Sicherheit

### Passwort-Schutz

- Alle `POST`, `PUT`, `DELETE` Requests benötigen `password` im Body
- Standard: `admin123` (in `server.py` Zeile 20 ändern!)
- ⚠️ **WICHTIG**: Ändern Sie das Passwort vor dem Deployment in der Produktion!

### CORS & Requests

- Admin-Panel: Lokal auf `http://localhost:5001/admin`
- App: Wird von GitHub Pages gehostet, hat keinen Zugriff auf Port 5001
- Deshalb: Admin-Panel nur lokal verwenden!

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

**Was wird deployed:**

- `src/index.html` → `docs/index.html`
- `src/app.js` → `docs/app.js`
- `src/styles.css` → `docs/styles.css`
- `src/sw.js` → `docs/sw.js`
- `src/manifest.json` → `docs/manifest.json`
- `src/data/exercises.json` → `docs/data/exercises.json`
- `src/data/videos/*` → `docs/data/videos/*`
- `templates/admin.html` → `docs/admin.html` (für lokale Verwaltung)

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

| Teil          | Tech                        |
| ------------- | --------------------------- |
| Frontend      | Vanilla JavaScript (SPA)    |
| Offline       | Service Worker + PWA        |
| Video-Hosting | Lokal (MP4) + YouTube/Vimeo |
| Admin-Backend | Flask (Python)              |
| Poster-Gen    | ffmpeg (automatisch)        |
| Deploy        | GitHub Pages                |
| Dateiformat   | JSON                        |

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
