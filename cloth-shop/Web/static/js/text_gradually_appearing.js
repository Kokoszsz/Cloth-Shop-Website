window.addEventListener('load', () => {
  setTimeout(() => {
    const fadeElements = document.querySelectorAll('#fade-container > *');
    let delay = 0;
    fadeElements.forEach((element) => {
      setTimeout(() => {
        element.style.opacity = '1';
      }, delay);
      delay += 800;
    });
  }, 1000); 
});
