document.getElementById('login-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const response = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    });

    const result = await response.json();
    const messageDiv = document.getElementById('message');

    if (response.ok) {
        messageDiv.innerHTML = `<p class="success">${result.message}</p>`;
        // Redirect to home page or dashboard after a short delay
        setTimeout(() => {
            window.location.href = '/api/v1/dashboard'; // change this to the desired redirect URL
        }, 2000);
    } else {
        messageDiv.innerHTML = `<p class="error">${result.message}</p>`;
    }
});
