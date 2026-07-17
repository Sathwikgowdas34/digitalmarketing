/**
 * Cart Management
 */

class Cart {
    constructor() {
        this.items = storage.get('cart') || [];
    }

    addProduct(product) {
        const existingItem = this.items.find(item => item.id === product.id);
        
        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            this.items.push({ ...product, quantity: 1 });
        }
        
        this.save();
        this.updateUI();
        showToast('Product added to cart', 'success');
    }

    removeProduct(productId) {
        this.items = this.items.filter(item => item.id !== productId);
        this.save();
        this.updateUI();
        showToast('Product removed from cart', 'info');
    }

    updateQuantity(productId, quantity) {
        const item = this.items.find(item => item.id === productId);
        if (item) {
            item.quantity = Math.max(1, quantity);
            this.save();
            this.updateUI();
        }
    }

    getTotal() {
        return this.items.reduce((total, item) => total + (item.price * item.quantity), 0);
    }

    getItemCount() {
        return this.items.reduce((count, item) => count + item.quantity, 0);
    }

    clear() {
        this.items = [];
        this.save();
        this.updateUI();
    }

    save() {
        storage.set('cart', this.items);
    }

    updateUI() {
        const cartCount = document.querySelector('.cart-count');
        const cartTotal = document.querySelector('.cart-total');
        
        if (cartCount) cartCount.textContent = this.getItemCount();
        if (cartTotal) cartTotal.textContent = formatCurrency(this.getTotal());
    }
}

const cart = new Cart();
cart.updateUI();
