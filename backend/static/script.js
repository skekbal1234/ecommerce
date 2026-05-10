let products = [];
let cart = [];

async function loadProducts() {
    try {
        const response = await fetch('/product');
        products = await response.json();
        displayProducts();
    } catch (error) {
        console.error('Error loading products:', error);
    }
}

function displayProducts() {
    const productList = document.getElementById('product-list');
    productList.innerHTML = products.map(product => `
        <div class="product-card">
            <img src="${product.image}" alt="${product.name}">
            <div class="details">
                <h3>${product.name}</h3>
                <p class="category">${product.category}</p>
                <p class="price">$${product.price.toFixed(2)}</p>
                <p class="description">${product.description}</p>
                <button onclick="addToCart(${product.id})">Add to Cart</button>
            </div>
        </div>
    `).join('');
}

function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    const existing = cart.find(item => item.id === productId);
    if (existing) {
        existing.quantity++;
    } else {
        cart.push({ ...product, quantity: 1 });
    }
    displayCart();
}

function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    displayCart();
}

function updateQuantity(productId, quantity) {
    const item = cart.find(item => item.id === productId);
    if (item) {
        item.quantity = Math.max(1, quantity);
        if (item.quantity === 0) {
            removeFromCart(productId);
        } else {
            displayCart();
        }
    }
}

function displayCart() {
    const cartItems = document.getElementById('cart-items');
    const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
    cartItems.innerHTML = cart.length === 0 ? '<p>Your selection is empty. Browse our exquisite collection above.</p>' :
        cart.map(item => `
            <div class="cart-item">
                <div>
                    <strong>${item.name}</strong>
                    <p>$${item.price.toFixed(2)}</p>
                </div>
                <div>
                    <input type="number" min="1" value="${item.quantity}" onchange="updateQuantity(${item.id}, this.value)">
                    <button onclick="removeFromCart(${item.id})">Remove</button>
                </div>
            </div>
        `).join('') + `<div class="cart-summary"><span>Total</span><strong>$${total.toFixed(2)}</strong></div>`;
}

async function checkout() {
    if (cart.length === 0) {
        alert('Your selection is empty! Please add some exquisite items to your cart.');
        return;
    }
    try {
        const response = await fetch('/checkout', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ cart })
        });
        const result = await response.json();
        document.getElementById('checkout-message').textContent = result.message + (result.total ? ` - Total: $${result.total}` : '');
        cart = [];
        displayCart();
    } catch (error) {
        console.error('Checkout error:', error);
    }
}

document.getElementById('checkout-btn').addEventListener('click', checkout);

loadProducts();