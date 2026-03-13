document.addEventListener('DOMContentLoaded', () => {
    if (!document.getElementById('global-notification-container')) {
        const container = document.createElement('div');
        container.id = 'global-notification-container';
        document.body.appendChild(container);
    }
});

let activeNotifications = [];

window.showNotification = function (title, message, type) {
    const container = document.getElementById('global-notification-container');
    if (!container) return;

    if (activeNotifications.length >= 3) {
        const oldest = activeNotifications.shift();
        if (oldest && oldest.parentNode) {
            oldest.classList.remove('show');
            oldest.classList.add('hide');
            setTimeout(() => {
                if (oldest.parentNode) oldest.parentNode.removeChild(oldest);
            }, 400);
        }
    }

    const notif = document.createElement('div');
    notif.className = `cyber-notification notification-${type}`;

    let iconClass = 'fas fa-info-circle';
    if (type === 'xp') iconClass = 'fas fa-bolt';
    else if (type === 'badge') iconClass = 'fas fa-trophy';
    else if (type === 'level') iconClass = 'fas fa-crown';
    else if (type === 'room') iconClass = 'fas fa-shield-check';

    notif.innerHTML = `
        <div class="notif-icon">
            <i class="${iconClass}"></i>
        </div>
        <div class="notif-content">
            <div class="notif-title">${title}</div>
            <div class="notif-message">${message}</div>
        </div>
    `;

    container.appendChild(notif);
    activeNotifications.push(notif);

    requestAnimationFrame(() => {
        requestAnimationFrame(() => {
            notif.classList.add('show');
            if (type === 'badge') {
                createNotifSparks(notif);
                playSound('badge');
            } else if (type === 'xp') {
                playSound('xp');
            } else if (type === 'level') {
                playSound('level');
            } else {
                playSound('xp');
            }
        });
    });

    setTimeout(() => {
        if (activeNotifications.includes(notif)) {
            activeNotifications = activeNotifications.filter(n => n !== notif);
            notif.classList.remove('show');
            notif.classList.add('hide');
            setTimeout(() => {
                if (notif.parentNode) notif.parentNode.removeChild(notif);
            }, 400);
        }
    }, 4000);
};

function playSound(type) {
    try {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        if (!AudioContext) return;
        const ctx = new AudioContext();
        if (ctx.state === 'suspended') return;

        const osc = ctx.createOscillator();
        const gainNode = ctx.createGain();
        osc.connect(gainNode);
        gainNode.connect(ctx.destination);

        if (type === 'xp') {
            osc.type = 'sine';
            osc.frequency.setValueAtTime(800, ctx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(1200, ctx.currentTime + 0.1);
            gainNode.gain.setValueAtTime(0.05, ctx.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.3);
            osc.start();
            osc.stop(ctx.currentTime + 0.3);
        } else if (type === 'badge') {
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(600, ctx.currentTime);
            osc.frequency.setValueAtTime(800, ctx.currentTime + 0.1);
            osc.frequency.setValueAtTime(1200, ctx.currentTime + 0.2);
            gainNode.gain.setValueAtTime(0.05, ctx.currentTime);
            gainNode.gain.linearRampToValueAtTime(0, ctx.currentTime + 0.5);
            osc.start();
            osc.stop(ctx.currentTime + 0.5);
        } else if (type === 'level') {
            osc.type = 'square';
            osc.frequency.setValueAtTime(400, ctx.currentTime);
            osc.frequency.setValueAtTime(600, ctx.currentTime + 0.2);
            gainNode.gain.setValueAtTime(0.03, ctx.currentTime);
            gainNode.gain.linearRampToValueAtTime(0, ctx.currentTime + 0.8);
            osc.start();
            osc.stop(ctx.currentTime + 0.8);
        }
    } catch (e) { }
}

function createNotifSparks(element) {
    const rect = element.getBoundingClientRect();
    for (let i = 0; i < 8; i++) {
        const spark = document.createElement('div');
        spark.style.position = 'fixed';
        spark.style.top = (rect.top + rect.height / 2) + 'px';
        spark.style.left = (rect.left + rect.width / 2 - 100) + 'px';
        spark.style.width = '4px';
        spark.style.height = '4px';
        spark.style.background = '#ffd700';
        spark.style.borderRadius = '50%';
        spark.style.boxShadow = '0 0 6px #ffd700';
        spark.style.zIndex = '100001';
        spark.style.pointerEvents = 'none';
        spark.style.transition = 'all 0.6s cubic-bezier(0.1, 0.8, 0.3, 1)';
        document.body.appendChild(spark);

        const angle = Math.random() * Math.PI * 2;
        const dist = 30 + Math.random() * 40;

        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                spark.style.transform = `translate(${Math.cos(angle) * dist}px, ${Math.sin(angle) * dist}px) scale(0)`;
                spark.style.opacity = '0';
            });
        });

        setTimeout(() => { if (spark.parentNode) spark.parentNode.removeChild(spark); }, 600);
    }
}
