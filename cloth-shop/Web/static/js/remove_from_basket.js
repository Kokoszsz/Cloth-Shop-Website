document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.remove-from-basket').forEach(item => {
    item.addEventListener('click', event => {
      const productId = item.getAttribute('id')
      const xhr = new XMLHttpRequest();
      xhr.open('DELETE', `/api/v1/basket/items/${productId}`, true);
      xhr.onload = () => {
        const response = JSON.parse(xhr.responseText);
        if (xhr.status === 200) {
          const basketItem = document.getElementById(`basket-item-${productId}`);
          basketItem.parentNode.removeChild(basketItem);
          document.querySelector('.total-cost').textContent = response.total_cost;
        } else {
          alert(response.error.message);
        }
      };
      xhr.send();
    });
  });
});
