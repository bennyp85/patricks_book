// js/script.js

import { colorMap, showColors, showChosenColorDisplay, initializeColorHandlers, resetColorSelection } from './colorHandler.js';
import { showNumbers, initializeNumberHandlers, resetNumberSelection, getSelectedNumber } from './numberHandler.js';
import { addToHistory, removeLastHistoryItem, clearHistory } from './historyHandler.js';

// DOM Elements
const deleteButton = document.getElementById('delete-button');
const clearButton = document.getElementById('clear-button');
const chosenColorDisplay = document.getElementById('chosen-color-display');

// Initialize application state
let selectedColor = null;

// Function to handle color selection
function handleColorSelect(color) {
    selectedColor = color;
    showNumbers(true);
}

// Function to handle number selection
function handleNumberSelect(number) {
    if (!selectedColor) {
        alert("Please select a color first.");
        return;
    }
    addToHistory(selectedColor, number, colorMap);
    showNumbers(false);
    showColors(true);
    showChosenColorDisplay(false);
}

// Initialize color handlers
initializeColorHandlers(handleColorSelect);

// Initialize number handlers
initializeNumberHandlers(handleNumberSelect);

// Initial UI State
showColors(true);
showNumbers(false);
showChosenColorDisplay(false);

// Delete Button Handler
deleteButton.addEventListener('click', () => {
    console.log('selectedColor:', selectedColor);
    console.log('getSelectedNumber():', getSelectedNumber());

    if (selectedColor && !getSelectedNumber()) {
        console.log('Condition met: selectedColor is true and getSelectedNumber() is false.');
        resetColorSelection();
        showNumbers(false);
        showColors(true);
        showChosenColorDisplay(false);
    } else {
        console.log('Condition not met: removing last history item.');
        removeLastHistoryItem();
    }
});

// Clear Button Handler
clearButton.addEventListener('click', () => {
    clearHistory();
});
