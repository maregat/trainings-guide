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
