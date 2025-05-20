# PODD Communication Interface Prototype

This project is a simple, frontend-only prototype inspired by a PODD (Pragmatic Organization Dynamic Display) communication system. It simulates a basic communication interface where users can select categories, choose icons, and form messages represented as a sequence of words.

## Features

- **Category-Based Navigation:**  
  A sidebar allows switching between predefined categories (e.g., Core Words, People, Foods, Actions, Places). Each category displays its relevant icons in a grid layout.

- **Grid-Based Icon Layout:**  
  Each category shows a responsive grid of selectable icons. Clicking an icon highlights it, indicating selection, and adds its label to a message textbox.

- **Persisting Selections:**  
  Selected items remain in the message textbox even as you switch categories, allowing the user to build longer, more complex "sentences."

- **Clear Button:**  
  A "Clear" button is provided to reset all selections at once, clearing the message textbox and resetting the displayed selection states.

- **No Backend Required:**  
  This is a static application built with HTML, CSS, and JavaScript. No server or backend code is required. Simply open the `index.html` file in a web browser to run the prototype.

- **Eye-Tracking Friendly Design (Future Integration):**  
  The icons and categories are presented with large clickable areas to support potential integration with eye-tracking hardware in the future.
