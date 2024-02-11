const inputs = document.querySelector(".inputs"),
      hintTag = document.querySelector(".hint span"),
      guessLeft = document.querySelector(".guess-left span"),
      wrongLetter = document.querySelector(".wrong-letter span"),
      scoreTag = document.querySelector(".score span"), // Ensure you have this in your HTML
      resetBtn = document.querySelector(".reset-btn"),
      typingInput = document.querySelector(".typing-input");

let word, maxGuesses, incorrectLetters = [], correctLetters = [], guessedWordsCount = 0, score = 0;

function randomWord() {
    // Check if all words have been guessed
    if(guessedWordsCount === wordList.length) {
        alert("Congratulations! You've guessed all the words.");
        // Optionally, disable the input and reset button, or redirect the user, etc.
        typingInput.disabled = true;
        resetBtn.disabled = true;
        return; // Exit the function
    }

    let ranObj = wordList[guessedWordsCount]; // Use the guessedWordsCount to get the next word
    word = ranObj.word;
    maxGuesses = 8; // or any other logic you have for this
    incorrectLetters = [];
    correctLetters = [];

    hintTag.textContent = ranObj.hint;
    guessLeft.textContent = maxGuesses;
    wrongLetter.textContent = incorrectLetters;
    inputs.innerHTML = ""; // Clear previous inputs

    let html = "";
    for (let i = 0; i < word.length; i++) {
        html += `<input type="text" disabled>`;
    }
    inputs.innerHTML = html;

    scoreTag.textContent = score; // Update score display
}

function initGame(e) {
    let key = e.target.value;
    if (key.match(/^[A-Za-z]+$/) && !incorrectLetters.includes(key) && !correctLetters.includes(key)) {
        if (word.includes(key)) {
            correctLetters.push(key);
            // Update the displayed inputs
            updateCorrectLetters(key);
        } else {
            maxGuesses--;
            incorrectLetters.push(key);
        }
        guessLeft.textContent = maxGuesses;
        wrongLetter.textContent = incorrectLetters.join(", ");
    }
    typingInput.value = ""; // Clear input box after each guess

    setTimeout(() => {
        if (correctLetters.length === new Set(word).size) {
            score++; // Increment score for correct word guess
            scoreTag.textContent = score; // Update score display
            guessedWordsCount++; // Increment guessed words count
            alert(`Correct! The word was ${word}. Next word!`);
            randomWord(); // Move to the next word
        } else if (maxGuesses <= 0) {
            alert("Game over! You've run out of guesses.");
            resetBtn.textContent = "Restart";
            resetBtn.addEventListener("click", () => window.location.reload()); // Restart the game
        }
    });
}

function updateCorrectLetters(key) {
    const inputsChildren = inputs.querySelectorAll("input");
    word.split("").forEach((char, index) => {
        if (char === key) {
            inputsChildren[index].value = key;
        }
    });
}

// Event listeners
resetBtn.addEventListener("click", randomWord);
typingInput.addEventListener("input", initGame);
inputs.addEventListener("click", () => typingInput.focus());
document.addEventListener("keydown", () => typingInput.focus());

randomWord(); // Initialize the first word
