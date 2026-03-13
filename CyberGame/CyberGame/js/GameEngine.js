import TimerController from './TimerController.js';
import EpisodeManager from './EpisodeManager.js';
import ScoreSystem from './ScoreSystem.js';

export default class GameEngine {
    constructor(episodeId) {
        this.episodeManager = new EpisodeManager(episodeId);
        this.scoreSystem = new ScoreSystem();
        this.timerController = new TimerController(
            this.episodeManager.getDuration(),
            'timer-display',
            () => this.handleTimeout()
        );

        this.gameState = 'BRIEFING'; // BRIEFING, EVIDENCE_ANALYSIS, EVALUATION, RESULT
        this.droppedEvidenceIds = new Set();

        this.populateEpisodeData();
        this.initDOMConnections();
        this.startGame();
    }

    populateEpisodeData() {
        const config = this.episodeManager.episodeConfig;

        // Update Title
        document.querySelector('.inv-title h2').textContent = `Episode ${config.id}: ${config.title}`;

        // Populate Evidence Logs
        const evidenceList = document.querySelector('.evidence-list');
        evidenceList.innerHTML = '';
        if (config.id === "1") {
            evidenceList.innerHTML = `
                <div class="evidence-card" draggable="true" data-type="email" data-evidence="fake_invoice">
                    <div class="evidence-icon"><i data-lucide="mail"></i></div>
                    <div class="evidence-content">
                        <h4>Email Logs</h4>
                        <p><strong>Sender:</strong> billing@micr0soft-support.com</p>
                        <p><strong>Subject:</strong> Urgent Invoice Payment Required</p>
                        <p><strong>Attachment:</strong> <span class="highlight-danger">invoice_update.pdf.exe</span></p>
                    </div>
                </div>
                <div class="evidence-card" draggable="true" data-type="login" data-evidence="foreign_ip">
                    <div class="evidence-icon"><i data-lucide="log-in"></i></div>
                    <div class="evidence-content">
                        <h4>Login Logs</h4>
                        <p><span class="highlight-warning">3:02 AM</span> login from foreign IP</p>
                        <p>Multiple failed login attempts</p>
                    </div>
                </div>
                <div class="evidence-card" draggable="true" data-type="network" data-evidence="tor_exit">
                    <div class="evidence-icon"><i data-lucide="activity"></i></div>
                    <div class="evidence-content">
                        <h4>Network Logs</h4>
                        <p>Encrypted outbound traffic</p>
                        <p>Connection to <span class="highlight-danger">TOR exit node</span></p>
                    </div>
                </div>
            `;
        } else if (config.id === "2") {
            evidenceList.innerHTML = `
                <div class="evidence-card" draggable="true" data-type="login" data-evidence="activity_logs">
                    <div class="evidence-icon"><i data-lucide="user-check"></i></div>
                    <div class="evidence-content">
                        <h4>Activity Logs</h4>
                        <p>User accessed patient database after office hours.</p>
                        <p>Multiple late-night logins detected.</p>
                        <p><span class="highlight-warning">Repeated USB device insertions</span> on workstation.</p>
                    </div>
                </div>
                <div class="evidence-card" draggable="true" data-type="network" data-evidence="file_access">
                    <div class="evidence-icon"><i data-lucide="file-search"></i></div>
                    <div class="evidence-content">
                        <h4>File Access Logs</h4>
                        <p>Large number of files copied from patient directory.</p>
                        <p>Access to <span class="highlight-danger">restricted medical folders</span>.</p>
                    </div>
                </div>
                <div class="evidence-card" draggable="true" data-type="email" data-evidence="network_logs">
                    <div class="evidence-icon"><i data-lucide="activity"></i></div>
                    <div class="evidence-content">
                        <h4>Network Logs</h4>
                        <p>Outbound traffic to cloud service.</p>
                        <p>Uploads to <span class="highlight-danger">personal Dropbox</span>.</p>
                    </div>
                </div>
            `;
        }

        // Populate Suspects
        const suspectsList = document.querySelector('.suspects-list');
        suspectsList.innerHTML = '';
        config.suspects.forEach(suspect => {
            const label = config.labels ? config.labels[suspect] : (suspect.charAt(0).toUpperCase() + suspect.slice(1));

            suspectsList.innerHTML += `
                <div class="suspect-card" data-suspect="${suspect}">
                    <div class="suspect-profile">
                        <div class="avatar"><i data-lucide="user"></i></div>
                        <div class="suspect-info">
                            <h4>${label}</h4>
                            <span>Unknown ID</span>
                        </div>
                    </div>
                    <div class="meter-container">
                        <div class="meter-label">Suspicion Level</div>
                        <div class="meter-bar">
                            <div class="meter-fill" style="width: 0%;" id="meter-${suspect}"></div>
                        </div>
                    </div>
                </div>
            `;
        });

        // Update Compromised Account Select Options
        const compromisedSelect = document.getElementById('compromised-account');
        compromisedSelect.innerHTML = '<option value="">-- Select Account --</option>';
        config.suspects.forEach(suspect => {
            const label = config.labels ? config.labels[suspect] : (suspect.charAt(0).toUpperCase() + suspect.slice(1));
            compromisedSelect.innerHTML += `<option value="${suspect}">${label}</option>`;
        });

        // Initialize Options Dynamically
        if (config.attackTypes) {
            const attackTypeSelect = document.getElementById('attack-type');
            attackTypeSelect.innerHTML = '<option value="">-- Select Attack Type --</option>';
            config.attackTypes.forEach(type => {
                attackTypeSelect.innerHTML += `<option value="${type.id}">${type.label}</option>`;
            });
        }

        const entryPointSelect = document.getElementById('entry-point');
        const entryPointGroup = entryPointSelect.closest('.action-group');
        if (config.entryPoints && config.entryPoints.length > 0) {
            entryPointGroup.style.display = 'block';
            entryPointSelect.innerHTML = '<option value="">-- Select Entry Point --</option>';
            config.entryPoints.forEach(ep => {
                entryPointSelect.innerHTML += `<option value="${ep.id}">${ep.label}</option>`;
            });
        } else {
            entryPointGroup.style.display = 'none';
        }

        if (config.containmentActions) {
            const containmentGrid = document.querySelector('.checkbox-grid');
            containmentGrid.innerHTML = '';
            config.containmentActions.forEach(action => {
                containmentGrid.innerHTML += `
                    <label class="cyber-checkbox">
                        <input type="checkbox" id="action-${action.id}" value="${action.id}"> ${action.label}
                    </label>
                `;
            });
        }

        if (window.lucide) {
            window.lucide.createIcons();
        }
    }

    initDOMConnections() {
        // Drag and Drop
        const evidenceCards = document.querySelectorAll('.evidence-card');
        const dropzone = document.getElementById('dropzone');
        const boardGrid = document.querySelector('.board-grid');

        evidenceCards.forEach(card => {
            card.addEventListener('dragstart', (e) => {
                e.dataTransfer.setData('text/plain', card.dataset.evidence);
                e.dataTransfer.setData('html', card.innerHTML);
                card.style.opacity = '0.5';
            });
            card.addEventListener('dragend', (e) => {
                card.style.opacity = '1';
            });
        });

        dropzone.addEventListener('dragover', (e) => {
            e.preventDefault();
            document.querySelector('.drop-target-area').classList.add('drag-over');
        });

        dropzone.addEventListener('dragleave', (e) => {
            document.querySelector('.drop-target-area').classList.remove('drag-over');
        });

        dropzone.addEventListener('drop', (e) => {
            e.preventDefault();
            document.querySelector('.drop-target-area').classList.remove('drag-over');

            const evidenceId = e.dataTransfer.getData('text/plain');
            const htmlContent = e.dataTransfer.getData('html');

            if (this.droppedEvidenceIds.has(evidenceId)) return;
            this.droppedEvidenceIds.add(evidenceId);

            // Add to grid
            const newEl = document.createElement('div');
            newEl.className = 'dropped-evidence';
            newEl.setAttribute('data-id', evidenceId);
            newEl.innerHTML = htmlContent;
            newEl.style.width = '240px';
            newEl.style.display = 'flex';
            newEl.style.flexDirection = 'column';
            newEl.style.gap = '0.5rem';

            // Add a glowing effect
            newEl.style.boxShadow = '0 0 20px var(--success)';
            setTimeout(() => newEl.style.boxShadow = '', 2000); // fade out glow

            boardGrid.appendChild(newEl);
            this.showNotification(`New evidence analyzed: ${evidenceId.replace('_', ' ')}`);

            // Update Logic
            const updatedMeters = this.episodeManager.updateSuspicion(evidenceId);
            this.updateMeterUI(updatedMeters);

            // State change
            if (this.gameState === 'BRIEFING') {
                this.gameState = 'EVIDENCE_ANALYSIS';
            }
        });

        // Submit Button
        document.getElementById('submit-investigation').addEventListener('click', () => {
            this.submitInvestigation();
        });

        // Fullscreen Toggle
        const fsToggle = document.getElementById('fullscreen-toggle');
        if (fsToggle) {
            fsToggle.addEventListener('click', () => {
                if (!document.fullscreenElement) {
                    document.documentElement.requestFullscreen().catch(err => console.log(err));
                    fsToggle.querySelector('i').setAttribute('data-lucide', 'minimize');
                } else {
                    document.exitFullscreen();
                    fsToggle.querySelector('i').setAttribute('data-lucide', 'maximize');
                }
                lucide.createIcons();
            });
        }

        document.getElementById('close-modal').addEventListener('click', () => {
            // Mock API call to save score
            console.log("Saving score to backend API...");
            window.location.href = 'index.html';
        });
    }

    startGame() {
        this.showNotification("System Initialized. Investigation started.");
        this.timerController.start();
    }

    handleTimeout() {
        this.gameState = 'RESULT';
        const config = this.episodeManager.episodeConfig;
        const failureText = config.failureMessage || `The threat actor has escalated privileges and encrypted the network before you could stop them.`;
        this.showModal('failure', 'TIME EXPIRED', `<p style="color:var(--secondary)">> OUTCOME: CRITICAL FAILURE</p><br><p>${failureText}</p>`);
    }

    updateMeterUI(meters) {
        for (let suspect in meters) {
            let meterId = `meter-${suspect}`;
            let el = document.getElementById(meterId);
            if (el) {
                el.style.width = meters[suspect] + '%';
            }
            // Add highlight classes if highly suspicious
            if (meters[suspect] > 75) {
                let card = document.querySelector(`.suspect-card[data-suspect="${suspect}"]`);
                if (card && !card.classList.contains('suspect-high')) {
                    card.classList.add('suspect-high');
                    this.showNotification(`Warning: ${suspect.toUpperCase()} showing high suspicion!`);
                }
            }
        }
    }

    submitInvestigation() {
        this.gameState = 'EVALUATION';
        const config = this.episodeManager.episodeConfig;

        const playerSubmission = {
            attackType: document.getElementById('attack-type').value,
            entryPoint: document.getElementById('entry-point').value,
            compromisedAccount: document.getElementById('compromised-account').value,
            containment: []
        };

        const checkboxes = document.querySelectorAll('.checkbox-grid input[type="checkbox"]:checked');
        checkboxes.forEach(cb => {
            playerSubmission.containment.push(cb.value);
        });

        const needsEntryPoint = config.entryPoints && config.entryPoints.length > 0;
        if (!needsEntryPoint) {
            playerSubmission.entryPoint = "none"; // Match default when not needed
        }

        if (!playerSubmission.attackType || (needsEntryPoint && !playerSubmission.entryPoint) || !playerSubmission.compromisedAccount) {
            this.showNotification("SYSTEM WARNING: Please complete the investigation form before submitting.", "error");
            this.gameState = 'EVIDENCE_ANALYSIS';
            return;
        }

        this.timerController.stop();
        const timeRemaining = this.timerController.getTimeRemaining();
        const correctSolution = this.episodeManager.getSolution();

        const result = this.scoreSystem.evaluate(playerSubmission, correctSolution, timeRemaining);

        this.gameState = 'RESULT';
        this.displayResult(result);
    }

    displayResult(result) {
        const config = this.episodeManager.episodeConfig;

        if (result.isSuccess) {
            const successText = config.successMessage || `<p>Excellent work, Detective.</p><p>You successfully neutralized the threat.</p>`;
            let html = `
                <p style="color:var(--success)">> OUTCOME: SUCCESS</p>
                <br>
                <p>${successText}</p>
                <br>
                <p>Final Score: <strong>${Math.floor(result.score)} / 100</strong></p>
                <p>Assigned Rank: <strong>${result.rank}</strong></p>
            `;
            this.showModal('success', '<i data-lucide="shield-check" class="icon-small"></i> Threat Neutralized', html);
        } else {
            const failureText = config.failureMessage || `<p>The threat actor has escalated privileges and encrypted the network before you could stop them.</p>`;
            let html = `<p style="color:var(--secondary)">> OUTCOME: CRITICAL FAILURE</p><br>`;
            html += `<p>${failureText}</p><br>`;
            result.feedback.forEach(f => {
                html += `<p>${f}</p>`;
            });
            html += `<br><p>Final Score: <strong>${Math.floor(result.score)} / 100</strong></p>`;

            this.showModal('failure', '<i data-lucide="alert-triangle" class="icon-small"></i> Investigation Failed', html);
        }
    }

    showModal(type, titleHtml, contentHtml) {
        const modal = document.getElementById('result-modal');
        const mContent = document.querySelector('.modal-content');
        const rTitle = document.getElementById('result-title');
        const rText = document.getElementById('result-text');

        modal.classList.remove('hidden');
        mContent.className = `modal-content ${type}`;
        rTitle.innerHTML = titleHtml;
        rText.innerHTML = contentHtml;
        lucide.createIcons();
    }

    showNotification(message, type = "info") {
        // Find or create notification container
        let container = document.getElementById('notification-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'notification-container';
            container.style.position = 'fixed';
            container.style.bottom = '20px';
            container.style.right = '20px';
            container.style.display = 'flex';
            container.style.flexDirection = 'column';
            container.style.gap = '10px';
            container.style.zIndex = '9999';
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        toast.style.background = type === 'error' ? 'rgba(255,0,60,0.9)' : 'rgba(0,240,255,0.9)';
        toast.style.color = type === 'error' ? '#fff' : '#000';
        toast.style.padding = '10px 20px';
        toast.style.borderRadius = '4px';
        toast.style.fontFamily = 'monospace';
        toast.style.boxShadow = `0 0 10px ${toast.style.background}`;
        toast.style.animation = 'popIn 0.3s ease-out forwards';
        toast.style.opacity = '0';

        toast.innerText = message;
        container.appendChild(toast);

        // Fade in
        setTimeout(() => toast.style.opacity = '1', 10);

        // Remove after 3s
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transition = 'opacity 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
}
