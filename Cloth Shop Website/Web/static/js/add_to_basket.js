document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.add-to-basket').forEach(function(link) {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      var productID = this.getAttribute('data-product_id');

      var modal = document.getElementById("myModal");
			modal.style.display = "block";


      var xhr = new XMLHttpRequest();
      xhr.open("POST", "/add-to-basket");
      xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
      xhr.send(JSON.stringify({ product_ID: productID }));
    });
  });
});




function closeModal() {
  var modal = document.getElementById("myModal");

	modal.style.display = "none";
}
