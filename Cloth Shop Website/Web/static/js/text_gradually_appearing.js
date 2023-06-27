window.addEventListener('load', () => {
  setTimeout(() => {
    const fadeElements = document.querySelectorAll('#fade-container > *');
    let delay = 0;
    fadeElements.forEach((element) => {
      setTimeout(() => {
        element.style.opacity = '1';
      }, delay);
      delay += 800; // Adjust the delay between each element appearing
    });
  }, 1000); // Wait for 5 seconds before executing the code
});
