// js/components.js
document.addEventListener('DOMContentLoaded', function() {
    // Load header
    fetch('templates/includes/header.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('header-placeholder').innerHTML = data;
            // Initialize mobile menu after header is loaded
            initializeMobileMenu();
        });

    // Load footer (if needed)
    // fetch('includes/footer.html')
    //     .then(response => response.text())
    //     .then(data => {
    //         document.getElementById('footer-placeholder').innerHTML = data;
    //     });
});

// Function to initialize mobile menu functionality
function initializeMobileMenu() {
    const mobileMenu = document.querySelector('.mobile-menu');
    const navLinks = document.querySelector('.nav-links');

    // Check if elements exist to avoid errors
    if (mobileMenu && navLinks) {
        // Function to toggle the mobile menu
        mobileMenu.addEventListener('click', () => {
            navLinks.classList.toggle('active'); // Toggle the active class to show/hide the menu
        });

        // Close the menu when clicking outside of it
        document.addEventListener('click', (event) => {
            if (!navLinks.contains(event.target) && !mobileMenu.contains(event.target)) {
                navLinks.classList.remove('active'); // Hide the menu if clicked outside
            }
        });
    }
}

// Initialize mobile menu functionality
function initializeMobileMenu() {
    const mobileMenu = document.querySelector('.mobile-menu');
    const navLinks = document.querySelector('.nav-links');

    if (mobileMenu && navLinks) {
        mobileMenu.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            mobileMenu.classList.toggle('active');
        });
    }
}