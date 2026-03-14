// Initialize Lucide Icons
lucide.createIcons();

document.addEventListener('DOMContentLoaded', () => {

    // Add interactivity to Like button
    const likeButton = document.querySelector('.btn-secondary[data-tooltip="Like"]');
    if (likeButton) {
        likeButton.addEventListener('click', function () {
            const icon = this.querySelector('i');
            this.classList.toggle('liked');

            if (this.classList.contains('liked')) {
                icon.classList.add('fill-icon');
                this.style.color = 'var(--primary)';
                this.style.borderColor = 'var(--primary)';
                this.setAttribute('data-tooltip', 'Unlike');

                // Add pop animation effect
                this.style.transform = 'scale(1.2)';
                setTimeout(() => {
                    this.style.transform = 'scale(1)';
                }, 150);
            } else {
                icon.classList.remove('fill-icon');
                this.style.color = 'white';
                this.style.borderColor = 'rgba(255, 255, 255, 0.2)';
                this.setAttribute('data-tooltip', 'Like');
            }
        });
    }

    // Add interactivity to Add to List button
    const addButton = document.querySelector('.btn-secondary[data-tooltip="Add to List"]');
    if (addButton) {
        addButton.addEventListener('click', function () {
            const icon = this.querySelector('i');

            if (icon.getAttribute('data-lucide') === 'plus') {
                icon.setAttribute('data-lucide', 'check');
                this.setAttribute('data-tooltip', 'Remove from List');
                this.style.color = 'var(--success)';
                this.style.borderColor = 'var(--success)';
            } else {
                icon.setAttribute('data-lucide', 'plus');
                this.setAttribute('data-tooltip', 'Add to List');
                this.style.color = 'white';
                this.style.borderColor = 'rgba(255, 255, 255, 0.2)';
            }

            // Re-render the icon since we changed its type
            lucide.createIcons();

            // Add pop animation effect
            this.style.transform = 'scale(1.2)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    }

    // Mission Card Click animations
    const missionCards = document.querySelectorAll('.mission-card');
    missionCards.forEach(card => {
        card.addEventListener('click', function () {
            // Ripple effect or launching animation
            const title = this.querySelector('.mission-title').textContent;

            // Create a launch message
            const loaderDiv = document.createElement('div');
            loaderDiv.style.position = 'fixed';
            loaderDiv.style.inset = 0;
            loaderDiv.style.backgroundColor = 'rgba(10, 10, 15, 0.9)';
            loaderDiv.style.zIndex = 9999;
            loaderDiv.style.display = 'flex';
            loaderDiv.style.flexDirection = 'column';
            loaderDiv.style.alignItems = 'center';
            loaderDiv.style.justifyContent = 'center';
            loaderDiv.style.color = 'var(--primary)';
            loaderDiv.style.fontFamily = 'var(--font-heading)';
            loaderDiv.style.transition = 'opacity 0.3s ease';

            loaderDiv.innerHTML = `
                <div style="font-size: 2rem; margin-bottom: 2rem; letter-spacing: 2px;">INITIALIZING SECURE CONNECTION...</div>
                <div style="font-size: 1.2rem; color: #fff;">Mission: <span style="color: var(--secondary)">${title}</span></div>
                <div style="width: 300px; height: 4px; background: #333; margin-top: 2rem; border-radius: 2px; overflow: hidden; position: relative;">
                    <div style="position: absolute; left: 0; top: 0; height: 100%; width: 0%; background: var(--primary); animation: loadBar 1.5s ease-in-out forwards; box-shadow: 0 0 10px var(--primary);"></div>
                </div>
                <style>
                    @keyframes loadBar {
                        0% { width: 0; }
                        50% { width: 70%; }
                        100% { width: 100%; }
                    }
                </style>
            `;

            document.body.appendChild(loaderDiv);

            // Remove after animation (mocking a page load)
            setTimeout(() => {
                loaderDiv.style.opacity = '0';
                setTimeout(() => {
                    loaderDiv.remove();
                    if (title === "The Midnight Invoice") {
                        window.location.href="../../../pages/CyberGame/CyberGame/investigation.html?ep=1";
                    } else if (title === "The Silent Insider" || title === "Insider Data Leak") {
                        window.location.href="../../../pages/CyberGame/CyberGame/investigation.html?ep=2";
                    }
                }, 300);
            }, 1800);
        });
    });

    // Main Play Button
    const playBtn = document.querySelector('.btn-primary');
    if (playBtn) {
        playBtn.addEventListener('click', function () {
            // Simulate playing the first mission
            missionCards[0].click();
        });
    }
});
