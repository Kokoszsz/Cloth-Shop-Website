window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
    document.querySelector('.panel').classList.add('show');
  } else {
    document.querySelector('.panel').classList.remove('show');
  }
}




