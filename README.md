# Trainings-Guide – Fußball Garten-Übungen

Interaktive PWA für Fußball-Trainingsübungen (U11/U12, Kreisauswahl-Level).

**Features:**
- 📱 Funktioniert offline (auf dem Handy im Garten, kein WLAN nötig)
- 🎬 Video-Platzhalter für jede Übung
- 📊 Fehleranalyse, Coaching-Tipps, Progressionen für jede Übung
- 🎯 Strukturiert nach Warm-Up (Koordination + Coerver-Basis) + Technische Skills
- ⏱️ Zeiten, Setup, Skalierungen (leichter/schwerer)

---

## Struktur

```
trainings-guide/
  ├── data/
  │   └── exercises.json          # Alle Übungen (Basis + erweiterte Inhalte)
  ├── src/
  │   ├── index.html              # PWA Shell
  │   ├── app.js                  # Haupt-App Logic
  │   ├── sw.js                   # Service Worker (Offline)
  │   └── styles.css              # Styling
  ├── public/
  │   ├── manifest.json           # PWA Manifest
  │   └── icons/                  # App-Icons
  └── package.json
```

---

## Setup & Starten

```bash
# Abhängigkeiten installieren (später, wenn nötig)
npm install

# Lokal starten
npm run dev
```

PWA wird dann unter `http://localhost:5173` verfügbar.

**Auf iPhone installieren:**
1. Im Safari öffnen
2. "Zum Home-Bildschirm" hinzufügen → sieht aus wie eine echte App
3. Offline nutzbar!

---

## Status

- [x] Projekt-Struktur
- [x] `exercises.json` mit fundiertem Basis-Content
- [ ] PWA bauen (HTML/CSS/JS)
- [ ] Video-Integration später

---

*Entwickelt für [Name Tochter], U11/U12, Kreisauswahl* ⚽
