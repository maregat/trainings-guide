#!/bin/bash

# Synchronisiere src/ zu docs/ für GitHub Pages Deployment

echo "🔄 Synchronisiere src/ → docs/"
echo ""

# Copy HTML, JS, CSS
cp src/index.html docs/index.html && echo "✅ index.html"
cp src/app.js docs/app.js && echo "✅ app.js"
cp src/styles.css docs/styles.css && echo "✅ styles.css"
cp src/manifest.json docs/manifest.json 2>/dev/null && echo "✅ manifest.json" || echo "⚠️ manifest.json nicht gefunden"

# Copy data files
cp src/data/exercises.json docs/data/exercises.json && echo "✅ exercises.json"
cp src/data/workouts.json docs/data/workouts.json && echo "✅ workouts.json"
cp src/data/sessions.json docs/data/sessions.json && echo "✅ sessions.json"

echo ""
echo "✅ Synchronisierung abgeschlossen!"
echo ""
echo "Jetzt:"
echo "1. git add docs/"
echo "2. git commit -m 'Sync to GitHub Pages'"
echo "3. git push"
