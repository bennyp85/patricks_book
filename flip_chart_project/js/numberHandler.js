// js/numberHandler.js

let selectedNumber = null;

const numbers = document.querySelectorAll('.number');

export function resetNumberSelection() {
    selectedNumber = null;
}

export function getSelectedNumber() {
    return selectedNumber;
}

export function showNumbers(show) {
    numbers.forEach(num => {
        num.style.display = show ? 'block' : 'none';
    });
}

export function initializeNumberHandlers(onNumberSelect) {
    numbers.forEach(num => {
        num.addEventListener('click', () => {
            selectedNumber = num.getAttribute('data-number');
            onNumberSelect(selectedNumber);
        });
    });
}
