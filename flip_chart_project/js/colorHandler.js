// js/colorHandler.js

export const colorMap = {
    "Red": "#FF0000",
    "Blue": "#0000FF",
    "Green": "#2eb72e",
    "Yellow": "#FFFF00",
    "Purple": "#800080",
    "Brown": "#8B4513",
    "Light Blue": "#ADD8E6",
    "Orange": "#FFA500",
    "Grey": "#808080",
    "Black": "#000000",
    "Dark Blue": "#00008B"
};

let selectedColor = null;

const colorSquares = document.querySelectorAll('.square');
const chosenColorDisplay = document.getElementById('chosen-color-display');
const chosenColorSquare = document.getElementById('chosen-color-square');

export function resetColorSelection() {
    selectedColor = null;
}

export function getSelectedColor() {
    return selectedColor;
}

export function showColors(show) {
    colorSquares.forEach(cs => {
        cs.style.display = show ? 'block' : 'none';
    });
}

export function showChosenColorDisplay(show, color = null) {
    if (show && color) {
        chosenColorSquare.style.backgroundColor = colorMap[color];
        chosenColorDisplay.style.display = 'block';
    } else {
        chosenColorDisplay.style.display = 'none';
    }
}

export function initializeColorHandlers(onColorSelect) {
    colorSquares.forEach(square => {
        square.addEventListener('click', () => {
            resetColorSelection();
            selectedColor = square.getAttribute('data-color');
            showColors(false);
            onColorSelect(selectedColor);
            showChosenColorDisplay(true, selectedColor);
        });
    });
}
