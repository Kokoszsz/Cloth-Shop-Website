document.querySelector('.filter form').addEventListener('submit', function(e) {
  e.preventDefault();

  var form = e.target;
  var data = new FormData(form);

  fetch('/filtered-products', {
      method: 'POST',
      body: data
  }).then(function(response) {
      return response.json();
  }).then(function(data) {
      var productGrid = document.getElementById('product-grid');
      productGrid.innerHTML = '';

      data.products.forEach(function(product) {
          var productItem = document.createElement('div');
          productItem.className = 'product-item';

          var image = document.createElement('img');
          image.src = '/static/images/' + product.image;
          image.alt = product.name;
          productItem.appendChild(image);

          var name = document.createElement('h2');
          name.textContent = product.name;
          productItem.appendChild(name);

          var price = document.createElement('p');
          price.className = 'price';
          price.textContent = '$' + product.cost_to_show;
          productItem.appendChild(price);

          productGrid.appendChild(productItem);
      });
  });
});