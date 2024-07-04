const socket = io.connect('http://localhost:5000');  // Adjust the URL as needed

// Elements
const questionNumberElement = document.getElementById('question-number');
const timerElement = document.getElementById('timer');
const questionElement = document.getElementById('question');
const optionsContainer = document.getElementById('options-container');

// Global variables
let questionIndex = 0;
let totalQuestions = 10;  // Set the total number of questions
let timer;

// Handle receiving a new question
socket.on('next_question', (data) => {
    questionIndex++;
    questionNumberElement.textContent = `Question ${questionIndex}/${totalQuestions}`;
    questionElement.textContent = data.question;
    displayOptions(data.options);
    startTimer(30);  // Reset and start the timer for 30 seconds
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
