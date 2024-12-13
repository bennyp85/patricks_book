// js/historyHandler.js

let historyItems = [];
const historyItemsContainer = document.getElementById('history-items');

export function addToHistory(color, number, colorMap) {
    const itemDiv = document.createElement('div');
    itemDiv.className = 'history-item';
    itemDiv.innerHTML = `
        <div class="color-square" style="background-color: ${colorMap[color]}"></div>
        <span>${color} ${number}</span>
    `;
    historyItemsContainer.appendChild(itemDiv);
    historyItems.push({ color, number });
}

export function removeLastHistoryItem() {
    if (historyItems.length === 0) {
        console.log('No history items to remove.');
        return;
    }
    const allItems = historyItemsContainer.querySelectorAll('.history-item');
    if (allItems.length > 0) {
        const lastItem = allItems[allItems.length - 1];
        console.log('Removing item:', lastItem.innerHTML);
        historyItemsContainer.removeChild(lastItem);
        historyItems.pop();
    } else {
        console.log('No history items found in the container.');
    }
}

export function clearHistory() {
    historyItems = [];
    historyItemsContainer.innerHTML = '';
}