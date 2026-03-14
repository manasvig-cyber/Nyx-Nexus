export default class TimerController {
    constructor(durationMinutes, displayElementId, onTimeoutCallback) {
        this.totalTime = durationMinutes * 60;
        this.timeRemaining = this.totalTime;
        this.displayElement = document.getElementById(displayElementId);
        this.onTimeout = onTimeoutCallback;
        this.interval = null;
    }

    start() {
        if (this.interval) return;
        this.updateDisplay();
        this.interval = setInterval(() => {
            if (this.timeRemaining > 0) {
                this.timeRemaining--;
                this.updateDisplay();

                // Near timeout warning
                if (this.timeRemaining === 300) { // 5 mins left
                    this.displayElement.style.color = 'var(--secondary)';
                    this.displayElement.style.borderColor = 'var(--secondary)';
                    this.displayElement.style.boxShadow = '0 0 10px rgba(255,0,60,0.5)';
                }
            } else {
                this.stop();
                if (this.onTimeout) this.onTimeout();
            }
        }, 1000);
    }

    stop() {
        if (this.interval) {
            clearInterval(this.interval);
            this.interval = null;
        }
    }

    getTimeRemaining() {
        return this.timeRemaining;
    }

    getTimeUsed() {
        return this.totalTime - this.timeRemaining;
    }

    updateDisplay() {
        if (!this.displayElement) return;
        const m = Math.floor(this.timeRemaining / 60).toString().padStart(2, '0');
        const s = (this.timeRemaining % 60).toString().padStart(2, '0');
        this.displayElement.textContent = `00:${m}:${s}`;
    }
}
