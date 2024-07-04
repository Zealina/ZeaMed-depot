document.addEventListener('DOMContentLoaded', (event) => {
    const socket = io.connect('http://' + document.domain + ':' + location.port);

    const chatInput = document.getElementById('chat-input');
    const sendMessageBtn = document.getElementById('send-message-btn');
    const chatMessages = document.getElementById('chat-messages');
    const playersList = document.getElementById('players');
    const chatInputForm = document.getElementById('chat-input-form');

    const isCreator = document.body.getAttribute('data-is-creator') === 'True';
    
    if (isCreator) {
        const formAddQuestion = document.getElementById('form-add-question');
        const closePopUp = document.getElementById('close-popup');
        const popupAddQuestion = document.getElementById('popup-add-question');
        const addQuestionBtn = document.getElementById('add-question-btn');

        closePopUp.addEventListener('click', () => popupAddQuestion.setAttribute('aria-hidden', 'true'));

        addQuestionBtn.addEventListener('click', () => popupAddQuestion.setAttribute('aria-hidden', 'false'));

        function validateQuestion(options, correct) {
            if (!options.includes(',,')) {
                throw Error('Must be more than One Option');
            }
            const optionArray = options.split(',,');

            if (optionArray.includes('')) {
                throw Error('Empty string cannot be an option');
            }

            if (isNaN(Number(correct))) {
                throw Error('Correct Option Index must be a Number');
            }
            if (Number(correct) < 0 || Number(correct) > optionArray.length - 1) {
                throw Error(`Correct Index is must be between 0 and ${optionArray.length - 1} `);
            }
        };

        formAddQuestion.addEventListener('submit', e => {
            try {
                e.preventDefault();
                const question = document.getElementById('question-input').value.trim();
                const options = document.getElementById('options-input').value.trim();
                const correct = document.getElementById('correct-option-input').value.trim();

                validateQuestion(options, correct);
                const data = {
                    question: question, 
                    options: options,
                    correct_option_index: Number(correct)
                }
                socket.emit('add_question', data);
                formAddQuestion.reset();
            }
            catch (e) {
                alert(e);
            }
        });
	socket.on('question_added', (data) => {
	    const counter = document.getElementById('question-counter');
	    counter.textContent = data.count;
	});
    }

    chatInputForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const message = chatInput.value.trim();
        if (message) {
            socket.emit('new_message', { username: getUsername(), message: message });
            chatInput.value = '';
        }
    });

    socket.on('connect', () => {
        const username = getUsername();
        socket.emit('join', { username: username });
	socket.emit('chat_history', {message: 'Chat History'});
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
