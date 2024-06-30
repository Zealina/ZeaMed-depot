document.addEventListener('DOMContentLoaded', function () {
    const registerForm = document.getElementById('register-form');

    registerForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const email = document.getElementById('email').value;
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm-password').value;

        if (password !== confirmPassword) {
            alert('Passwords do not match');
            return;
        }

        const payload = {
            email: email,
            username: username,
            password: password,
            firstname: '',  // Adjust these fields based on your actual form
            lastname: ''    // Adjust these fields based on your actual form
        };

        try {
            const response = await fetch('/api/v1/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const result = await response.json();

            if (response.status === 201) {
                alert('Registration successful!');
                window.location.href = '/api/v1/auth/login';  // Redirect to login page
            } else {
                alert(`Registration failed: ${result.message}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while registering. Please try again later.');
        }
    });
});
