/**
 * Wishlist Management
 */

class Wishlist {
    constructor() {
        this.items = storage.get('wishlist') || [];
        this.init();
    }

    init() {
        document.querySelectorAll('.wishlist-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.toggle(e));
        });
    }

    toggle(event) {
        event.preventDefault();
        const productId = event.currentTarget.dataset.productId;
        const productTitle = event.currentTarget.dataset.productTitle;
        
        if (this.has(productId)) {
            this.remove(productId);
        } else {
            this.add({ id: productId, title: productTitle });
        }
        
        this.updateUI(event.currentTarget);
    }

    add(product) {
        if (!this.has(product.id)) {
            this.items.push(product);
            this.save();
            showToast(`${product.title} added to wishlist`, 'success');
        }
    }

    remove(productId) {
        this.items = this.items.filter(item => item.id !== productId);
        this.save();
        showToast('Removed from wishlist', 'info');
    }

    has(productId) {
        return this.items.some(item => item.id === productId);
    }

    getItems() {
        return this.items;
    }

    clear() {
        this.items = [];
        this.save();
    }

    save() {
        storage.set('wishlist', this.items);
    }

    updateUI(element) {
        const icon = element.querySelector('i');
        if (this.has(element.dataset.productId)) {
            icon.classList.remove('far');
            icon.classList.add('fas');
            element.classList.add('active');
        } else {
            icon.classList.remove('fas');
            icon.classList.add('far');
            element.classList.remove('active');
        }
    }
}

const wishlist = new Wishlist();
