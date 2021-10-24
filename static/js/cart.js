// fetch('/checkout_stripe')
// 	.then((result) => {
// 		return result.json();
// 	})
// 	.then((data) => {
// 		// Initialize Stripe.js
// 		const stripe = Stripe(data.publicKey);
// 	});

fetch('/checkout_stripe')
	.then((result) => {
		return result.json();
	})
	.then((data) => {
		// Initialize Stripe.js
		const stripe = Stripe(data.publicKey);

		// new
		// Event handler
		document.querySelector('#stripeSubmitBtn').addEventListener('click', () => {
			// Get Checkout Session ID
			fetch('/stripe_checkout_session')
				.then((result) => {
					return result.json();
				})
				.then((data) => {
					console.log(data);
					// Redirect to Stripe Checkout
					return stripe.redirectToCheckout({ sessionId: data.sessionId });
				})
				.then((res) => {
					console.log(res);
				});
		});
	});

fetch('/checkout_stripe')
	.then((result) => {
		return result.json();
	})
	.then((data) => {
		// Initialize Stripe.js
		const stripe = Stripe(data.publicKey);

		// new
		// Event handler
		document.querySelector('#stripePayoutBtn').addEventListener('click', () => {
			// Get Checkout Session ID
			fetch('/stripe_payout_session')
				.then((result) => {
					return result.json();
				})
				.then((data) => {
					console.log(data);
					// Redirect to Stripe Checkout
					// redirect URL will be data.id
					//return stripe.redirectToCheckout({ sessionId: data.sessionId });
				})
				.then((res) => {
					//console.log(res);
				});
		});
	});
