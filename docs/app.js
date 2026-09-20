let exercisesData = null;
let currentView = 'categories';
let currentCategory = null;

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
        
        // Lade exercises.json
        const response = await fetch('./data/exercises.json');
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

// ============================================
// Views: Kategorie-Ansicht
// ============================================

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
    
    // Header
    const header = document.createElement('h2');
    header.className = 'section-header';
    header.innerHTML = `${getCategoryIcon(categoryKey)} ${category.name}`;
    elements.categoriesContainer.appendChild(header);
    
    // Übungen als Liste
    const exercisesList = document.createElement('div');
    exercisesList.style.padding = '0 1rem';
    
    exercises.forEach(exercise => {
        const item = document.createElement('div');
        item.className = 'category-card';
        item.style.marginBottom = '1rem';
        item.innerHTML = `
            <div style="text-align: left;">
                <div class="category-name" style="font-size: 1.1rem; margin-bottom: 0.5rem;">
                    ${exercise.name}
                </div>
                <div style="color: var(--color-text-secondary); font-size: 0.85rem;">
                    ⏱️ ${exercise.duration} | ${exercise.solo ? '👤 Solo' : '👥 2+ Personen'}
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
    
    showView('exercise');
    
    let html = `
        <div class="exercise-header">
            <h1 class="exercise-title">${exercise.name}</h1>
            <div class="exercise-meta">
                <div class="meta-item">⏱️ ${exercise.duration}</div>
                <div class="meta-item">${exercise.solo ? '👤 Solo' : '👥 2+ Personen'}</div>
                ${exercise.setup?.equipment ? `<div class="meta-item">🎒 ${exercise.setup.equipment.length} Items</div>` : ''}
            </div>
        </div>
        
        <div class="section-content">
            <p style="color: var(--color-text-secondary); margin-bottom: 1rem;">${exercise.description}</p>
        </div>
    `;
    
    // Video Placeholder
    if (exercise.videoPlaceholder) {
        html += `
            <div style="padding: 0 1.5rem;">
                <div class="video-placeholder" onclick="showVideoPlaceholder('${exercise.name}', '${exercise.videoPlaceholder.duration}')">
                    <div class="video-icon">🎬</div>
                    <p>Video anschauen</p>
                    <small>~${exercise.videoPlaceholder.duration}</small>
                </div>
            </div>
        `;
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
        exercise => exercise.category === categoryKey
    ).sort((a, b) => a.order - b.order);
}

function getCategoryIcon(categoryKey) {
    const icons = {
        warmup: '🔥',
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
    
    if (viewName === 'category') {
        elements.categoryView.classList.add('active');
    } else if (viewName === 'exercise') {
        elements.exerciseView.classList.add('active');
    } else if (viewName === 'video') {
        elements.videoView.classList.add('active');
    }
}

function showVideoPlaceholder(title, duration) {
    elements.videoTitle.textContent = `${title} (${duration})`;
    showView('video');
    elements.backBtn.classList.remove('hidden');
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
// Start
// ============================================

document.addEventListener('DOMContentLoaded', init);
