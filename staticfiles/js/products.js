const loadProducts = async (filter = "", limit = 3) => {
    const response = await fetch('website\static\data\products.json');
    const productsData = await response.json();
    
    const productsContainer = document.getElementById('products-container');
    productsContainer.innerHTML = ''; // Clear existing products

    // Filter the products based on the search input
    const filteredProducts = productsData.filter(product => 
        product.name.toLowerCase().includes(filter.toLowerCase())
    );

    const categories = [...new Set(filteredProducts.map(p => p.category))];

    categories.forEach(category => {
        const categoryDiv = document.createElement('div');
        categoryDiv.classList.add('category-section');
        
        const categoryTitle = document.createElement('h3');
        categoryTitle.textContent = category;
        categoryDiv.appendChild(categoryTitle);

        const productsGrid = document.createElement('div');
        productsGrid.classList.add('products-grid');

        // Limit the number of displayed products
        const limitedProducts = filteredProducts.filter(p => p.category === category).slice(0, limit);
        limitedProducts.forEach(product => {
            const productItem = document.createElement('div');
            productItem.classList.add('product-item');
            productItem.innerHTML = `
                <img src="${product.image}" alt="${product.name}" class="product-image">
                <h4>${product.name}</h4>
                <p><strong>Description:</strong> ${product.description}</p>
                <p><strong>Dimensions:</strong> ${product.dimensions}</p>
                <p><strong>Key Features:</strong> ${product.features}</p>
            `;
            productsGrid.appendChild(productItem);

            // Add click event to the image
            const productImage = productItem.querySelector('.product-image');
            productImage.addEventListener('click', () => {
                showImageModal(product.image, product.name); // Show the enlarged image
            });
        });

        const viewMoreButton = document.createElement('button');
        viewMoreButton.textContent = 'View More';
        viewMoreButton.classList.add('view-more-button');
        viewMoreButton.addEventListener('click', () => showModal(category, filteredProducts));

        // Append the products grid and button to the category section
        categoryDiv.appendChild(productsGrid);
        categoryDiv.appendChild(viewMoreButton);
        
        productsContainer.appendChild(categoryDiv);
    });
};

// Function to show the modal with an enlarged image
const showImageModal = (imageSrc, altText) => {
    const imageModal = document.getElementById('imageModal');
    const modalImage = document.getElementById('modalImage');
    modalImage.src = imageSrc;
    modalImage.alt = altText;
    imageModal.style.display = 'block'; // Show the image modal
};

// Close image modal when clicking on the close button
document.querySelector('.close-image').onclick = function() {
    document.getElementById('imageModal').style.display = 'none';
};

// Close image modal when clicking outside of the modal content
window.onclick = function(event) {
    const imageModal = document.getElementById('imageModal');
    if (event.target === imageModal) {
        imageModal.style.display = 'none';
    }
};

// Function to show the modal with all products in a category
const showModal = (category, allProducts) => {
    const modal = document.getElementById('productModal');
    const modalProductContainer = document.getElementById('modalProductContainer');
    modalProductContainer.innerHTML = ''; // Clear existing content

    const productsInCategory = allProducts.filter(product => product.category === category);
    productsInCategory.forEach(product => {
        const productItem = document.createElement('div');
        productItem.classList.add('modal-product-item'); // Updated class for modal grid
        productItem.innerHTML = `
            <img src="${product.image}" alt="${product.name}" class="modal-product-image">
            <h4>${product.name}</h4>
            <p><strong>Description:</strong> ${product.description}</p>
            <p><strong>Dimensions:</strong> ${product.dimensions}</p>
            <p><strong>Key Features:</strong> ${product.features}</p>
        `;
        modalProductContainer.appendChild(productItem);

        // Add click event to the image in the modal as well
        const modalImage = productItem.querySelector('.modal-product-image');
        modalImage.addEventListener('click', () => {
            showImageModal(product.image, product.name);
        });
    });

    // Set up the close functionality for the modal
    const closeModal = document.querySelector('.close');
    closeModal.onclick = function() {
        modal.style.display = 'none'; // Close the modal
    };

    // Close modal when clicking outside of the modal content
    window.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    };

    modal.style.display = 'block'; // Show the modal
};

// Create and insert search input
const searchInput = document.createElement('input');
searchInput.type = 'search';
searchInput.placeholder = 'Search for products...';
searchInput.addEventListener('input', () => {
    loadProducts(searchInput.value);
});

// Insert search input into the DOM
const searchContainer = document.getElementById('search-container');
searchContainer.appendChild(searchInput);

// Initial load
loadProducts();