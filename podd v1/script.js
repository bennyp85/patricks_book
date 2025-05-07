document.addEventListener('DOMContentLoaded', () => {
    const icons = document.querySelectorAll('.icon');
    const clickedList = document.getElementById('clicked-list');
    const deleteButton = document.getElementById('delete-button');
    const clearButton = document.getElementById('clear-button');

    icons.forEach(icon => {
        icon.addEventListener('click', () => {
            const page = icon.dataset.page;
            
            if (page) {
                // Redirect to [number].html
                console.log(`Redirecting to: ${page}`);
                // To enable actual redirection, uncomment the line below:
                // window.location.href = page;
                
                // Get icon text for display in clicked area
                const textElement = icon.querySelector('.icon-main-text');
                let iconText = icon.dataset.text || '';
                
                if (textElement) {
                    iconText = textElement.innerHTML.replace(/<br\s*\/?>/gi, " ").trim();
                }
                
                // Add to clicked list as text
                const listItem = document.createElement('li');
                listItem.textContent = `Navigated to page for: ${iconText} (link: ${page})`;
                clickedList.appendChild(listItem);
                
            } else {
                // For icons without page redirection, show the image
                const iconImg = icon.querySelector('img');
                
                if (iconImg) {
                    // Create a list item
                    const listItem = document.createElement('li');
                    
                    // Create a new image element that's a copy of the icon image
                    const imgCopy = document.createElement('img');
                    imgCopy.src = iconImg.src;
                    imgCopy.alt = iconImg.alt;
                    imgCopy.classList.add('clicked-icon-image');
                    
                    // Add the image to the list item
                    listItem.appendChild(imgCopy);
                    
                    // Add to the clicked list
                    clickedList.appendChild(listItem);
                }
            }
        });
    });
    
    // Delete button - removes the last item
    deleteButton.addEventListener('click', () => {
        const items = clickedList.querySelectorAll('li');
        if (items.length > 0) {
            // Remove the last item
            clickedList.removeChild(items[items.length - 1]);
        }
    });
    
    // Clear button - removes all items
    clearButton.addEventListener('click', () => {
        // Remove all items
        clickedList.innerHTML = '';
    });
});