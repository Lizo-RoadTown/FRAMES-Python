// FRAMES Student Onboarding - Module Viewer

let currentModule = null;
let sections = [];
let currentSectionIndex = 0;
let startTime = Date.now();

async function loadModule() {
    try {
        const response = await fetch(`/api/modules/${MODULE_ID}`);
        const data = await response.json();

        currentModule = data.module;
        sections = data.sections;

        displayModuleHeader();
        displaySection(0);
        updateNavigation();

    } catch (error) {
        console.error('Error loading module:', error);
        document.getElementById('module-content').innerHTML = `
            <div style="text-align: center; padding: 3rem; color: #ef4444;">
                <h2>Error loading module</h2>
                <p>${error.message}</p>
            </div>
        `;
    }
}

function displayModuleHeader() {
    document.getElementById('module-title').textContent = currentModule.title;
    document.getElementById('module-meta').innerHTML = `
        <span>${currentModule.category || 'General'}</span> •
        <span>${sections.length} sections</span> •
        <span>⏱️ ${currentModule.estimated_minutes} minutes</span>
    `;
    document.title = `${currentModule.title} - FRAMES`;
}

function displaySection(index) {
    if (index < 0 || index >= sections.length) return;

    currentSectionIndex = index;
    const section = sections[index];

    document.getElementById('module-content').innerHTML = `
        <div class="section">
            ${section.title ? `<h2>${section.title}</h2>` : ''}
            <div class="section-content">${formatContent(section.content, section.section_type)}</div>
        </div>
    `;

    updateProgress();
    updateNavigation();
    window.scrollTo(0, 0);

    // Track section view
    trackProgress('section_view', index);
}

function formatContent(content, type) {
    // Simple content formatting
    if (type === 'text') {
        return content.replace(/\n\n/g, '</p><p>').replace(/\n/g, '<br>');
    }

    // Handle other types (video, image, etc.) later
    return content;
}

function updateProgress() {
    const progress = ((currentSectionIndex + 1) / sections.length) * 100;
    document.getElementById('progress-fill').style.width = `${progress}%`;
}

function updateNavigation() {
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const indicator = document.getElementById('section-indicator');

    prevBtn.disabled = currentSectionIndex === 0;
    nextBtn.disabled = currentSectionIndex === sections.length - 1;

    indicator.textContent = `Section ${currentSectionIndex + 1} of ${sections.length}`;

    if (currentSectionIndex === sections.length - 1) {
        nextBtn.textContent = '✓ Complete';
        nextBtn.style.background = '#10b981';
    } else {
        nextBtn.textContent = 'Next →';
        nextBtn.style.background = '';
    }
}

function nextSection() {
    if (currentSectionIndex < sections.length - 1) {
        displaySection(currentSectionIndex + 1);
    } else {
        // Module completed
        trackProgress('complete');
        alert('Module completed! Great job! 🎉');
        window.location.href = '/';
    }
}

function prevSection() {
    if (currentSectionIndex > 0) {
        displaySection(currentSectionIndex - 1);
    }
}

async function trackProgress(eventType, sectionNumber = null) {
    try {
        await fetch(`/api/modules/${MODULE_ID}/progress`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                event_type: eventType,
                section_number: sectionNumber,
                timestamp: new Date().toISOString(),
                time_elapsed: Math.floor((Date.now() - startTime) / 1000)
            })
        });
    } catch (error) {
        console.error('Error tracking progress:', error);
    }
}

// Event listeners
document.getElementById('next-btn').addEventListener('click', nextSection);
document.getElementById('prev-btn').addEventListener('click', prevSection);

// Keyboard navigation
document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') nextSection();
    if (e.key === 'ArrowLeft') prevSection();
});

// Track when user leaves
window.addEventListener('beforeunload', () => {
    trackProgress('pause', currentSectionIndex);
});

// Load module when page loads
document.addEventListener('DOMContentLoaded', loadModule);
