document.addEventListener('DOMContentLoaded', () => {
    const numbers = document.querySelectorAll('.number');
    const historyBar = document.getElementById('historyBar');
    const greenBtn = document.getElementById('greenBtn');
    const deleteBtn = document.getElementById('deleteBtn');
    const clearBtn = document.getElementById('clearBtn');
    let history = [];
    let isGreen = false;

    // Initialize button to show opposite of current number color
    greenBtn.textContent = 'Green'; // Start with Green text
    greenBtn.style.backgroundColor = '#4CAF50'; // Start with green color
    
    greenBtn.addEventListener('click', () => {
        isGreen = !isGreen;
        document.body.classList.toggle('green-numbers', isGreen);
        // Update button to show the color we can change TO
        greenBtn.textContent = isGreen ? 'Blue' : 'Green';
        greenBtn.style.backgroundColor = isGreen ? '#2196F3' : '#4CAF50';
    });

    numbers.forEach(button => {
        button.addEventListener('click', () => {
            const value = button.getAttribute('data-value');
            history.push(value);
            updateHistory();
        });
    });

    deleteBtn.addEventListener('click', () => {
        history.pop();
        updateHistory();
    });

    clearBtn.addEventListener('click', () => {
        history = [];
        updateHistory();
    });

    function updateHistory() {
        historyBar.textContent = history.join(' ');
    }

    numbers.forEach(button => {
        button.addEventListener('focus', () => {
            button.style.outline = '2px solid yellow';
        });
        button.addEventListener('blur', () => {
            button.style.outline = '2px solid transparent';
        });
    });
});