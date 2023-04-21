window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 500 || document.documentElement.scrollTop > 500) {
    document.querySelector('.panel').classList.add('show');
  } else {
    document.querySelector('.panel').classList.remove('show');
  }
}




