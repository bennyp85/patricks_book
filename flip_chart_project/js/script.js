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

let isSelectionInProgress = false;

// Function to handle color selection
function handleColorSelect(color) {
    selectedColor = color;
    isSelectionInProgress = true; // Set flag when a color is selected
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
    resetNumberSelection();
    isSelectionInProgress = false; // Reset flag after selection is complete
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
    console.log('isSelectionInProgress:', isSelectionInProgress);
    console.log('history.length:', history.length);

    if (isSelectionInProgress) {
        console.log('Selection in progress. Resetting selection.');
        resetColorSelection();
        showColors(true);
        showNumbers(false);
        showChosenColorDisplay(false);
        isSelectionInProgress = false;
    } else if (history.length > 0) {
        console.log('No selection in progress. Removing last history item.');
        removeLastHistoryItem();
    } else {
        console.log('No action to perform.');
    }
});

// Clear Button Handler
clearButton.addEventListener('click', () => {
    clearHistory();
});
