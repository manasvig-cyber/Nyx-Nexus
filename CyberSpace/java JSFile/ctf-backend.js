// CTF Backend Persistence logic
// Requirements:
// 1. On page load, get solved challenges from backend and set UI to MISSION COMPLETED.
// 2. On solving, intercept checkFlag (which calls updateProgress and updateTerminal) to send to backend.

document.addEventListener('DOMContentLoaded', () => {
    // 1. Fetch solved challenges for user_id = 1
    fetch('http://127.0.0.1:8000/api/ctf/progress?user_id=1')
        .then(res => res.json())
        .then(data => {
            if (data && data.solved) {
                data.solved.forEach(chalId => {
                    // Force the challenge to be solved in local UI state
                    completed.add(chalId);

                    const card = document.getElementById(`card${chalId}`);
                    const input = document.getElementById(`flagInput${chalId}`);
                    const scan = document.getElementById(`scan${chalId}`);
                    
                    if (card) {
                        card.classList.add('completed', 'success-glow');
                    }
                    if (input) {
                        input.disabled = true;
                        if (input.nextElementSibling) {
                            input.nextElementSibling.style.display = 'none';
                        }
                    }
                    if (scan) {
                        scan.classList.remove('active');
                    }
                });
                
                // Refresh progress visually
                if (typeof updateProgress === 'function') {
                    updateProgress();
                }
            }
        })
        .catch(err => console.error("Could not fetch CTF progress", err));

    // Wait slightly to ensure global checkFlag is defined, then hook into it
    setTimeout(() => {
        if (typeof window.checkFlag === 'function') {
            const originalCheckFlag = window.checkFlag;
            window.checkFlag = function(id, correct) {
                // Determine if it wasn't already solved
                const alreadySolved = completed.has(id);
                
                // Let the original logic validate the flag and show success/fail
                originalCheckFlag(id, correct);

                // Wait for original checkFlag's setTimeout (which is 1000ms) to resolve
                setTimeout(() => {
                    // Only send if it was just solved
                    if (!alreadySolved && completed.has(id)) {
                        fetch('http://127.0.0.1:8000/api/ctf/submit', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                user_id: 1,
                                challenge_id: id
                            })
                        }).catch(err => console.error("Failed to submit CTF challenge", err));
                    }
                }, 1100);
            };
        }
    }, 100);
});
