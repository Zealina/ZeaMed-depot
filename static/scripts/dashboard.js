document.addEventListener('DOMContentLoaded', function() {
    const sections = document.querySelectorAll('.section');
    const links = document.querySelectorAll('.sidebar ul li a');

    const createRoomBtn = document.getElementById('create-room-btn');
    const joinRoomBtn = document.getElementById('join-room-btn');
    const roomForm = document.getElementById('room-form');
    const roomFormSubmit = document.getElementById('room-form-submit');
    let actionType = ''; // To track whether creating or joining a room

    createRoomBtn.addEventListener('click', function() {
        roomForm.style.display = 'block';
        actionType = 'create';
    });

    joinRoomBtn.addEventListener('click', function() {
        roomForm.style.display = 'block';
        actionType = 'join';
    });

    roomForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const roomName = document.getElementById('room-name').value;

        fetch(actionType === 'create' ? '/api/v1/create-room' : '/api/v1/join-room', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ roomName })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(`${actionType === 'create' ? 'Room created' : 'Joined room'} successfully!`);
                if (data.redirect_url) {
                    window.location.href = data.redirect_url; // Redirect to the new page
                }
            } else {
                alert(`Failed to ${actionType} room: ${data.message}`);
            }
        })
        .catch(error => {
            alert(`Error: ${error.message}`);
        });

        roomForm.style.display = 'none';
        roomForm.reset();
    });

    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href.startsWith('#')) {
                e.preventDefault();
                const targetId = href.substring(1);
                sections.forEach(section => {
                    section.style.display = section.id === targetId ? 'block' : 'none';
                });
            } else {
                window.location.href = href;
            }
        });
    });
});
