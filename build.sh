#!/bin/bash

# ============================================
# Trainings-Guide Build Script
# Kopiert alle Dateien von src/ + app/ zu docs/ für GitHub Pages Deployment
# ============================================

set -e  # Exit on error

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                    🔨 BUILD SCRIPT - STARTING                      ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# ============================================
# Cleanup docs/
# ============================================

echo "📋 Step 1: Cleanup /docs (alte Deployment-Dateien löschen)"
echo "─────────────────────────────────────────────────────────────────"

# Lösche alle Dateien in docs/ außer .git
rm -f ./docs/index.html
rm -f ./docs/app.js
rm -f ./docs/styles.css
rm -f ./docs/sw.js
rm -f ./docs/manifest.json
rm -rf ./docs/data
rm -rf ./docs/videos

echo "✅ /docs bereinigt"
echo ""

# ============================================
# Copy src files
# ============================================

echo "📋 Step 2: Copy src/ → /docs (Komplette Anwendung)"
echo "─────────────────────────────────────────────────────────────────"

cp ./src/index.html ./docs/index.html
echo "   ✅ index.html"

cp ./src/app.js ./docs/app.js
echo "   ✅ app.js"

cp ./src/styles.css ./docs/styles.css
echo "   ✅ styles.css"

cp ./src/sw.js ./docs/sw.js
echo "   ✅ sw.js"

cp ./src/manifest.json ./docs/manifest.json
echo "   ✅ manifest.json"

echo "✅ App-Dateien kopiert"
echo ""

# ============================================
# Copy data files
# ============================================

echo "📋 Step 3: Copy src/data/ → /docs/data (Daten)"
echo "─────────────────────────────────────────────────────────────────"

mkdir -p ./docs/data

cp ./src/data/exercises.json ./docs/data/exercises.json
echo "   ✅ exercises.json ($(wc -c < ./docs/data/exercises.json) bytes)"

# Kopiere Videos (falls vorhanden)
if [ -d ./src/data/videos ]; then
    mkdir -p ./docs/data/videos
    cp -r ./src/data/videos/* ./docs/data/videos/ 2>/dev/null || true
    video_count=$(find ./docs/data/videos -type f | wc -l)
    if [ "$video_count" -gt 0 ]; then
        echo "   ✅ Videos ($video_count Dateien)"
    fi
fi

echo "✅ Daten-Dateien kopiert"
echo ""

# ============================================
# Verification
# ============================================

echo "📋 Step 4: Verification (überprüfe dass alles da ist)"
echo "─────────────────────────────────────────────────────────────────"

required_files=(
    "./docs/index.html"
    "./docs/app.js"
    "./docs/styles.css"
    "./docs/sw.js"
    "./docs/manifest.json"
    "./docs/data/exercises.json"
)

all_good=true
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        size=$(wc -c < "$file")
        printf "   ✅ %-30s (%d bytes)\n" "$file" "$size"
    else
        echo "   ❌ $file MISSING!"
        all_good=false
    fi
done

echo ""

if [ "$all_good" = true ]; then
    echo "╔════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                    ║"
    echo "║        ✅ BUILD COMPLETE - docs/ is ready for GitHub Pages         ║"
    echo "║                                                                    ║"
    echo "║        Next steps:                                                 ║"
    echo "║        $ git add -A                                                ║"
    echo "║        $ git commit -m 'Deploy: New architecture'                 ║"
    echo "║        $ git push origin main                                      ║"
    echo "║                                                                    ║"
    echo "╚════════════════════════════════════════════════════════════════════╝"
    echo ""
    exit 0
else
    echo "╔════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                    ║"
    echo "║        ❌ BUILD FAILED - Some files are missing!                   ║"
    echo "║                                                                    ║"
    echo "╚════════════════════════════════════════════════════════════════════╝"
    echo ""
    exit 1
fi
