document.addEventListener('DOMContentLoaded', () => {
    const titleUpload = document.getElementById('titleUpload');
    
    // Get references to all UI elements
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
    const findBtn = document.getElementById('findBtn');

    let dvdHistory = [];
    let sceneHistory = [];
    let isGreen = false;
    let isSceneMode = false;
    
    // Make title clickable only if no CSV data is loaded
    if (titleUpload) {
        // Add visual indicator if CSV is loaded or not
        if (!localStorage.getItem('csvData')) {
            titleUpload.classList.add('needs-upload');
            titleUpload.title = "Click to upload CSV data";
            
            // Add event listener only if no CSV data
            titleUpload.addEventListener('click', () => {
                showFileUploadModal();
            });
        } else {
            // CSV is already loaded - make title show this
            titleUpload.classList.add('data-loaded');
            titleUpload.title = "CSV data loaded";
            
            // Add different click behavior - show info about loaded data
            titleUpload.addEventListener('click', () => {
                showCSVInfoModal();
            });
        }
    }
    
    // Function to create and show file upload modal
    function showFileUploadModal() {
        // Create modal container
        const modalOverlay = document.createElement('div');
        modalOverlay.className = 'file-upload-overlay';
        modalOverlay.style.position = 'fixed';
        modalOverlay.style.top = '0';
        modalOverlay.style.left = '0';
        modalOverlay.style.width = '100%';
        modalOverlay.style.height = '100%';
        modalOverlay.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
        modalOverlay.style.zIndex = '1000';
        modalOverlay.style.display = 'flex';
        modalOverlay.style.justifyContent = 'center';
        modalOverlay.style.alignItems = 'center';
        
        // Create modal content
        const modalContent = document.createElement('div');
        modalContent.className = 'file-upload-modal';
        modalContent.style.backgroundColor = '#fff';
        modalContent.style.padding = '20px';
        modalContent.style.borderRadius = '8px';
        modalContent.style.width = '80%';
        modalContent.style.maxWidth = '500px';
        modalContent.style.textAlign = 'center';
        
        // Add heading
        const heading = document.createElement('h2');
        heading.textContent = 'Upload CSV File';
        heading.style.marginBottom = '20px';
        
        // Add file input
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.id = 'csvFileInput';
        fileInput.accept = '.csv';
        fileInput.style.display = 'block';
        fileInput.style.margin = '20px auto';
        
        // Add upload button
        const uploadButton = document.createElement('button');
        uploadButton.textContent = 'Upload';
        uploadButton.style.padding = '10px 20px';
        uploadButton.style.backgroundColor = '#4CAF50';
        uploadButton.style.color = 'white';
        uploadButton.style.border = 'none';
        uploadButton.style.borderRadius = '4px';
        uploadButton.style.cursor = 'pointer';
        uploadButton.style.fontSize = '16px';
        
        // Status message
        const statusMessage = document.createElement('p');
        statusMessage.id = 'uploadStatus';
        statusMessage.style.marginTop = '15px';
        
        // Add event listener for file upload
        uploadButton.addEventListener('click', () => {
            const file = fileInput.files[0];
            if (!file) {
                statusMessage.textContent = 'Please select a CSV file first.';
                statusMessage.style.color = 'red';
                return;
            }
            
            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    const csvContent = e.target.result;
                    localStorage.setItem('csvData', csvContent);
                    statusMessage.textContent = 'File uploaded successfully!';
                    statusMessage.style.color = 'green';
                    
                    // Close modal after a short delay
                    setTimeout(() => {
                        document.body.removeChild(modalOverlay);
                    }, 1500);
                } catch (error) {
                    statusMessage.textContent = 'Error uploading file: ' + error.message;
                    statusMessage.style.color = 'red';
                }
            };
            
            reader.onerror = () => {
                statusMessage.textContent = 'Error reading file.';
                statusMessage.style.color = 'red';
            };
            
            reader.readAsText(file);
        });
        
        // Assemble modal
        modalContent.appendChild(heading);
        modalContent.appendChild(fileInput);
        modalContent.appendChild(uploadButton);
        modalContent.appendChild(statusMessage);
        modalOverlay.appendChild(modalContent);
        
        // Add modal to the document
        document.body.appendChild(modalOverlay);
    }
    
    // Function to show info about loaded CSV
    function showCSVInfoModal() {
        const csvData = localStorage.getItem('csvData');
        if (!csvData) return;
        
        // Count number of entries in CSV
        const lines = csvData.split(/\r?\n/).filter(line => line.trim().length > 0);
        const entryCount = lines.length;
        
        // Create modal container
        const modalOverlay = document.createElement('div');
        modalOverlay.className = 'file-upload-overlay';
        modalOverlay.style.position = 'fixed';
        modalOverlay.style.top = '0';
        modalOverlay.style.left = '0';
        modalOverlay.style.width = '100%';
        modalOverlay.style.height = '100%';
        modalOverlay.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
        modalOverlay.style.zIndex = '1000';
        modalOverlay.style.display = 'flex';
        modalOverlay.style.justifyContent = 'center';
        modalOverlay.style.alignItems = 'center';
        
        // Create modal content
        const modalContent = document.createElement('div');
        modalContent.className = 'file-info-modal';
        modalContent.style.backgroundColor = '#fff';
        modalContent.style.padding = '20px';
        modalContent.style.borderRadius = '8px';
        modalContent.style.width = '80%';
        modalContent.style.maxWidth = '500px';
        modalContent.style.textAlign = 'center';
        modalContent.style.color = '#333';
        
        // Add heading
        const heading = document.createElement('h2');
        heading.textContent = 'CSV Data Loaded';
        heading.style.marginBottom = '20px';
        
        // Add info text
        const infoText = document.createElement('p');
        infoText.textContent = `${entryCount} entries loaded`;
        infoText.style.marginBottom = '20px';
        infoText.style.fontSize = '18px';
        
        // Add buttons
        const buttonContainer = document.createElement('div');
        buttonContainer.style.display = 'flex';
        buttonContainer.style.justifyContent = 'space-around';
        
        // Close button
        const closeButton = document.createElement('button');
        closeButton.textContent = 'Close';
        closeButton.style.padding = '10px 20px';
        closeButton.style.backgroundColor = '#4CAF50';
        closeButton.style.color = 'white';
        closeButton.style.border = 'none';
        closeButton.style.borderRadius = '4px';
        closeButton.style.cursor = 'pointer';
        closeButton.style.fontSize = '16px';
        
        // Replace button
        const replaceButton = document.createElement('button');
        replaceButton.textContent = 'Replace CSV';
        replaceButton.style.padding = '10px 20px';
        replaceButton.style.backgroundColor = '#f39c12';
        replaceButton.style.color = 'white';
        replaceButton.style.border = 'none';
        replaceButton.style.borderRadius = '4px';
        replaceButton.style.cursor = 'pointer';
        replaceButton.style.fontSize = '16px';
        
        // Event listeners
        closeButton.addEventListener('click', () => {
            document.body.removeChild(modalOverlay);
        });
        
        replaceButton.addEventListener('click', () => {
            document.body.removeChild(modalOverlay);
            showFileUploadModal();
        });
        
        // Assemble modal
        buttonContainer.appendChild(closeButton);
        buttonContainer.appendChild(replaceButton);
        modalContent.appendChild(heading);
        modalContent.appendChild(infoText);
        modalContent.appendChild(buttonContainer);
        modalOverlay.appendChild(modalContent);
        
        // Add modal to the document
        document.body.appendChild(modalOverlay);
    }
    
    // Redirect to location.html with current DVD and Scene values
    findBtn.addEventListener('click', () => {
        const dvd = dvdHistory.join('');
        const scene = sceneHistory.join('');
        const color = isGreen ? 'green' : 'white';
        const params = new URLSearchParams({ dvd, color, scene });
        window.location.href = `location.html?${params.toString()}`;
    });

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