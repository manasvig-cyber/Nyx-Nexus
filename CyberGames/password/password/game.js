// Game variables
let currentScenario = null;
let attempts = 5;
let timerInterval = null;
let secondsElapsed = 0;
let hintsUnlocked = 0;
let isGameActive = false;

// DOM Elements
const screens = {
    splash: document.getElementById('splash-screen'),
    game: document.getElementById('game-screen'),
    end: document.getElementById('end-screen')
};

const ui = {
    timer: document.getElementById('timer'),
    attempts: document.getElementById('attempts'),
    caseTitle: document.getElementById('case-title'),
    caseParagraph: document.getElementById('case-paragraph'),
    caseLink: document.getElementById('case-link'),
    hintStatuses: [
        document.getElementById('hint-1-status'),
        document.getElementById('hint-2-status'),
        document.getElementById('hint-3-status')
    ],
    hintDisplay: document.getElementById('hint-display'),
    passwordInput: document.getElementById('password-input'),
    feedbackMessage: document.getElementById('feedback-message'),
    endTitle: document.getElementById('end-title'),
    endTime: document.getElementById('end-time'),
    finalTime: document.getElementById('final-time')
};

// Start Button
document.getElementById('start-btn').addEventListener('click', startGame);
document.getElementById('restart-btn').addEventListener('click', backToSplash);

function showScreen(screenName) {
    Object.values(screens).forEach(screen => screen.classList.add('hidden'));
    screens[screenName].classList.remove('hidden');
}

function formatTime(totalSeconds) {
    const m = Math.floor(totalSeconds / 60).toString().padStart(2, '0');
    const s = (totalSeconds % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
}

function updateTimer() {
    secondsElapsed++;
    ui.timer.textContent = formatTime(secondsElapsed);
}

function startTimer() {
    clearInterval(timerInterval);
    secondsElapsed = 0;
    ui.timer.textContent = "00:00";
    timerInterval = setInterval(updateTimer, 1000);
}

function stopTimer() {
    clearInterval(timerInterval);
}

let displayedHints = [];
let hintLocked = [true, true, true];

function loadScenario() {
    // Random scenario selection
    const randomIndex = Math.floor(Math.random() * scenarios.length);
    currentScenario = scenarios[randomIndex];
    
    ui.caseTitle.textContent = currentScenario.title;
    ui.caseParagraph.textContent = currentScenario.paragraph;
    ui.caseLink.href = currentScenario.link;
    
    // Reset hints
    hintsUnlocked = 0;
    displayedHints = [];
    hintLocked = [true, true, true];
    
    ui.hintDisplay.classList.add('hidden');
    ui.hintDisplay.innerHTML = "";
    
    ui.hintStatuses.forEach((el, index) => {
        el.textContent = `[HINT ${index + 1} 🔒]`;
        el.classList.remove('unlocked');
    });
}

function revealHint() {
    if (hintsUnlocked < 3 && currentScenario) {
        // Unlock the next hint
        const hintIndex = hintsUnlocked;
        hintLocked[hintIndex] = false;
        hintsUnlocked++;
        
        // Add hint to displayed list
        displayedHints.push(`HINT ${hintsUnlocked}: ${currentScenario.hints[hintIndex]}`);
        
        // Update all badges to reflect the current state
        ui.hintStatuses.forEach((el, idx) => {
            if (!hintLocked[idx]) {
                el.textContent = `[HINT ${idx + 1} 🔓]`;
                el.classList.add('unlocked');
            } else {
                el.textContent = `[HINT ${idx + 1} 🔒]`;
                el.classList.remove('unlocked');
            }
        });
        
        // Render all accumulated hints
        ui.hintDisplay.classList.remove('hidden');
        ui.hintDisplay.innerHTML = displayedHints.map(hint => `<div>${hint}</div>`).join('');
    }
}

function showFeedback(message, type) {
    ui.feedbackMessage.textContent = message;
    ui.feedbackMessage.className = ''; // remove existing classes
    ui.feedbackMessage.classList.add(`color-${type}`);
    
    // Clear after some time if it's not a final message
    if (isGameActive && type !== 'success') {
        setTimeout(() => {
            if (ui.feedbackMessage.textContent === message) {
                ui.feedbackMessage.textContent = "";
            }
        }, 3000);
    }
}

function startGame() {
    isGameActive = true;
    attempts = 5;
    ui.attempts.textContent = `Attempts: ${attempts}`;
    ui.passwordInput.value = "";
    ui.feedbackMessage.textContent = "";
    
    loadScenario();
    showScreen('game');
    startTimer();
    ui.passwordInput.focus();
}

function backToSplash() {
    isGameActive = false;
    stopTimer();
    showScreen('splash');
}

function endGame(won) {
    isGameActive = false;
    stopTimer();
    
    ui.endTime.classList.add('hidden');
    
    if (won) {
        ui.endTitle.textContent = "PASSWORD CRACKED!";
        ui.endTitle.style.color = "var(--highlight-color)";
        ui.finalTime.textContent = formatTime(secondsElapsed);
        ui.endTime.classList.remove('hidden');
    } else {
        ui.endTitle.textContent = "MISSION FAILED!";
        ui.endTitle.style.color = "var(--danger-color)";
    }
    
    showScreen('end');
}

// Audio effects
const thunderSound = new Audio('password/thunder.mp3');

function submitPassword() {
    if (!isGameActive) return;
    
    const inputPwd = ui.passwordInput.value.trim();
    if (!inputPwd) return;
    
    ui.passwordInput.value = ""; // Clear input
    
    if (inputPwd.toLowerCase() === currentScenario.password.toLowerCase()) {
        // Play thunder sound
        try {
            thunderSound.currentTime = 0;
            thunderSound.play().catch(e => console.log("Audio play failed:", e));
        } catch (e) {
            console.log("Audio not supported or file not found.");
        }
        
        showFeedback("PASSWORD CRACKED!", "success");
        setTimeout(() => endGame(true), 1500);
    } else {
        attempts--;
        ui.attempts.textContent = `Attempts: ${attempts}`;
        
        if (attempts > 0) {
            showFeedback(`ACCESS DENIED! ${attempts} attempts remaining.`, "danger");
        } else {
            showFeedback("ACCESS DENIED!", "danger");
            setTimeout(() => endGame(false), 1500);
        }
    }
}

// Keyboard controls
document.addEventListener('keydown', (e) => {
    // Only handle if game is active
    if (!isGameActive) return;

    // CTRL + H for hint
    // Wait, e.key doesn't play well with e.ctrlKey always. e.key could be 'h' or 'H'
    if (e.ctrlKey && e.key.toLowerCase() === 'h') {
        e.preventDefault();
        revealHint();
    }
    
    // BACKSPACE to delete characters
    // (This is naturally handled by the input field, but we can prevent default if needed. Standard input handles it)
    
    // ENTER to submit
    if (e.key === 'Enter') {
        submitPassword();
    }

    // ESC to exit mission
    if (e.key === 'Escape') {
        backToSplash();
    }
});

// Always focus input on game screen click
ui.passwordInput.addEventListener('blur', () => {
    if (isGameActive) {
        // Little timeout to allow clicks on links
        setTimeout(() => {
            if (isGameActive && document.activeElement !== ui.caseLink) {
                 ui.passwordInput.focus();
            }
        }, 10);
    }
});
document.addEventListener('click', (e) => {
    if (isGameActive && e.target !== ui.caseLink) {
        ui.passwordInput.focus();
    }
});
