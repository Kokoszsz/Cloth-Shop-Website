document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.remove-from-basket').forEach(item => {
    item.addEventListener('click', event => {
      const productId = item.getAttribute('id')
      const xhr = new XMLHttpRequest();
      xhr.open('DELETE', `/basket/${productId}`, true);
      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.onload = () => {
        if (xhr.status === 200) {
          const response = JSON.parse(xhr.responseText);
          if (response.success) {
            const basketItem = document.getElementById(`basket-item-${productId}`);
            basketItem.parentNode.removeChild(basketItem);
            document.querySelector('.total-cost').textContent = response.totalCost;
          } else {
            alert(response.message);
          }
        }
      };
      xhr.send();
    });
  });
});