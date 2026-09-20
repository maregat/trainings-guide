# Trainings-Guide Starten

## Schnelleinstieg

### Option 1: Mit Python (einfachste Lösung)

```bash
cd /home/mare/Nextcloud/Fussball/trainings-guide
python -m http.server 8000
```

Dann öffne: **http://localhost:8000/src/**

### Option 2: Mit Node.js (falls installiert)

```bash
cd trainings-guide
npx http-server src/
```

### Option 3: Mit Live Server (VS Code Extension)

1. Installiere "Live Server" in VS Code
2. Rechtsklick auf `src/index.html` → "Open with Live Server"

---

## Auf dem iPhone nutzen

1. **Öffne Safari** und gehe zu `http://<dein-computer-ip>:8000/src/`
2. **Teile-Button** → "Zum Home-Bildschirm"
3. Die App ist jetzt auf deinem Home-Screen wie eine echte App
4. **Funktioniert offline!** (nach dem ersten Laden)

---

## Projekt-Struktur

```
trainings-guide/
├── src/
│   ├── index.html      ← Die App öffnen
│   ├── app.js          ← Hauptlogik
│   ├── sw.js           ← Service Worker (Offline)
│   └── styles.css      ← Styling
├── data/
│   └── exercises.json  ← Alle Übungen & Inhalte
├── public/
│   └── manifest.json   ← PWA-Konfiguration
└── README.md
```

---

## Entwicklung

### Neue Übung hinzufügen

Bearbeite `data/exercises.json` und füge einen neuen Exercise-Block ein:

```json
{
  "id": "unique_id",
  "category": "warmup",
  "subCategory": "coordination",
  "name": "Übungs-Name",
  "order": 1,
  "description": "...",
  "duration": "...",
  "setup": { ... },
  "technique": { ... },
  "commonMistakes": [ ... ],
  "coachingTips": { ... },
  "progressionPath": [ ... ],
  "videoPlaceholder": { "url": null, "duration": "0:20-0:30" }
}
```

Die App lädt die Datei automatisch nach Reload.

### Video einbinden

Später: Ersetze `"url": null` mit der tatsächlichen Video-URL.

---

## Browser-Unterstützung

- ✅ Safari (iPhone/Mac)
- ✅ Chrome (Android/Mac/Windows)
- ✅ Firefox
- ⚠️ Edge

---

## Tipps

- **Offline**: App lädt die Übungen einmal, dann funktioniert sie ohne Internet
- **Responsive**: Optimiert für kleine Handy-Bildschirme
- **Touch-freundlich**: Große Buttons, keine Scroll-Probleme

---

Viel Erfolg beim Training! ⚽
