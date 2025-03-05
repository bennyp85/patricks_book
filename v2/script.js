document.addEventListener('DOMContentLoaded', () => {
    const numbers = document.querySelectorAll('.number');
    const dvdHistoryBar = document.getElementById('dvdHistoryBar');
    const sceneHistoryBar = document.getElementById('sceneHistoryBar');
    const greenBtn = document.getElementById('greenBtn');
    const sceneBtn = document.getElementById('sceneBtn');
    const dvdClearBtn = document.getElementById('dvdClearBtn');
    const dvdDeleteBtn = document.getElementById('dvdDeleteBtn');
    const sceneClearBtn = document.getElementById('sceneClearBtn');
    const sceneDeleteBtn = document.getElementById('sceneDeleteBtn');
    const dvdLabel = document.getElementById('dvdLabel');
    const sceneLabel = document.getElementById('sceneLabel');
    
    let dvdHistory = [];
    let sceneHistory = [];
    let isGreen = false;
    let isSceneMode = false; // Track if we're in scene input mode

    // Initialize button to show opposite of current number color
    greenBtn.textContent = 'Green'; // Start with Green text
    greenBtn.style.backgroundColor = '#4CAF50'; // Start with green color
    
    // Initialize Scene button
    sceneBtn.textContent = 'Scene'; // Start with Scene text
    sceneBtn.style.backgroundColor = '#2196F3'; // Start with blue color
    
    // Initialize with DVD label highlighted
    dvdLabel.classList.add('active-label');
    
    greenBtn.addEventListener('click', () => {
        isGreen = !isGreen;
        document.body.classList.toggle('green-numbers', isGreen);
        // Update button to show the color we can change TO
        greenBtn.textContent = isGreen ? 'White' : 'Green';
        greenBtn.style.backgroundColor = isGreen ? '#FFFFFF' : '#4CAF50';
    });

    sceneBtn.addEventListener('click', () => {
        isSceneMode = !isSceneMode;
        // Update both text and color
        if (isSceneMode) {
            sceneBtn.textContent = 'DVD';
            sceneBtn.style.backgroundColor = '#FF9800'; // Orange for Scene mode
            sceneLabel.classList.add('active-label');
            dvdLabel.classList.remove('active-label');
        } else {
            sceneBtn.textContent = 'Scene';
            sceneBtn.style.backgroundColor = '#2196F3'; // Blue for DVD mode
            dvdLabel.classList.add('active-label');
            sceneLabel.classList.remove('active-label');
        }
    });

    numbers.forEach(button => {
        button.addEventListener('click', () => {
            const value = button.getAttribute('data-value');
            if (isSceneMode) {
                sceneHistory.push(value);
                updateSceneHistory();
            } else {
                dvdHistory.push(value);
                updateDVDHistory();
            }
        });
    });

    // DVD buttons
    dvdDeleteBtn.addEventListener('click', () => {
        dvdHistory.pop();
        updateDVDHistory();
    });

    dvdClearBtn.addEventListener('click', () => {
        dvdHistory = [];
        updateDVDHistory();
    });

    // Scene buttons
    sceneDeleteBtn.addEventListener('click', () => {
        sceneHistory.pop();
        updateSceneHistory();
    });

    sceneClearBtn.addEventListener('click', () => {
        sceneHistory = [];
        updateSceneHistory();
    });

    function updateDVDHistory() {
        dvdHistoryBar.textContent = dvdHistory.join(' ');
    }

    function updateSceneHistory() {
        sceneHistoryBar.textContent = sceneHistory.join(' ');
    }
});