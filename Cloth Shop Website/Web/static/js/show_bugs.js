// Define bug data for each page
const bugProductDetail = [
    { marginLeft: 17, marginTop: 10, width: 250, height: 150, title: 'Magnifier featrue', description: 'Magnifier featrue does not work properly for some products.' },
];

const bugBasket = [
    { marginLeft: 17, marginTop: 10, width: 150, height: 150, title: 'Delete product', description: 'Products do not disappear immediately after clicking trash icon.' },
    { marginLeft: 17, marginTop: 10, width: 150, height: 150, title: 'Increase number of products', description: 'Number of products can be increased but this number changes to 1 after reloading page.' }
];

const bugCloth = [
    { marginLeft: 17, marginTop: 10, width: 150, height: 150, title: 'Min and Max value', description: 'Min value and Max value are overlapping other elements when making window shorter.' },
];

let bugsVisible = false;

function getCurrentPage() {

    const currentUrl = window.location.href;
    console.log(currentUrl)

    const pathName = new URL(currentUrl).pathname
    if (pathName === '/') {
        return 'home';
    } else if (pathName === '/cloth') {
        return 'cloth';
    } else if (currentUrl.includes('/product_detail')) {
        return 'product_detail';
    } else if (pathName === '/account') {
        return 'account';
    } else if (pathName === '/basket') {
        return 'basket';
    } else if (pathName === '/login') {
        return 'login';
    } else if (pathName === '/checkout') {
        return 'checkout';
    }

    return 'unknown'; 
}

document.getElementById('showBugsButton').addEventListener('click', function () {
    // Determine the current page (you can use the window.location or another method)
    const currentPage = getCurrentPage(); // Implement this function to return the current page

    if (bugsVisible) {
        hideBugs();
    } else {
        // Show bugs based on the current page
        console.log(currentPage)
        switch (currentPage) {
            case 'product_detail':
                showBugs(bugProductDetail);
                break;
            case 'basket':
                showBugs(bugBasket);
                break;
            case 'cloth':
                showBugs(bugCloth);
                break;
            // Add more cases for other pages
            default:
                // Handle cases for pages with no bugs
                break;
        }
    }
});


function showBugs(bugData) {
    const bugElement = document.createElement('div');
    bugElement.classList.add('bug-indicator');
    bugElement.style.position = 'absolute';
    bugElement.style.zIndex = '1';
    bugElement.style.left = '0';
    bugElement.style.top = '0';
    bugElement.style.width = '100%';
    bugElement.style.height = `${document.documentElement.scrollHeight}px`;
    bugElement.style.backgroundColor = 'rgba(0, 0, 0, 0.4';
    bugData.forEach(bug => {

        // Create a tooltip for bug description
        const tooltip = document.createElement('div');
        tooltip.classList.add('tooltip');
        bugElement.style.position = 'absolute';
        tooltip.style.display = 'flex';
        tooltip.style.flexDirection = 'column';
        tooltip.style.alignItems = 'center';
        tooltip.style.justifyContent = 'center';
        tooltip.style.backgroundColor = 'white';
        tooltip.style.marginLeft = `${bug.marginLeft}%`;
        tooltip.style.marginTop = `${bug.marginTop}%`;
        tooltip.style.padding = '20px';
        tooltip.style.border = '1px solid #888';
        tooltip.style.width = bug.width + 'px';
        tooltip.style.height = bug.height + 'px';
        tooltip.style.textAlign = 'center';

        // Title of the bug with bigger font
        const title = document.createElement('div');
        title.textContent = bug.title; // Add a 'title' property to your bug data
        title.style.fontSize = '20px'
        title.style.fontWeight = 'bold'

        // Description of the bug with smaller font
        const description = document.createElement('div');
        description.classList.add('bug-description');
        description.textContent = bug.description;

        tooltip.appendChild(title);
        tooltip.appendChild(description);
        bugElement.appendChild(tooltip);

    document.body.appendChild(bugElement);
        
    });

    bugsVisible = true; // Update visibility flag
}


function hideBugs() {
    // Remove all bug indicators and descriptions
    const bugIndicators = document.querySelectorAll('.bug-indicator');
    bugIndicators.forEach(bugIndicator => {
        document.body.removeChild(bugIndicator);
    });

    bugsVisible = false; // Update visibility flag
}
