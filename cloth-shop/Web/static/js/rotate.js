const expandElement = document.querySelector('.expand');
const inputElements = document.querySelector('.hidden');

let hidden = true;

expandElement.addEventListener('click', () => {
    console.log('muffi')
    expandElement.classList.toggle('rotate');
    if (hidden) {
        inputElements.style.maxHeight = inputElements.scrollHeight + 'px'; 
        inputElements.style.opacity = '1'; 
        hidden = false;
    } 
    else {
        inputElements.style.maxHeight = '0px'; 
        inputElements.style.opacity = '0'; 
        hidden = true;
    }
});
