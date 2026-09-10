document.addEventListener('DOMContentLoaded', function() {
  document.body.addEventListener('click', function(e) {
    var link = e.target.closest('.add-to-basket');
    if (link) {
      e.preventDefault();
      var productID = Number(link.getAttribute('data-product_id'));

      var xhr = new XMLHttpRequest();
      xhr.open("POST", "/api/v1/basket/items");
      xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
      xhr.onload = function() {
        if (xhr.status === 201) {
          var modal = document.getElementById("myModal");
          modal.style.display = "block";
          document.body.style.overflow = 'hidden';
        } else {
          console.error('Adding to the basket failed with status ' + xhr.status);
        }
      };
      xhr.send(JSON.stringify({ product_id: productID }));
    }
  });
});







function closeModal() {
  var modal = document.getElementById("myModal");

  document.body.style.overflow = 'auto';
  modal.style.display = "none";
}
