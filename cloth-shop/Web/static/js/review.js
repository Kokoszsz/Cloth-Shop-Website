const reviewText = document.getElementById("reviewText");
const reviewButton = document.getElementById("reviewButton");
const reviewsContainer = document.getElementById("reviews");

async function submitReview() {
    event.preventDefault();
    clearError();
    const content = reviewText.value.trim();
    const productId = reviewButton.getAttribute('data-product-id');

    if (content.length < 5) {
        // Display error for review that is too short
        showError("Review is too short (minimum 5 characters)");
        return;
    }

    if (content.length > 1000) {
        // Display error for review that is too long
        showError("Review is too long (maximum 1000 characters)");
        return;
    }

    try {
        const response = await fetch(`/api/v1/products/${productId}/reviews`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ content }),
        });

        const data = await response.json();
        if (response.status === 201) {
            displayReview(content, data.id);
        } 
        else {
            showError(data.error.message);
        }
    } 
    catch (error) {
        console.error('An error occurred:', error);
    }
};

function showError(message) {
    const errorDiv = document.createElement("div");
    errorDiv.classList.add("error");
    errorDiv.textContent = message;

    // Assuming you have an error container element
    const errorContainer = document.getElementById("errorContainer");
    errorContainer.innerHTML = "";
    errorContainer.appendChild(errorDiv);
}

function clearError() {
    const errorContainer = document.getElementById("errorContainer");
    errorContainer.textContent = "";
}

async function removeReview(buttonElement) {
    const reviewContainer = buttonElement.closest('.reviewContainer');
    const reviewId = reviewContainer.getAttribute('data-review-id');
    //console.log(reviewId)
    try {
        const response = await fetch(`/api/v1/reviews/${reviewId}`, {
            method: 'DELETE',
        });

        if (response.status === 204) {
            if (reviewContainer) {
                reviewsContainer.removeChild(reviewContainer);
            }
        } else {
            console.error('Failed to remove review');
        }
    } catch (error) {
        console.error('An error occurred:', error);
    }
}


function displayReview(text, reviewId) {
    // Create reviewContainer div
    const reviewContainer = document.createElement("div");
    reviewContainer.classList.add("reviewContainer");
    reviewContainer.dataset.reviewId = reviewId;

    // Create reviewHeader div
    const reviewHeader = document.createElement("div");
    reviewHeader.classList.add("reviewHeader");

    // Create headerLeft div
    const headerLeft = document.createElement("div");
    headerLeft.classList.add("headerLeft");

    // Create userName span
    const userName = document.createElement("span");
    userName.classList.add("userName");
    // Replace this with the logic to get the username by ID
    userName.textContent = "User Name"; // Example username

    // Create userIcon div
    const userIcon = document.createElement("div");
    // Add the logic to set the user icon

    // Append userName and userIcon to headerLeft
    headerLeft.appendChild(userName);
    headerLeft.appendChild(userIcon);

    // Create reviewContent div
    const reviewContent = document.createElement("div");
    reviewContent.classList.add("reviewContent");
    // Set innerHTML to properly render line breaks
    reviewContent.innerHTML = text;

    // Enable word wrapping
    reviewContent.style.wordWrap = "break-word";

    // Append headerLeft, reviewContent, and headerRight to reviewHeader
    reviewHeader.appendChild(headerLeft);
    reviewHeader.appendChild(reviewContent);


    // Create reviewDate span
    const reviewDate = document.createElement("span");
    reviewDate.classList.add("reviewDate");
    // Replace this with the review date
    reviewDate.textContent = "Review Date"; // Example date

    // Append reviewDate to headerRight
    headerLeft.appendChild(reviewDate);

    const removeContainer = document.createElement("div");
    removeContainer.classList.add("removeContainer");
    reviewContent.style.textAlign = "right";

    // Create removeButton button
    const removeButton = document.createElement("button");
    removeButton.classList.add("removeButton");
    removeButton.textContent = "Remove";
    removeButton.addEventListener("click", function () {
        removeReview(removeButton);
    });
    
    // Append reviewHeader and removeButton to reviewContainer
    removeContainer.appendChild(removeButton)
    reviewContainer.appendChild(reviewHeader);
    reviewContainer.appendChild(removeContainer);

    // Append reviewContainer to reviewsContainer
    reviewsContainer.appendChild(reviewContainer);

    // Clear the reviewText input
    reviewText.value = "";
}


