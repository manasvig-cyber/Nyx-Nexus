export class ShootingStar {
    constructor(canvas, ctx) {
        this.canvas = canvas;
        this.ctx = ctx;
        this.reset();
    }

    reset() {
        this.length = Math.random() * 150 + 50; // Tail length 50 to 200
        this.speed = Math.random() * 10 + 8; // Speed 8 to 18
        this.opacity = Math.random() * 0.4 + 0.6; // Brightness 0.6 to 1.0

        // Start either from top or left to move diagonally
        if (Math.random() > 0.5) {
            // start at top edge
            this.x = Math.random() * this.canvas.width;
            this.y = -this.length;
        } else {
            // start at left edge
            this.x = -this.length;
            this.y = Math.random() * this.canvas.height;
        }
    }

    update() {
        // Move diagonally down-right (angle is PI/4, so dx = dy)
        this.x += this.speed;
        this.y += this.speed;

        // Reset if moved off the bottom or right edge of the screen
        if (this.x > this.canvas.width + this.length || this.y > this.canvas.height + this.length) {
            this.reset();
            // Stagger respawns by positioning them further back
            if (Math.random() > 0.5) {
                this.y = -this.length - Math.random() * 500;
            } else {
                this.x = -this.length - Math.random() * 500;
            }
        }
    }

    draw() {
        this.ctx.beginPath();
        // Head of the star
        this.ctx.moveTo(this.x, this.y);
        // Tail of the star
        this.ctx.lineTo(this.x - this.length, this.y - this.length);

        // Gradient for a fading trail
        const gradient = this.ctx.createLinearGradient(
            this.x, this.y,
            this.x - this.length, this.y - this.length
        );
        gradient.addColorStop(0, `rgba(0, 255, 127, ${this.opacity})`); // Neon green #00ff7f
        gradient.addColorStop(1, `rgba(0, 255, 127, 0)`);

        this.ctx.strokeStyle = gradient;
        this.ctx.lineWidth = 3;
        this.ctx.stroke();

        // Glowing dot at the head (the star meteor itself)
        this.ctx.beginPath();
        this.ctx.arc(this.x, this.y, 1.5, 0, Math.PI * 2);
        this.ctx.fillStyle = `rgba(0, 255, 127, ${this.opacity})`;
        this.ctx.fill();

        // Add glow effect using shadow
        this.ctx.shadowBlur = 15;
        this.ctx.shadowColor = '#00ff7f';
    }
}

export function initStars() {
    const canvas = document.getElementById('cyberStarsCanvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    // Initial size
    resize();
    window.addEventListener('resize', resize);

    const stars = [];
    const numStars = 40; // Number of concurrent shooting stars

    for (let i = 0; i < numStars; i++) {
        const star = new ShootingStar(canvas, ctx);
        // Randomize initial positions all over the screen to prevent clumping
        star.x = Math.random() * canvas.width;
        star.y = Math.random() * canvas.height;
        stars.push(star);
    }

    function animate() {
        // Clear canvas with transparency for the next frame
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        stars.forEach(star => {
            ctx.save();
            star.update();
            star.draw();
            ctx.restore(); // Ensure we don't leak shadow state to clearRect
        });

        requestAnimationFrame(animate);
    }

    // Start animation loop
    animate();
}
