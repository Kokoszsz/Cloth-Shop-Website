// Example list of countries
var countries = ["USA", "Canada", "UK", "Australia", "Germany", "France", "Italy", "Spain", "Japan", "China", "India", "Brazil", "Poland"];

// Get the input field and attach event listeners
var countryInput = document.getElementById("country");
var suggestionsContainer = document.getElementById("suggestions-container");

// Event listener for input field focus
countryInput.addEventListener("focus", function() {
  filterSuggestions();
  showSuggestions();
});

// Event listener for input field blur
countryInput.addEventListener("blur", function() {
  setTimeout(hideSuggestions, 100); 
});

// Event listener for input field keyup
countryInput.addEventListener("keyup", function() {
    filterSuggestions();
    showSuggestions();
});

// Function to show suggestions
function showSuggestions() {
  suggestionsContainer.style.display = "block";
}

// Function to hide suggestions
function hideSuggestions() {
  suggestionsContainer.style.display = "none";
}

// Function to filter suggestions based on input value
function filterSuggestions() {
  var inputText = countryInput.value.toLowerCase();
  var filteredCountries = countries.filter(function(country) {
    return country.toLowerCase().startsWith(inputText);
  });

  displaySuggestions(filteredCountries);
}

// Function to display suggestions in a dropdown list
function displaySuggestions(suggestions) {
  suggestionsContainer.innerHTML = "";

  suggestions.forEach(function(suggestion) {
    var suggestionItem = document.createElement("div");
    suggestionItem.textContent = suggestion;
    suggestionItem.classList.add("suggestion-item");

    suggestionItem.addEventListener("click", function() {
      countryInput.value = suggestion;
      hideSuggestions();
    });

    suggestionsContainer.appendChild(suggestionItem);
  });
}

