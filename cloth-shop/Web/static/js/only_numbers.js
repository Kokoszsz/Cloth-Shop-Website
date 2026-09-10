var minInput = document.getElementsByName('minvalue')[0];
var maxInput = document.getElementsByName('maxvalue')[0];
      
        // Allow numbers only
        minInput.addEventListener('input', function(evt) {
          if (isNaN(parseFloat(evt.target.value))) {
            evt.target.value = '0';
          }
        });
      
        maxInput.addEventListener('input', function(evt) {
          if (isNaN(parseFloat(evt.target.value))) {
            evt.target.value = '0';
          }
        });