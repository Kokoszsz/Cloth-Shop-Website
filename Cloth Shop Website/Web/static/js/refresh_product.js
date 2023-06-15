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
  
            var productDetails = document.createElement('div');
            productDetails.className = 'product-details';
            productItem.appendChild(productDetails);
  
            var productData = document.createElement('div');
            productData.className = 'product-data';
            productDetails.appendChild(productData);

            var productLink = document.createElement('a');
            productLink.href = 'cloth/product_detail/' + product.id; 
            productLink.className = 'product-link';
            productData.appendChild(productLink);
  
            var name = document.createElement('h2');
            name.textContent = product.name;
            productLink.appendChild(name);
  
            var price = document.createElement('p');
            price.className = 'price';
            price.textContent = product.cost.toFixed(2) + ' $';
            productData.appendChild(price);
  
            var addToBasket = document.createElement('a');
            addToBasket.className = 'add-to-basket';
            addToBasket.href = '#';
            addToBasket.dataset.product_id = product.id;
            productDetails.appendChild(addToBasket);
  
            var cartPlusSvg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
            cartPlusSvg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
            cartPlusSvg.setAttribute('width', '22');
            cartPlusSvg.setAttribute('height', '22');
            cartPlusSvg.setAttribute('fill', 'currentColor');
            cartPlusSvg.setAttribute('class', 'bi bi-cart-plus');
            cartPlusSvg.setAttribute('viewBox', '0 0 16 16');
            addToBasket.appendChild(cartPlusSvg);
  
            var path1 = document.createElementNS('http://www.w3.org/2000/svg', 'path');
            path1.setAttribute('d', 'M9 5.5a.5.5 0 0 0-1 0V7H6.5a.5.5 0 0 0 0 1H8v1.5a.5.5 0 0 0 1 0V8h1.5a.5.5 0 0 0 0-1H9V5.5z');
            cartPlusSvg.appendChild(path1);
  
            var path2 = document.createElementNS('http://www.w3.org/2000/svg', 'path');
            path2.setAttribute('d', 'M.5 1a.5.5 0 0 0 0 1h1.11l.401 1.607 1.498 7.985A.5.5 0 0 0 4 12h1a2 2 0 1 0 0 4 2 2 0 0 0 0-4h7a2 2 0 1 0 0 4 2 2 0 0 0 0-4h1a.5.5 0 0 0 .491-.408l1.5-8A.5.5 0 0 0 14.5 3H2.89l-.405-1.621A.5.5 0 0 0 2 1H.5zm3.915 10L3.102 4h10.796l-1.313 7h-8.17zM6 14a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm7 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0z');
            cartPlusSvg.appendChild(path2);
  
            productGrid.appendChild(productItem);
        });
    });
  });
  