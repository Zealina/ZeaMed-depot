const socket = io.connect('http://localhost:5000');  // Adjust the URL as needed

// Elements
const questionNumberElement = document.getElementById('question-number');
const timerElement = document.getElementById('timer');
const questionElement = document.getElementById('question');
const optionsContainer = document.getElementById('options-container');
const submitButton = document.getElementById('option-submit');
const optionsForm = document.getElementById('question-option-form');


optionsForm.addEventListener('submit', (e) => {
    try {
        e.preventDefault();
        const  selectedOption = optionsForm.querySelector('input[type=radio][name=option]:checked');
        if (!selectedOption) {
            throw Error('Select an option');
        }
        socket.emit('answered_question', {answer: selectedOption.value});
    } catch (error) {
        alert(error);
    }
})

function addOption(option) {
    const optionField = document.createElement("div");
    optionField.classList.add('option-field');
    
    const radio = document.createElement('input');
    radio.setAttribute('type', 'radio');
    radio.setAttribute('name', 'option');
    radio.setAttribute('value', option);
    radio.setAttribute('id', option);
    
    const label = document.createElement('label');
    label.setAttribute('for', option);

    optionField.appendChild(radio);
    optionField.appendChild(label);

    optionsContainer.appendChild(optionField);
}

function addQuestion(data) {
    questionElement.textContent = data.question;

    optionsContainer.children.forEach((option) => option.remove());

    for (let i = 0; i < data.options.length; i++) {
           addOption(data.options[i]);
    }
    questionNumberElement.textContent = `Question ${data.questionIndex + 1}/${data.totalQuestions}`;
}

let timer;

// Handle receiving a new question
socket.on('next_question', (data) => {
    questionIndex++;
    addQuestion(data);
    const duration = Number(data.duration);
    
    startTimer(duration);  // Reset and start the timer for 30 seconds
});

// Handle game over
socket.on('game_over', (data) => {
    alert(`Game Over! Your scores: ${JSON.stringify(data.scores)}`);
    window.location.href = '/result';  // Redirect to the result page or any other appropriate action
});

// Handle errors
socket.on('error', (data) => {
    alert(data.message);
});

// Handle game start notification for creator
socket.on('game_in_progress', () => {
    alert('Game is in progress');
});

// Display options
function displayOptions(options) {
    optionsContainer.innerHTML = '';
    options.forEach((option, index) => {
        const optionButton = document.createElement('button');
        optionButton.classList.add('option-button');
        optionButton.textContent = option;
        optionButton.onclick = () => submitAnswer(option);
        optionsContainer.appendChild(optionButton);
    });
}

// Submit answer
function submitAnswer(answer) {
    socket.emit('answer_question', { answer: answer });
}

// Function to start and display the timer
function startTimer(seconds) {
    clearInterval(timer);
    let timeLeft = seconds;
    timerElement.textContent = `Time Left: ${timeLeft}s`;

    timer = setInterval(() => {
        timeLeft--;
        timerElement.textContent = `Time Left: ${timeLeft}s`;
        if (timeLeft <= 0) {
            clearInterval(timer);
        }
    }, 1000);
}

// Initialize game start
socket.emit('start_game');