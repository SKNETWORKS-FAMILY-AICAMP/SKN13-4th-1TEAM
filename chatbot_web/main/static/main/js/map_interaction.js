document.addEventListener("DOMContentLoaded", () => {
  const paths = document.querySelectorAll(".land");

  paths.forEach(path => {
    // --- CLICK EVENT ---
    path.addEventListener("click", () => {
      const isCurrentlyFocused = path.classList.contains("focused");
      const previouslyFocused = document.querySelector(".land.focused");

      if (previouslyFocused) {
        previouslyFocused.classList.remove("focused");
      }

      if (!isCurrentlyFocused) {
        path.classList.add("focused");
        // Delay DOM change to allow transition to start
        setTimeout(() => {
          // Ensure the element is still in the DOM and has a parent
          if (path.parentNode) {
            path.parentNode.appendChild(path);
          }
        }, 300); // 50ms delay
      }
    });

    // --- MOUSEOVER EVENT ---
    path.addEventListener('mouseover', () => {
      if (path.classList.contains('focused')) {
        return;
      }

      // Delay DOM change to allow transition to start
      setTimeout(() => {
        // Ensure the element is still in the DOM and has a parent
        if (path.parentNode) {
          const focusedElement = document.querySelector('.land.focused');
          if (focusedElement) {
            path.parentNode.insertBefore(path, focusedElement);
          } else {
            path.parentNode.appendChild(path);
          }
        }
      }, 50); // 50ms delay
    });
  });
});
