#!/usr/bin/env python3
"""
Video Upload Server für Trainings-Guide
Admin-Backend für Video-Verwaltung
"""

import os
import json
import mimetypes
import subprocess
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'src/data/videos'
ALLOWED_EXTENSIONS = {'mp4', 'webm', 'avi', 'mov', 'mkv'}
ADMIN_PASSWORD = 'admin123'  # Change this!

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 * 1024  # 2GB

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def sanitize_filename(filename):
    """Convert filename to safe format (lowercase, underscores)"""
    name = Path(filename).stem
    ext = Path(filename).suffix.lower()
    # Replace spaces and special chars with underscores
    safe_name = ''.join(c if c.isalnum() else '_' for c in name).lower()
    return safe_name + ext

def generate_poster(video_path, exercise_id):
    """Generate JPG poster from first frame of video using ffmpeg"""
    try:
        poster_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{exercise_id}.jpg")
        
        # Use ffmpeg to extract first frame at 0.5 seconds
        cmd = [
            'ffmpeg', '-i', video_path,
            '-ss', '0.5',
            '-vframes', '1',
            '-q:v', '2',
            '-y',  # Overwrite
            poster_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and os.path.exists(poster_path):
            return f"./data/videos/{exercise_id}.jpg"
        else:
            print(f"Warning: Failed to generate poster for {exercise_id}")
            return None
    except Exception as e:
        print(f"Error generating poster: {e}")
        return None

@app.route('/')
@app.route('/admin')
def admin():
    """Serve the admin panel"""
    return render_template('admin.html')

@app.route('/api/exercises', methods=['GET'])
def get_exercises():
    """Get all exercises from exercises.json"""
    try:
        with open('src/data/exercises.json') as f:
            data = json.load(f)
        
        # Return full exercise data for editing
        exercises = []
        for ex_id, exercise in data['exercises'].items():
            exercises.append({
                'id': ex_id,
                'name': exercise.get('name', ''),
                'category': exercise.get('category', ''),
                'description': exercise.get('description', ''),
                'duration': exercise.get('duration', ''),
                'videoLink': exercise.get('videoLink', {'url': None, 'title': None}),
                'poster': exercise.get('poster', None)
            })
        
        # Return exercises sorted by category, then by name
        return jsonify({
            'exercises': sorted(exercises, key=lambda x: (x.get('category', ''), x.get('name', ''))),
            'categories': data.get('categories', {})
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/exercises/<exercise_id>', methods=['GET'])
def get_exercise(exercise_id):
    """Get single exercise"""
    try:
        with open('src/data/exercises.json') as f:
            data = json.load(f)
        
        if exercise_id not in data['exercises']:
            return jsonify({'error': 'Exercise not found'}), 404
        
        return jsonify({'exercise': data['exercises'][exercise_id]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/exercises', methods=['POST'])
def create_exercise():
    """Create new exercise"""
    try:
        password = request.json.get('password', '')
        if password != ADMIN_PASSWORD:
            return jsonify({'error': 'Invalid password'}), 403
        
        exercise_data = request.json
        exercise_id = exercise_data.get('id', '')
        
        if not exercise_id or not exercise_data.get('name', ''):
            return jsonify({'error': 'ID and name required'}), 400
        
        with open('src/data/exercises.json', 'r') as f:
            data = json.load(f)
        
        if exercise_id in data['exercises']:
            return jsonify({'error': 'Exercise ID already exists'}), 409
        
        # Create new exercise
        new_exercise = {
            'id': exercise_id,
            'name': exercise_data.get('name', ''),
            'category': exercise_data.get('category', ''),
            'description': exercise_data.get('description', ''),
            'duration': exercise_data.get('duration', ''),
            'videoLink': {'url': None, 'title': None},
            'poster': None
        }
        
        data['exercises'][exercise_id] = new_exercise
        
        with open('src/data/exercises.json', 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return jsonify({'success': True, 'exercise': new_exercise})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/exercises/<exercise_id>', methods=['PUT'])
def update_exercise(exercise_id):
    """Update exercise metadata (not video)"""
    try:
        password = request.json.get('password', '')
        if password != ADMIN_PASSWORD:
            return jsonify({'error': 'Invalid password'}), 403
        
        exercise_data = request.json
        
        with open('src/data/exercises.json', 'r') as f:
            data = json.load(f)
        
        if exercise_id not in data['exercises']:
            return jsonify({'error': 'Exercise not found'}), 404
        
        # Update allowed fields only
        allowed_fields = ['name', 'category', 'description', 'duration']
        for field in allowed_fields:
            if field in exercise_data:
                data['exercises'][exercise_id][field] = exercise_data[field]
        
        with open('src/data/exercises.json', 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return jsonify({'success': True, 'exercise': data['exercises'][exercise_id]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload_video():
    """Upload video and update exercises.json"""
    try:
        # Check password
        password = request.form.get('password', '')
        if password != ADMIN_PASSWORD:
            return jsonify({'error': 'Invalid password'}), 403
        
        # Check files
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        exercise_id = request.form.get('exercise_id', '')
        if not exercise_id:
            return jsonify({'error': 'No exercise selected'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        # Generate safe filename
        ext = Path(file.filename).suffix.lower()
        safe_filename = f"{exercise_id}{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
        
        # Save file
        file.save(filepath)
        file_size = os.path.getsize(filepath)
        
        # Generate poster from first frame
        poster_url = generate_poster(filepath, exercise_id)
        
        # Update exercises.json
        with open('src/data/exercises.json', 'r') as f:
            data = json.load(f)
        
        if exercise_id not in data['exercises']:
            return jsonify({'error': 'Exercise not found'}), 404
        
        # Set video URL
        video_url = f"./data/videos/{safe_filename}"
        data['exercises'][exercise_id]['videoLink'] = {
            'url': video_url,
            'title': data['exercises'][exercise_id]['name']
        }
        
        # Set poster URL if generated
        if poster_url:
            data['exercises'][exercise_id]['poster'] = poster_url
        
        # Save updated exercises.json
        with open('src/data/exercises.json', 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return jsonify({
            'success': True,
            'filename': safe_filename,
            'url': video_url,
            'poster': poster_url,
            'size_mb': round(file_size / (1024 * 1024), 2),
            'message': f"✅ Video uploaded and linked to exercise!"
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/exercises/<exercise_id>', methods=['DELETE'])
def delete_exercise(exercise_id):
    """Delete exercise (metadata AND video files)"""
    try:
        password = request.json.get('password', '')
        if password != ADMIN_PASSWORD:
            return jsonify({'error': 'Invalid password'}), 403
        
        with open('src/data/exercises.json', 'r') as f:
            data = json.load(f)
        
        if exercise_id not in data['exercises']:
            return jsonify({'error': 'Exercise not found'}), 404
        
        # Delete video file
        current_video = data['exercises'][exercise_id].get('videoLink', {}).get('url', '')
        if current_video and current_video.startswith('./data/videos/'):
            video_filename = current_video.replace('./data/videos/', '')
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
            if os.path.exists(video_path):
                os.remove(video_path)
        
        # Delete poster file
        poster_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{exercise_id}.jpg")
        if os.path.exists(poster_path):
            os.remove(poster_path)
        
        # Delete from JSON
        del data['exercises'][exercise_id]
        
        with open('src/data/exercises.json', 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return jsonify({'success': True, 'message': 'Exercise deleted'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cleanup', methods=['POST'])
def cleanup_unused_videos():
    """Delete all video files that are not linked in exercises.json"""
    try:
        password = request.json.get('password', '')
        if password != ADMIN_PASSWORD:
            return jsonify({'error': 'Invalid password'}), 403
        
        # Load exercises
        with open('src/data/exercises.json', 'r') as f:
            data = json.load(f)
        
        # Collect all linked video files
        linked_files = set()
        for exercise in data['exercises'].values():
            video_url = exercise.get('videoLink', {}).get('url', '')
            if video_url and video_url.startswith('./data/videos/'):
                filename = video_url.replace('./data/videos/', '')
                linked_files.add(filename)
            
            # Also check poster files
            exercise_id = exercise.get('id', '')
            if exercise_id:
                linked_files.add(f"{exercise_id}.jpg")
        
        # Find all video files (mp4, webm, avi, etc.)
        video_extensions = {'.mp4', '.webm', '.avi', '.mov', '.mkv'}
        poster_extensions = {'.jpg', '.png'}
        
        all_files = []
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.isfile(filepath):
                ext = os.path.splitext(filename)[1].lower()
                if ext in video_extensions or ext in poster_extensions:
                    all_files.append(filename)
        
        # Find unused files
        unused_files = []
        for filename in all_files:
            if filename not in linked_files:
                unused_files.append(filename)
        
        # Delete unused files
        deleted_count = 0
        deleted_files = []
        for filename in unused_files:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                os.remove(filepath)
                deleted_count += 1
                deleted_files.append(filename)
            except Exception as e:
                pass
        
        # Calculate freed space
        freed_space_mb = sum(
            os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'], f)) / 1024 / 1024
            for f in deleted_files if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], f))
        )
        
        return jsonify({
            'success': True,
            'deleted_count': deleted_count,
            'deleted_files': deleted_files,
            'linked_count': len(linked_files),
            'total_files': len(all_files),
            'message': f'✅ {deleted_count} ungenutzte Dateien gelöscht'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ CATEGORY MANAGEMENT ============

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all categories with exercise counts"""
    try:
        with open('src/data/exercises.json', 'r') as f:
            data = json.load(f)
        
        categories = data.get('categories', {})
        exercises = data.get('exercises', {})
        
        # Count exercises per category
        category_counts = {}
        for ex_id, ex in exercises.items():
            cat = ex.get('category', '')
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        # Build response with counts
        result = {}
        for cat_id, cat_data in categories.items():
            result[cat_id] = {
                'id': cat_id,
                'name': cat_data.get('name', ''),
                'description': cat_data.get('description', ''),
                'order': cat_data.get('order', 999),
                'phase': cat_data.get('phase', ''),
                'exercise_count': category_counts.get(cat_id, 0)
            }
        
        return jsonify({'categories': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories', methods=['POST'])
def create_category():
    """Create new category"""
    try:
        password = request.json.get('password', '')
        if password != ADMIN_PASSWORD:
            return jsonify({'error': 'Invalid password'}), 403
        
        cat_id = request.json.get('id', '').strip()
        cat_name = request.json.get('name', '').strip()
        
        if not cat_id or not cat_name:
            return jsonify({'error': 'ID and name required'}), 400
        
        # Sanitize ID
        cat_id = ''.join(c if c.isalnum() or c == '_' else '_' for c in cat_id).lower()
        
        with open('src/data/exercises.json', 'r') as f:
            data = json.load(f)
        
        if cat_id in data['categories']:
            return jsonify({'error': 'Category ID already exists'}), 409
        
        # Create new category
        new_category = {
            'name': cat_name,
            'description': request.json.get('description', ''),
            'order': max([c.get('order', 0) for c in data['categories'].values()] + [0]) + 1,
            'phase': request.json.get('phase', 'main')
        }
        
        data['categories'][cat_id] = new_category
        
        with open('src/data/exercises.json', 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return jsonify({'success': True, 'category_id': cat_id, 'category': new_category})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories/<category_id>', methods=['PUT'])
def update_category(category_id):
    """Update category metadata"""
    try:
        password = request.json.get('password', '')
        if password != ADMIN_PASSWORD:
            return jsonify({'error': 'Invalid password'}), 403
        
        with open('src/data/exercises.json', 'r') as f:
            data = json.load(f)
        
        if category_id not in data['categories']:
            return jsonify({'error': 'Category not found'}), 404
        
        # Update fields
        data['categories'][category_id]['name'] = request.json.get('name', data['categories'][category_id].get('name', ''))
        data['categories'][category_id]['description'] = request.json.get('description', data['categories'][category_id].get('description', ''))
        
        if 'order' in request.json:
            data['categories'][category_id]['order'] = request.json.get('order')
        
        with open('src/data/exercises.json', 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return jsonify({'success': True, 'category': data['categories'][category_id]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories/<category_id>', methods=['DELETE'])
def delete_category(category_id):
    """Delete category and move exercises to another category"""
    try:
        password = request.json.get('password', '')
        if password != ADMIN_PASSWORD:
            return jsonify({'error': 'Invalid password'}), 403
        
        target_category = request.json.get('target_category', '')
        
        with open('src/data/exercises.json', 'r') as f:
            data = json.load(f)
        
        # Validation
        if category_id not in data['categories']:
            return jsonify({'error': 'Category not found'}), 404
        
        if len(data['categories']) <= 1:
            return jsonify({'error': 'Cannot delete last category'}), 400
        
        if not target_category or target_category == category_id:
            return jsonify({'error': 'Target category required'}), 400
        
        if target_category not in data['categories']:
            return jsonify({'error': 'Target category not found'}), 404
        
        # Find exercises in this category
        exercises_to_move = [ex_id for ex_id, ex in data['exercises'].items() 
                            if ex.get('category') == category_id]
        
        # Move all exercises to target category
        for ex_id in exercises_to_move:
            data['exercises'][ex_id]['category'] = target_category
        
        # Delete category
        del data['categories'][category_id]
        
        with open('src/data/exercises.json', 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return jsonify({
            'success': True,
            'message': f'✅ Kategorie gelöscht, {len(exercises_to_move)} Übungen verschoben',
            'moved_count': len(exercises_to_move)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🎬 Admin Server starting...")
    print("📱 Open http://localhost:5001/admin in your browser")
    print("🔐 Password: admin123 (change in server.py!)")
    app.run(debug=True, port=5001)
