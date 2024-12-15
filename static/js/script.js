// Initialize AOS (Animate On Scroll)
AOS.init({
    duration: 1000,
    once: true
});

// Load current year
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('currentYear').textContent = new Date().getFullYear();
});

// Theme toggle functionality
document.addEventListener('DOMContentLoaded', () => {
    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    const themeIcon = document.getElementById('theme-icon');

    // Check the saved theme in localStorage
    const currentTheme = localStorage.getItem('theme') || 'light';
    if (currentTheme === 'dark') {
        document.body.classList.add('dark-theme');
        themeIcon.classList.replace('fa-sun', 'fa-moon'); // Change icon to moon
    }

    themeToggleBtn.addEventListener('click', () => {
        // Toggle between light and dark themes
        if (document.body.classList.contains('dark-theme')) {
            document.body.classList.remove('dark-theme');
            localStorage.setItem('theme', 'light');
            themeIcon.classList.replace('fa-moon', 'fa-sun'); // Change icon to sun
        } else {
            document.body.classList.add('dark-theme');
            localStorage.setItem('theme', 'dark');
            themeIcon.classList.replace('fa-sun', 'fa-moon'); // Change icon to moon
        }
    });
});

// Header scroll effect
window.addEventListener('scroll', () => {
    const header = document.querySelector('.header');
    header.classList.toggle('scrolled', window.scrollY > 100);
}, { passive: true }); // Add passive option for better performance

// Mobile menu functionality
document.addEventListener('DOMContentLoaded', () => {
    const mobileMenu = document.querySelector('.mobile-menu');
    const navLinks = document.querySelector('.nav-links');
    const closeButton = document.querySelector('.close-btn');

    // Function to toggle the mobile menu
    mobileMenu.addEventListener('click', () => {
        navLinks.classList.toggle('active'); // Toggle the active class to show/hide the menu
    });

    // Close the menu when clicking the close button
    if (closeButton) {
        closeButton.addEventListener('click', () => {
            navLinks.classList.remove('active'); // Hide the menu
        });
    }

    // Close the menu when clicking outside of it
    document.addEventListener('click', (event) => {
        if (!navLinks.contains(event.target) && !mobileMenu.contains(event.target)) {
            navLinks.classList.remove('active'); // Hide the menu if clicked outside
        }
    });
});

// Newsletter Form Submission
document.querySelector('.newsletter-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const email = this.querySelector('input[type="email"]').value;
    alert('Thank you for subscribing! We will keep you updated.');
    this.reset();
});

// Function to load HTML content into specified elements
function loadHTML(id, file) {
    fetch(file)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(data => {
            document.getElementById(id).innerHTML = data;
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}