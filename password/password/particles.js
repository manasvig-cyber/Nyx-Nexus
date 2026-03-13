const canvas = document.getElementById('bg-canvas');
const ctx = canvas.getContext('2d');

let width, height;

function resize() {
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width;
    canvas.height = height;
}

window.addEventListener('resize', resize);
resize();

class Particle {
    constructor() {
        this.reset();
    }

    reset() {
        this.x = Math.random() * width;
        this.y = Math.random() * height;
        this.size = Math.random() * 2 + 1;
        this.speedX = (Math.random() - 0.5) * 0.5;
        this.speedY = (Math.random() - 0.5) * 0.5 - 0.5; // Drift upwards slightly
        this.alpha = Math.random() * 0.5 + 0.1;
    }

    update() {
        this.x += this.speedX;
        this.y += this.speedY;

        if (this.x < 0 || this.x > width || this.y < 0 || this.y > height) {
            this.reset();
        }
    }

    draw() {
        ctx.fillStyle = `rgba(100, 200, 255, ${this.alpha})`;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }
}

const particles = [];
const particleCount = 100;

for (let i = 0; i < particleCount; i++) {
    particles.push(new Particle());
}

// Flash element
const flashDiv = document.createElement('div');
flashDiv.className = 'flash';
document.body.appendChild(flashDiv);

function doLightningFlash() {
    if (Math.random() < 0.005) { // Occasional flash
        flashDiv.style.opacity = Math.random() * 0.5 + 0.1;
        setTimeout(() => {
            flashDiv.style.opacity = 0;
            if (Math.random() < 0.3) {
                // Secondary flash
                setTimeout(() => {
                    flashDiv.style.opacity = Math.random() * 0.3 + 0.1;
                    setTimeout(() => {
                        flashDiv.style.opacity = 0;
                    }, 50);
                }, 100);
            }
        }, 50);
    }
}

function animateParticles() {
    ctx.clearRect(0, 0, width, height);
    
    // Draw particles
    for (let p of particles) {
        p.update();
        p.draw();
    }

    doLightningFlash();

    requestAnimationFrame(animateParticles);
}

animateParticles();
