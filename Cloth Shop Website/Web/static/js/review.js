const reviewText = document.getElementById("reviewText");
const reviewButton = document.getElementById("reviewButton");
const reviewsContainer = document.getElementById("reviews");

async function submitReview() {
    event.preventDefault();
    const content = reviewText.value.trim();
    const productId = reviewButton.getAttribute('data-product-id');
    if (content.length > 0) {
        try {
            const response = await fetch('/save_review', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ content, productId: productId}),
            });

            if (response.ok) {
                const data = await response.json();
                if (data.message == 'Review saved successfully') {
                    displayReview(content, data.id);
                }
            } 
            else {
                console.error('Failed to submit review');
            }
        } 
        catch (error) {
            console.error('An error occurred:', error);
        }
    }
};

async function removeReview(buttonElement) {
    const reviewContainer = buttonElement.closest('.reviewContainer');
    const reviewId = reviewContainer.getAttribute('data-review-id');
    //console.log(reviewId)
    try {
        const response = await fetch('/delete_review', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ reviewId }),
        });

        if (response.ok) {
            const data = await response.json();
            if (data.success) {
                if (reviewContainer) {
                    reviewsContainer.removeChild(reviewContainer);
                }
            }
        } else {
            console.error('Failed to remove review');
        }
    } catch (error) {
        console.error('An error occurred:', error);
    }
}


function displayReview(text, reviewId) {
    const reviewContainer = document.createElement("div");
    reviewContainer.classList.add("reviewContainer");
    reviewContainer.id = 'reviewContainer';
    reviewContainer.setAttribute("data-review-id", reviewId);

    const reviewDiv = document.createElement("div");
    reviewDiv.classList.add("review");
    reviewDiv.textContent = text;

    const removeButton = document.createElement("button");
    removeButton.classList.add("removeButton");
    removeButton.textContent = "Remove";

    removeButton.addEventListener("click", function() {
        removeReview(removeButton);
    });

    reviewContainer.appendChild(reviewDiv);
    reviewContainer.appendChild(removeButton);

    reviewsContainer.appendChild(reviewContainer);
    reviewText.value = "";
}
