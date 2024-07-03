document.addEventListener('DOMContentLoaded', (event) => {
    const socket = io.connect('http://' + document.domain + ':' + location.port);

    const chatInput = document.getElementById('chat-input');
    const sendMessageBtn = document.getElementById('send-message-btn');
    const chatMessages = document.getElementById('chat-messages');
    const playersList = document.getElementById('players');

    sendMessageBtn.addEventListener('click', () => {
        const message = chatInput.value.trim();
        if (message) {
            socket.emit('new_message', { username: getUsername(), message: message });
            chatInput.value = '';
        }
    });

    socket.on('connect', () => {
        const username = getUsername();
        socket.emit('join', { username: username });
    });

    socket.on('player_joined', (data) => {
        const messageItem = document.createElement('div');
        messageItem.innerHTML = `<span class="joined-message">${data.username} has joined the game.</span>`;
        chatMessages.appendChild(messageItem);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        updatePlayersList(data.username);
    });

    socket.on('player_left', (data) => {
        const messageItem = document.createElement('div');
        messageItem.innerHTML = `<span class="left-message">${data.username} has left the game.</span>`;
        chatMessages.appendChild(messageItem);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        removePlayerFromList(data.username);
    });

    socket.on('message_sent', (data) => {
        const messageItem = document.createElement('div');
        messageItem.innerHTML = `<strong>${data.username}</strong>: ${data.message}`;
        chatMessages.appendChild(messageItem);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    });

    socket.on('history_loaded', (data) => {
        data.history.forEach((msg) => {
            const messageItem = document.createElement('div');
            if (msg.username === 'System') {
                messageItem.innerHTML = `<span class="joined-message">${msg.message}</span>`;
            } else {
                messageItem.innerHTML = `<strong>${msg.username}</strong>: ${msg.message}`;
            }
            chatMessages.appendChild(messageItem);
        });
        chatMessages.scrollTop = chatMessages.scrollHeight;
    });

    function getUsername() {
        return document.getElementById('username').textContent;
    }

    function updatePlayersList(username) {
        const playerItem = document.createElement('li');
        playerItem.textContent = username;
        playersList.appendChild(playerItem);
    }

    function removePlayerFromList(username) {
        const playerItems = playersList.getElementsByTagName('li');
        for (let i = 0; i < playerItems.length; i++) {
            if (playerItems[i].textContent === username) {
                playersList.removeChild(playerItems[i]);
                break;
            }
        }
    }
});
