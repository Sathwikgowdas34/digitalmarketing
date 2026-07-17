/**
 * Payment Processing
 */

class PaymentProcessor {
    constructor() {
        this.stripePublicKey = document.querySelector('[data-stripe-key]')?.dataset.stripeKey;
        this.razorpayKey = document.querySelector('[data-razorpay-key]')?.dataset.razorpayKey;
    }

    async processStripePayment(orderId) {
        try {
            const response = await fetchJSON(`/payments/stripe/create-checkout-session/${orderId}`, {
                method: 'POST'
            });

            if (response.sessionId && window.Stripe) {
                const stripe = Stripe(this.stripePublicKey);
                const { error } = await stripe.redirectToCheckout({
                    sessionId: response.sessionId
                });
                
                if (error) {
                    showToast(error.message, 'danger');
                }
            }
        } catch (error) {
            showToast('Payment processing failed', 'danger');
        }
    }

    async processRazorpayPayment(orderId) {
        try {
            const response = await fetchJSON(`/payments/razorpay/create-order/${orderId}`, {
                method: 'POST'
            });

            if (response.razorpay_order_id && window.Razorpay) {
                const options = {
                    key: this.razorpayKey,
                    amount: response.amount,
                    currency: response.currency,
                    order_id: response.razorpay_order_id,
                    handler: (response) => {
                        this.verifyRazorpayPayment(orderId, response);
                    },
                    prefill: {
                        email: document.querySelector('[data-user-email]')?.dataset.userEmail
                    }
                };
                
                const razorpay = new Razorpay(options);
                razorpay.open();
            }
        } catch (error) {
            showToast('Payment initialization failed', 'danger');
        }
    }

    async verifyRazorpayPayment(orderId, paymentResponse) {
        try {
            const formData = new FormData();
            formData.append('order_id', orderId);
            formData.append('payment_id', paymentResponse.razorpay_payment_id);
            formData.append('signature', paymentResponse.razorpay_signature);

            const response = await fetch('/payments/razorpay/verify', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                window.location.href = '/downloads';
            } else {
                showToast('Payment verification failed', 'danger');
            }
        } catch (error) {
            showToast('Verification error', 'danger');
        }
    }
}

const paymentProcessor = new PaymentProcessor();
