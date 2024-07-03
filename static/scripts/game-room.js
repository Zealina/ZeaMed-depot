document.addEventListener('DOMContentLoaded', (event) => {
    const socket = io.connect('http://' + document.domain + ':' + location.port);

    const chatInput = document.getElementById('chat-input');
    const sendMessageBtn = document.getElementById('send-message-btn');
    const chatMessages = document.getElementById('chat-messages');
    const playersList = document.getElementById('players');

    sendMessageBtn.addEventListener('click', () => {
        const message = chatInput.value;
        if (message) {
            socket.emit('chat_message', { message: message });
            chatInput.value = '';
        }
    });

    socket.on('connect', () => {
        const username = document.getElementById('username').textContent;
        socket.emit('join', { username: username });
    });

    socket.on('player_joined', (data) => {
        const playerItem = document.createElement('li');
        playerItem.textContent = data.username;
        playersList.appendChild(playerItem);

        const messageItem = document.createElement('div');
        messageItem.textContent = `${data.username} has joined the game.`;
        chatMessages.appendChild(messageItem);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    });

    socket.on('chat_message', (data) => {
        const messageItem = document.createElement('div');
        messageItem.textContent = data.message;
        chatMessages.appendChild(messageItem);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    });

    const startGameBtn = document.getElementById('start-game-btn');
    startGameBtn?.addEventListener('click', () => {
        socket.emit('start_game', {});
    });

    const addQuestionBtn = document.getElementById('add-question-btn');
    addQuestionBtn?.addEventListener('click', () => {
        const questionText = prompt('Enter the question:');
        if (questionText) {
            socket.emit('add_question', { question: questionText });
        }
    });

    socket.on('question_added', (data) => {
        alert(`Question added: ${data.question}`);
    });

    socket.on('game_started', (data) => {
        alert('Game started with questions: ' + data.questions.join(', '));
    });
});
