let exercisesData = null;
let currentView = 'categories';
let currentCategory = null;
let currentExerciseId = null;

const elements = {
    app: document.getElementById('app'),
    categoryView: document.getElementById('category-view'),
    exerciseView: document.getElementById('exercise-view'),
    videoView: document.getElementById('video-view'),
    categoriesContainer: document.querySelector('.categories-container'),
    exerciseContainer: document.querySelector('.exercise-container'),
    sidebar: document.getElementById('sidebar'),
    categoriesNav: document.getElementById('categories-nav'),
    menuBtn: document.getElementById('menu-btn'),
    closeMenuBtn: document.getElementById('close-menu'),
    backBtn: document.getElementById('back-btn'),
    loading: document.getElementById('loading'),
    videoTitle: document.getElementById('video-title')
};

// ============================================
// Initialisierung
// ============================================

async function init() {
    try {
        showLoading();
        
        // Initialize workout elements first
        initWorkoutElements();
        
        // Lade exercises.json mit Version-Busting (v6)
        const response = await fetch('./data/exercises.json?v=7&t=' + Date.now());
        if (!response.ok) throw new Error('Fehler beim Laden von exercises.json');
        
        exercisesData = await response.json();
        
        // Setup Event Listener
        setupEventListeners();
        
        // Render Categories
        renderCategories();
        renderSidebar();
        
        hideLoading();
    } catch (error) {
        console.error('Init Error:', error);
        hideLoading();
        showError('Fehler beim Laden der Daten. Bitte laden Sie die Seite neu.');
    }
}

function setupEventListeners() {
    elements.menuBtn.addEventListener('click', () => {
        elements.sidebar.classList.add('open');
    });
    
    elements.closeMenuBtn.addEventListener('click', () => {
        elements.sidebar.classList.remove('open');
    });
    
    elements.backBtn.addEventListener('click', goBack);
    
    // Overlay zum Schließen der Sidebar
    document.addEventListener('click', (e) => {
        if (elements.sidebar.classList.contains('open') &&
            !elements.sidebar.contains(e.target) &&
            !elements.menuBtn.contains(e.target)) {
            elements.sidebar.classList.remove('open');
        }
    });
}

// Pull-to-Refresh Functionality
let pullStartY = 0;
let isPulling = false;



function renderCategories() {
    const categories = exercisesData.categories;
    
    elements.categoriesContainer.innerHTML = '';
    
    Object.entries(categories).forEach(([key, category]) => {
        const exercisesInCategory = getExercisesInCategory(key);
        
        const card = document.createElement('div');
        card.className = 'category-card';
        card.innerHTML = `
            <div class="category-icon">${getCategoryIcon(key)}</div>
            <div class="category-name">${category.name}</div>
            <div class="category-count">${exercisesInCategory.length} Übungen</div>
        `;
        
        card.addEventListener('click', () => {
            currentCategory = key;
            renderExerciseList(key);
        });
        
        elements.categoriesContainer.appendChild(card);
    });
}

function renderSidebar() {
    const categories = exercisesData.categories;
    
    elements.categoriesNav.innerHTML = '';
    
    Object.entries(categories).forEach(([key, category]) => {
        const exercisesInCategory = getExercisesInCategory(key);
        
        const navItem = document.createElement('div');
        navItem.className = 'nav-category';
        navItem.innerHTML = `
            <div class="nav-category-name">${getCategoryIcon(key)} ${category.name}</div>
            <div class="nav-category-count">${exercisesInCategory.length} Übungen</div>
        `;
        
        navItem.addEventListener('click', () => {
            currentCategory = key;
            renderExerciseList(key);
            elements.sidebar.classList.remove('open');
        });
        
        elements.categoriesNav.appendChild(navItem);
    });
}

// ============================================
// Views: Übungs-Liste
// ============================================

function renderExerciseList(categoryKey) {
    const exercises = getExercisesInCategory(categoryKey);
    const category = exercisesData.categories[categoryKey];
    
    showView('category');
    elements.categoriesContainer.innerHTML = '';
    
    // Tabs Container
    const tabsContainer = document.createElement('div');
    tabsContainer.className = 'exercise-tabs';
    
    // Alle Kategorien als Tabs
    Object.entries(exercisesData.categories).forEach(([key, cat]) => {
        const tab = document.createElement('button');
        tab.className = 'exercise-tab';
        if (key === categoryKey) {
            tab.classList.add('active');
        }
        tab.innerHTML = `${getCategoryIcon(key)}<span>${cat.name}</span>`;
        tab.addEventListener('click', () => {
            renderExerciseList(key);
        });
        tabsContainer.appendChild(tab);
    });
    
    elements.categoriesContainer.appendChild(tabsContainer);
    
    // Übungen darunter
    const exercisesList = document.createElement('div');
    exercisesList.className = 'exercises-list';
    
    exercises.forEach(exercise => {
        const item = document.createElement('div');
        item.className = 'exercise-item';
        const partnerIcon = exercise.isPartnerExercise ? '👥 ' : '';
        item.innerHTML = `
            <div style="text-align: left;">
                <div class="exercise-item-name">
                    ${partnerIcon}${exercise.name}
                </div>
                <div class="exercise-item-meta">
                    ⏱️ ${exercise.duration || 'N/A'}
                </div>
            </div>
        `;
        
        item.addEventListener('click', () => {
            renderExerciseDetail(exercise.id);
        });
        
        exercisesList.appendChild(item);
    });
    
    elements.categoriesContainer.appendChild(exercisesList);
    
    // Back Button zeigen
    elements.backBtn.classList.remove('hidden');
    currentView = 'exerciseList';
}

// ============================================
// Views: Übungs-Detail
// ============================================

function renderExerciseDetail(exerciseId) {
    const exercise = exercisesData.exercises[exerciseId];
    if (!exercise) return;
    
    currentExerciseId = exerciseId;
    
    showView('exercise');
    
    const partnerIcon = exercise.isPartnerExercise ? '👥 ' : '';
    
    let html = `
        <div class="exercise-header">
            <h1 class="exercise-title">${partnerIcon}${exercise.name}</h1>
            <div class="exercise-meta">
                <div class="meta-item">⏱️ ${exercise.duration || 'N/A'}</div>
            </div>
        </div>
        
        <div class="section-content">
            <p style="color: var(--color-text-secondary); margin-bottom: 1rem;">${exercise.description}</p>
        </div>
    `;
    
    // Video Link
    if (exercise.videoLink) {
        if (exercise.videoLink.url) {
            const videoUrl = exercise.videoLink.url;
            
            // Prüfe ob lokale MP4-Datei (HTML5 Video Player)
            if (videoUrl.includes('.mp4') || videoUrl.includes('./data/videos')) {
                const videoId = 'video-' + exercise.id;
                // Poster URL: gleiche wie Video, aber .jpg statt .mp4
                const posterUrl = videoUrl.replace(/\.mp4$/, '.jpg');
                html += `
                    <div style="padding: 0 1.5rem; margin-bottom: 1.5rem;">
                        <div style="position: relative; width: 100%; max-width: 100%; aspect-ratio: 16 / 9; background: #000; border-radius: 8px; overflow: hidden;">
                            <video 
                                id="${videoId}"
                                controls 
                                loop
                                muted
                                playsinline
                                webkit-playsinline
                                x5-playsinline
                                disablePictureInPicture
                                poster="${posterUrl}"
                                style="width: 100%; height: 100%; display: block; object-fit: contain;"
                                preload="metadata">
                                <source src="${videoUrl}" type="video/mp4">
                                Dein Browser unterstützt HTML5 Video nicht.
                            </video>
                        </div>
                    </div>
                    <script>
                        (function() {
                            const vid = document.getElementById('${videoId}');
                            if (vid) {
                                vid.addEventListener('fullscreenchange', (e) => {
                                    if (document.fullscreenElement) {
                                        document.exitFullscreen().catch(() => {});
                                    }
                                });
                                vid.addEventListener('webkitfullscreenchange', (e) => {
                                    if (document.webkitFullscreenElement) {
                                        document.webkitExitFullscreen?.();
                                    }
                                });
                            }
                        })();
                    </script>
                `;
            }
            // Prüfe ob Vimeo
            else if (videoUrl.includes('vimeo.com')) {
                // Vimeo: Video einbetten
                // URL-Format: https://vimeo.com/1051337825/514bb750ce
                // Embed-Format: https://player.vimeo.com/video/1051337825?h=514bb750ce
                const vimeoMatch = videoUrl.match(/vimeo\.com\/(\d+)(?:\/([a-f0-9]+))?/);
                if (vimeoMatch) {
                    const videoId = vimeoMatch[1];
                    const token = vimeoMatch[2];
                    const embedUrl = token 
                        ? `https://player.vimeo.com/video/${videoId}?h=${token}&muted=1`
                        : `https://player.vimeo.com/video/${videoId}?muted=1`;
                    
                    html += `
                        <div style="padding: 0 1.5rem; margin-bottom: 1.5rem;">
                            <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: 8px;">
                                <iframe 
                                    src="${embedUrl}" 
                                    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; border-radius: 8px;"
                                    allow="autoplay; fullscreen; picture-in-picture" 
                                    allowfullscreen>
                                </iframe>
                            </div>
                            <div style="margin-top: 0.75rem; font-size: 0.85rem;">
                                <a href="${videoUrl}" target="_blank" style="color: #0066cc; text-decoration: none;">🔗 Video auf Vimeo öffnen</a>
                            </div>
                        </div>
                    `;
                }
            }
            // YouTube oder andere Links
            else {
                html += `
                    <div style="padding: 0 1.5rem; margin-bottom: 1.5rem;">
                        <a href="${videoUrl}" target="_blank" style="display: inline-block; padding: 0.75rem 1.5rem; background: #ff0000; color: white; text-decoration: none; border-radius: 6px; font-weight: bold; cursor: pointer;">
                            🎥 Video anschauen
                        </a>
                    </div>
                `;
            }
        } else {
            // Platzhalter für später
            html += `
                <div style="padding: 0 1.5rem;">
                    <div class="video-placeholder">
                        <div class="video-icon">🎬</div>
                        <p>Video folgt in Kürze</p>
                    </div>
                </div>
            `;
        }
    }
    
    // Aufbau / Setup
    if (exercise.setup) {
        html += `
            <div class="section-header">🎒 Aufbau</div>
            <div class="section-content">
                <div class="content-item">
                    <div class="content-label">Material</div>
                    <div>
                        ${exercise.setup.equipment.map(e => `<div class="list-item">${e}</div>`).join('')}
                    </div>
                </div>
                <div class="content-item">
                    <div class="content-label">Platz</div>
                    <div class="content-text">${exercise.setup.space}</div>
                </div>
            </div>
        `;
    }
    
    // Technique
    if (exercise.technique) {
        html += `
            <div class="section-header">🎯 Technik</div>
            <div class="section-content">
                <div class="content-item">
                    <div class="content-label">Fokus</div>
                    <div class="content-text">${exercise.technique.focus}</div>
                </div>
                <div class="content-item">
                    <div class="content-label">Wichtige Punkte</div>
                    <div>
                        ${exercise.technique.keyPoints.map(p => `<div class="list-item">${p}</div>`).join('')}
                    </div>
                </div>
            </div>
        `;
    }
    
    // Common Mistakes
    if (exercise.commonMistakes && exercise.commonMistakes.length > 0) {
        html += `
            <div class="section-header">❌ Häufige Fehler</div>
            <div class="section-content">
                ${exercise.commonMistakes.map(mistake => `
                    <div class="mistake-block">
                        <div class="label">Fehler: ${mistake.mistake}</div>
                        <div class="text"><strong>Problem:</strong> ${mistake.consequence}</div>
                        <div class="text"><strong>Lösung:</strong> ${mistake.correction}</div>
                    </div>
                `).join('')}
            </div>
        `;
    }
    
    // Coaching Tips
    if (exercise.coachingTips) {
        html += `
            <div class="section-header">👨‍🏫 Coaching-Tipps</div>
            <div class="section-content">
                <div class="content-item">
                    <div class="content-label">Was beobachten?</div>
                    <div class="content-text">${exercise.coachingTips.observation}</div>
                </div>
                <div class="content-item">
                    <div class="content-label">Leichter machen</div>
                    <div class="content-text">${exercise.coachingTips.scaling_easier}</div>
                </div>
                <div class="content-item">
                    <div class="content-label">Schwerer machen</div>
                    <div class="content-text">${exercise.coachingTips.scaling_harder}</div>
                </div>
                <div class="content-item">
                    <div class="content-label">Motivation</div>
                    <div class="content-text">${exercise.coachingTips.motivation}</div>
                </div>
            </div>
        `;
    }
    
    // Progression
    if (exercise.progressionPath && exercise.progressionPath.length > 0) {
        html += `
            <div class="section-header">📈 Progression</div>
            <div class="section-content">
                ${exercise.progressionPath.map(p => `<div class="list-item">${p}</div>`).join('')}
            </div>
        `;
    }
    
    elements.exerciseContainer.innerHTML = html;
    currentView = 'exerciseDetail';
}

// ============================================
// Hilfsfunktionen
// ============================================

function getExercisesInCategory(categoryKey) {
    return Object.values(exercisesData.exercises).filter(
        exercise => exercise.category === categoryKey && exercise.published !== false
    ).sort((a, b) => a.name.localeCompare(b.name));  // Sort by name instead of order
}

function getCategoryIcon(categoryKey) {
    const icons = {
        warmup_coordination: '🏃',
        warmup_coerver: '🎪',
        firstTouch: '🎯',
        ballIntake: '🔄',
        ballControl: '👣',
        dribbling: '⚽',
        directionChange: '↩️',
        juggling: '🤹',
        partner: '👥'
    };
    return icons[categoryKey] || '⚽';
}

function showView(viewName) {
    elements.categoryView.classList.remove('active');
    elements.exerciseView.classList.remove('active');
    elements.videoView.classList.remove('active');
    workoutElements.workoutsView.classList.remove('active');
    workoutElements.workoutExecuteView.classList.remove('active');
    
    if (viewName === 'category' || viewName === 'categories') {
        elements.categoryView.classList.add('active');
    } else if (viewName === 'exercise') {
        elements.exerciseView.classList.add('active');
    } else if (viewName === 'video') {
        elements.videoView.classList.add('active');
    } else if (viewName === 'workouts') {
        workoutElements.workoutsView.classList.add('active');
    } else if (viewName === 'workout-execute') {
        workoutElements.workoutExecuteView.classList.add('active');
    }
}

function showVideoPlaceholder(title, duration) {
    elements.videoTitle.textContent = `${title} (${duration})`;
    showView('video');
    elements.backBtn.classList.remove('hidden');
}

// ============================================

function closeVideoModal() {
    document.getElementById('video-modal').classList.add('hidden');
    document.getElementById('modal-backdrop').classList.add('hidden');
    // Reset form
    document.getElementById('video-url').value = '';
    document.getElementById('video-title').value = '';
}

function saveVideoLink() {
    const url = document.getElementById('video-url').value.trim();
    const title = document.getElementById('video-title').value.trim();
    
    if (!url) {
        alert('Bitte gib einen YouTube-Link ein');
        return;
    }
    
    // Validate URL is YouTube
    if (!url.includes('youtube.com') && !url.includes('youtu.be')) {
        alert('Bitte gib einen gültigen YouTube-Link ein');
        return;
    }
    
    // Save to localStorage for current exercise
    if (currentExerciseId) {
        const videoData = {
            url: url,
            title: title || 'Training Video',
            saved: new Date().toISOString()
        };
        localStorage.setItem(`video_${currentExerciseId}`, JSON.stringify(videoData));
        alert('Video-Link lokal gespeichert! (Nur auf diesem Gerät)');
        closeVideoModal();
    }
}

function openVideoEditModal(exerciseId) {
    currentExerciseId = exerciseId;
    const exercise = exercisesData.exercises[exerciseId];
    
    if (exercise && exercise.videoLink && exercise.videoLink.url) {
        document.getElementById('video-url').value = exercise.videoLink.url;
        document.getElementById('video-title').value = exercise.videoLink.title || '';
    }
    
    openVideoModal();
}

// Setup Modal Event Listeners
function setupModalListeners() {
    document.getElementById('close-modal').addEventListener('click', closeVideoModal);
    document.getElementById('cancel-modal-btn').addEventListener('click', closeVideoModal);
    document.getElementById('modal-backdrop').addEventListener('click', closeVideoModal);
    document.getElementById('save-video-btn').addEventListener('click', saveVideoLink);
    
    // Save on Enter in title field
    document.getElementById('video-title').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') saveVideoLink();
    });
}


function goBack() {
    if (currentView === 'exerciseDetail') {
        renderExerciseList(currentCategory);
    } else if (currentView === 'exerciseList') {
        showView('category');
        renderCategories();
        elements.backBtn.classList.add('hidden');
    } else if (currentView === 'video') {
        renderExerciseDetail(Object.values(exercisesData.exercises).find(e => e.name === elements.videoTitle.textContent.split(' (')[0])?.id);
    }
}

function showLoading() {
    elements.loading.classList.remove('hidden');
}

function hideLoading() {
    elements.loading.classList.add('hidden');
}

function showError(message) {
    alert(`Fehler: ${message}`);
}

// ============================================
// WORKOUTS MANAGEMENT
// ============================================

let workoutsData = [];
let currentWorkout = null;
let currentSession = null;
let currentBlockIndex = 0;
let currentExerciseIndex = 0;
let completedExercises = [];

// Lazy-load workoutElements after DOM is ready
let workoutElements = {};

function initWorkoutElements() {
    workoutElements = {
        workoutsView: document.getElementById('workouts-view'),
        workoutExecuteView: document.getElementById('workout-execute-view'),
        workoutsContainer: document.querySelector('.workouts-container'),
        workoutExecuteContainer: document.querySelector('.workout-execute-container'),
        workoutsMenuBtn: document.getElementById('workouts-menu-btn')
    };
    
    // Add event listener for menu button
    if (workoutElements.workoutsMenuBtn) {
        workoutElements.workoutsMenuBtn.addEventListener('click', () => {
            showView('workouts');
            renderWorkouts();
            elements.sidebar.classList.remove('open');
        });
    }
}

async function loadWorkouts() {
    try {
        // Load workouts.json directly like exercises.json
        const response = await fetch('./data/workouts.json?v=1&t=' + Date.now());
        if (!response.ok) throw new Error('Fehler beim Laden von workouts.json');
        const data = await response.json();
        workoutsData = data.workouts || [];
        console.log('✅ Workouts loaded:', workoutsData.length);
    } catch (error) {
        console.error('❌ Error loading workouts:', error);
        workoutsData = [];
    }
}

function renderWorkouts() {
    workoutElements.workoutsContainer.innerHTML = '';
    
    if (workoutsData.length === 0) {
        workoutElements.workoutsContainer.innerHTML = '<div style="padding: 20px; text-align: center; color: #999;">Keine Trainingseinheiten verfügbar</div>';
        return;
    }
    
    // Group by unit and week
    const grouped = {};
    workoutsData.forEach(w => {
        const key = `${w.unit}-${w.week}`;
        if (!grouped[key]) grouped[key] = [];
        grouped[key].push(w);
    });
    
    // Display grouped
    Object.entries(grouped).sort().forEach(([key, items]) => {
        items.forEach(workout => {
            const exerciseCount = workout.blocks.reduce((sum, b) => sum + b.exercises.length, 0);
            
            const card = document.createElement('div');
            card.className = 'workout-card';
            card.style.cssText = `
                padding: 15px;
                background: #f8f9fa;
                border-radius: 8px;
                margin-bottom: 12px;
                border-left: 5px solid #667eea;
                cursor: pointer;
                transition: all 0.2s;
            `;
            
            card.innerHTML = `
                <div style="font-weight: 600; margin-bottom: 5px;">${workout.name}</div>
                <div style="font-size: 0.85em; color: #666; margin-bottom: 8px;">
                    ${workout.blocks.length} Blöcke | ${exerciseCount} Übungen | ${workout.totalDuration} Min
                </div>
                <div style="font-size: 0.8em; color: #999;">Level ${workout.difficulty}: ${workout.goal}</div>
            `;
            
            card.addEventListener('click', () => startWorkoutSession(workout));
            card.addEventListener('mouseover', () => card.style.background = '#f0f1ff');
            card.addEventListener('mouseout', () => card.style.background = '#f8f9fa');
            
            workoutElements.workoutsContainer.appendChild(card);
        });
    });
}

async function startWorkoutSession(workout) {
    currentWorkout = workout;
    currentBlockIndex = 0;
    currentExerciseIndex = 0;
    completedExercises = [];
    
    // Create session record
    const sessionId = `session-${Date.now()}`;
    currentSession = {
        id: sessionId,
        workout_id: workout.id,
        created_at: new Date().toISOString(),
        current_block_index: 0,
        current_exercise_index: 0,
        completed_exercises: []
    };
    
    // Try to save session (optional)
    try {
        await fetch('/api/sessions', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(currentSession)
        });
    } catch (e) {
        console.log('Session save failed (offline?), continuing...');
    }
    
    // Display workout execution view
    showView('workout-execute');
    displayWorkoutExecution();
}

function displayWorkoutExecution() {
    if (!currentWorkout || currentBlockIndex >= currentWorkout.blocks.length) {
        showWorkoutComplete();
        return;
    }
    
    const block = currentWorkout.blocks[currentBlockIndex];
    const exercise = block.exercises[currentExerciseIndex];
    
    if (!exercise) {
        currentBlockIndex++;
        currentExerciseIndex = 0;
        displayWorkoutExecution();
        return;
    }
    
    const totalExercises = currentWorkout.blocks.reduce((sum, b) => sum + b.exercises.length, 0);
    const completedCount = completedExercises.length;
    const progressPercent = Math.round((completedCount / totalExercises) * 100);
    
    workoutElements.workoutExecuteContainer.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <h2 style="margin: 0; font-size: 1.2em;">${currentWorkout.name}</h2>
            <button onclick="goBackFromWorkout()" style="padding: 8px 12px; background: #ddd; border: none; border-radius: 6px; cursor: pointer;">← Back</button>
        </div>
        
        <div style="background: #667eea; color: white; padding: 10px; border-radius: 6px; margin-bottom: 15px; font-size: 0.9em;">
            Block: <strong>${currentBlockIndex + 1}/${currentWorkout.blocks.length}</strong> | Progress: <strong>${completedCount}/${totalExercises} (${progressPercent}%)</strong>
        </div>
        
        <div style="width: 100%; height: 8px; background: #eee; border-radius: 4px; margin-bottom: 20px;">
            <div style="width: ${progressPercent}%; height: 100%; background: #667eea;"></div>
        </div>
        
        <div style="background: #f0f1ff; padding: 12px; border-radius: 6px; margin-bottom: 15px;">
            <div style="font-size: 0.85em; color: #666;">Block: ${block.name}</div>
        </div>
        
        <div style="background: white; border: 2px solid #667eea; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <div style="font-size: 1.1em; font-weight: 600; margin-bottom: 10px;">${exercise.sets}x${exercise.reps}</div>
            <div style="font-size: 0.9em; color: #555;">${exercise.notes || 'No notes'}</div>
        </div>
        
        <button onclick="markExerciseComplete()" style="width: 100%; padding: 12px; background: #27ae60; color: white; border: none; border-radius: 6px; font-weight: 600; cursor: pointer;">
            ✓ Done - Next Exercise
        </button>
    `;
}

function markExerciseComplete() {
    const block = currentWorkout.blocks[currentBlockIndex];
    const exercise = block.exercises[currentExerciseIndex];
    
    completedExercises.push({
        block: currentBlockIndex,
        exercise: currentExerciseIndex,
        exerciseId: exercise.exerciseId,
        timestamp: Date.now()
    });
    
    currentExerciseIndex++;
    displayWorkoutExecution();
    
    if (currentSession) {
        fetch(`/api/sessions/${currentSession.id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                current_block_index: currentBlockIndex,
                current_exercise_index: currentExerciseIndex,
                completed_exercises: completedExercises
            })
        }).catch(e => console.log('Session save failed'));
    }
}

function showWorkoutComplete() {
    const totalExercises = currentWorkout.blocks.reduce((sum, b) => sum + b.exercises.length, 0);
    
    workoutElements.workoutExecuteContainer.innerHTML = `
        <div style="text-align: center; padding: 40px 20px;">
            <div style="font-size: 4em; margin-bottom: 20px;">🎉</div>
            <h2 style="font-size: 1.5em; margin-bottom: 10px;">Congratulations!</h2>
            <p style="color: #666; font-size: 1.1em; margin-bottom: 20px;">All exercises completed!</p>
            <div style="background: #f0f1ff; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                <div>✅ ${totalExercises}/${totalExercises} Exercises</div>
                <div>⏱️ ${currentWorkout.totalDuration} Min</div>
            </div>
            <button onclick="goBackFromWorkout()" style="width: 100%; padding: 12px; background: #667eea; color: white; border: none; border-radius: 6px; cursor: pointer;">
                ← Back to Workouts
            </button>
        </div>
    `;
}

function goBackFromWorkout() {
    currentWorkout = null;
    currentSession = null;
    showView('workouts');
    renderWorkouts();
    elements.sidebar.classList.remove('open');
}

// ============================================
// Service Worker Update Check
// ============================================

function setupUpdateCheck() {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.ready.then((registration) => {
            console.log('Service Worker ready for update checks');
            
            // Checke alle 5 Sekunden auf Update (für schnelleres Testen)
            // In Produktion: setInterval(checkForUpdates, 5 * 60 * 1000); // 5 Minuten
            setInterval(checkForUpdates, 5000);
            
            // Sofort einmal checken
            checkForUpdates();
            
            // Höre auf controllerchange
            navigator.serviceWorker.addEventListener('controllerchange', () => {
                console.log('New Service Worker activated');
                showUpdateBanner();
            });
        });
    }
}

function checkForUpdates() {
    if (!navigator.serviceWorker.controller) return;
    
    fetch('./sw.js?v=' + Date.now(), { cache: 'no-store' })
        .then(response => {
            if (response.ok) {
                navigator.serviceWorker.controller.postMessage({ type: 'CHECK_UPDATE' });
            }
        })
        .catch(err => console.log('Update check failed:', err));
}

function showUpdateBanner() {
    const banner = document.getElementById('update-banner');
    const btn = document.getElementById('update-btn');
    
    banner.classList.remove('hidden');
    
    btn.addEventListener('click', () => {
        // Reload with new service worker
        window.location.reload();
    });
}

// ============================================
// Start
// ============================================

document.addEventListener('DOMContentLoaded', async () => {
    await init();
    await loadWorkouts();
    setupUpdateCheck();
});
