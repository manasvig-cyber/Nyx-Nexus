/**
 * CYBER NETWORK BREACH SIMULATOR
 * Advanced Cybersecurity Training Engine
 */

const canvas = document.getElementById('mazeCanvas');
const ctx = canvas.getContext('2d');

const GRID_SIZE = 20;
let CELL_SIZE = 30;

// Game State
let networkGrid = [];
let agent = { x: 0, y: 0, gridX: 0, gridY: 0, tools: [] };
let rootServer = { x: GRID_SIZE - 1, y: GRID_SIZE - 1 };
let breachTimer = 0;
let gameState = 'MENU';
let discovery = []; // Fog of War data
let entities = []; // Challenges and items
let activeChallenge = null;

// Node Types
const NODE_TYPES = {
    FIREWALL: 'firewall',
    THREAT: 'threat',
    PACKET: 'packet',
    LOG: 'log',
    TOOL: 'tool',
    GATE: 'gate'
};

const COLORS = {
    firewall: '#00f2ff',
    route: '#0a0a14',
    agent: '#39ff14',
    rootServer: '#ff1493',
    threat: '#ff1212',
    packet: '#ffb432',
    log: '#ffffff',
    tool: '#39ff14',
    gate: '#ff9614',
    fog: '#000000'
};

class GridNode {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.walls = { top: true, right: true, bottom: true, left: true };
        this.visited = false;
        this.discovered = false;
    }

    draw() {
        if (!this.discovered) {
            this.drawFog();
            return;
        }

        const x = this.x * CELL_SIZE;
        const y = this.y * CELL_SIZE;

        ctx.strokeStyle = COLORS.firewall;
        ctx.lineWidth = 2;
        ctx.shadowBlur = 5;
        ctx.shadowColor = COLORS.firewall;

        if (this.walls.top) { ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + CELL_SIZE, y); ctx.stroke(); }
        if (this.walls.right) { ctx.beginPath(); ctx.moveTo(x + CELL_SIZE, y); ctx.lineTo(x + CELL_SIZE, y + CELL_SIZE); ctx.stroke(); }
        if (this.walls.bottom) { ctx.beginPath(); ctx.moveTo(x + CELL_SIZE, y + CELL_SIZE); ctx.lineTo(x, y + CELL_SIZE); ctx.stroke(); }
        if (this.walls.left) { ctx.beginPath(); ctx.moveTo(x, y + CELL_SIZE); ctx.lineTo(x, y); ctx.stroke(); }

        ctx.shadowBlur = 0;
    }

    drawFog() {
        ctx.fillStyle = COLORS.fog;
        ctx.fillRect(this.x * CELL_SIZE, this.y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
    }
}

function initNetwork() {
    networkGrid = [];
    for (let x = 0; x < GRID_SIZE; x++) {
        networkGrid[x] = [];
        for (let y = 0; y < GRID_SIZE; y++) {
            networkGrid[x][y] = new GridNode(x, y);
        }
    }

    const stack = [];
    let current = networkGrid[0][0];
    current.visited = true;
    stack.push(current);

    while (stack.length > 0) {
        const neighbors = getNeighbors(current);
        if (neighbors.length > 0) {
            const next = neighbors[Math.floor(Math.random() * neighbors.length)];
            removeWalls(current, next.cell, next.dir);
            next.cell.visited = true;
            stack.push(next.cell);
            current = next.cell;
        } else {
            current = stack.pop();
        }
    }

    // Add extra network routes
    for (let i = 0; i < 25; i++) {
        let rx = Math.floor(Math.random() * (GRID_SIZE - 2)) + 1;
        let ry = Math.floor(Math.random() * (GRID_SIZE - 2)) + 1;
        let dirs = ['top', 'right', 'bottom', 'left'];
        removeWalls(networkGrid[rx][ry], null, dirs[Math.floor(Math.random() * 4)]);
    }

    spawnSecurityEntities();
    updateVisibility(0, 0, 2);
}

function getNeighbors(node) {
    const neighbors = [];
    const dirs = [
        { x: 0, y: -1, dir: 'top' }, { x: 1, y: 0, dir: 'right' },
        { x: 0, y: 1, dir: 'bottom' }, { x: -1, y: 0, dir: 'left' }
    ];

    dirs.forEach(d => {
        const nx = node.x + d.x, ny = node.y + d.y;
        if (nx >= 0 && nx < GRID_SIZE && ny >= 0 && ny < GRID_SIZE && !networkGrid[nx][ny].visited) {
            neighbors.push({ cell: networkGrid[nx][ny], dir: d.dir });
        }
    });
    return neighbors;
}

function removeWalls(a, b, dir) {
    a.walls[dir] = false;
    if (b) {
        if (dir === 'top') b.walls.bottom = false;
        if (dir === 'right') b.walls.left = false;
        if (dir === 'bottom') b.walls.top = false;
        if (dir === 'left') b.walls.right = false;
    } else {
        const nx = a.x + (dir === 'right' ? 1 : dir === 'left' ? -1 : 0);
        const ny = a.y + (dir === 'bottom' ? 1 : dir === 'top' ? -1 : 0);
        if (nx >= 0 && nx < GRID_SIZE && ny >= 0 && ny < GRID_SIZE) {
            networkGrid[nx][ny].walls[dir === 'top' ? 'bottom' : dir === 'bottom' ? 'top' : dir === 'left' ? 'right' : 'left'] = false;
        }
    }
}

function spawnSecurityEntities() {
    entities = [];
    const addEntity = (type, count) => {
        for (let i = 0; i < count; i++) {
            let rx = Math.floor(Math.random() * GRID_SIZE), ry = Math.floor(Math.random() * GRID_SIZE);
            if ((rx !== 0 || ry !== 0) && (rx !== GRID_SIZE - 1 || ry !== GRID_SIZE - 1)) {
                entities.push({ x: rx, y: ry, type, id: Math.random() });
            }
        }
    };

    addEntity(NODE_TYPES.THREAT, 6);
    addEntity(NODE_TYPES.PACKET, 4);
    addEntity(NODE_TYPES.LOG, 4);
    addEntity(NODE_TYPES.TOOL, 3);
    addEntity(NODE_TYPES.GATE, 3);
}

function updateVisibility(gx, gy, radius) {
    for (let x = gx - radius; x <= gx + radius; x++) {
        for (let y = gy - radius; y <= gy + radius; y++) {
            if (x >= 0 && x < GRID_SIZE && y >= 0 && y < GRID_SIZE) {
                networkGrid[x][y].discovered = true;
            }
        }
    }
}

window.onkeydown = (e) => {
    if (gameState !== 'PLAYING' || activeChallenge) return;

    if (e.key === 's' || e.key === 'S') {
        runNetworkScan();
        return;
    }

    const { gridX, gridY } = agent;
    let moved = false;

    if (e.key === 'ArrowUp' && !networkGrid[gridX][gridY].walls.top) { agent.gridY--; moved = true; }
    if (e.key === 'ArrowDown' && !networkGrid[gridX][gridY].walls.bottom) { agent.gridY++; moved = true; }
    if (e.key === 'ArrowLeft' && !networkGrid[gridX][gridY].walls.left) { agent.gridX--; moved = true; }
    if (e.key === 'ArrowRight' && !networkGrid[gridX][gridY].walls.right) { agent.gridX++; moved = true; }

    if (moved) {
        updateVisibility(agent.gridX, agent.gridY, 1);
        checkNodeInteractions();
    }
};

function runNetworkScan() {
    const pulse = document.getElementById('scan-pulse');
    pulse.style.left = agent.x + 'px';
    pulse.style.top = agent.y + 'px';
    pulse.classList.remove('hidden');
    setTimeout(() => pulse.classList.add('hidden'), 600);
    updateVisibility(agent.gridX, agent.gridY, 3);
}

const CHALLENGES = {
    threat: [
        { q: "ALERT: Suspicious login detected from internal workstation.", opts: ["BLOCK IP", "ALLOW TRAFFIC"], ans: 0 },
        { q: "ALERT: Port 445 scanning activity detected.", opts: ["ISOLATE SYSTEM", "LOG AND IGNORE"], ans: 0 }
    ],
    packet: [
        { q: "PACKET: 192.168.1.10 -> 8.8.8.8 | Payload: GET /?id=1' OR '1'='1", opts: ["SQL INJECTION", "XSS", "DDOS"], ans: 0 },
        { q: "PACKET: Multiple SYN packets to port 80 with no ACK.", opts: ["SYN FLOOD", "FINGERPRINTING", "BUFFER OVERFLOW"], ans: 0 }
    ],
    log: [
        { q: "LOG: admin failed, admin failed, root success at 03:00AM", opts: ["BRUTE FORCE", "PHISHING", "NORMAL LOGIN"], ans: 0 }
    ],
    gate: [
        { q: "FIREWALL RULE: Incoming Port 22 identified.", opts: ["OPEN PORT", "BLOCK PORT", "INSPECT TRAFFIC"], ans: 1 }
    ],
    boss: [
        { q: "FINAL SECURITY CHECK: Traffic: GET /admin?name=<script>alert(1)</script>", opts: ["SQLi", "XSS", "CSRF"], ans: 1 }
    ]
};

function checkNodeInteractions() {
    // Root Server Check
    if (agent.gridX === rootServer.x && agent.gridY === rootServer.y) {
        triggerChallenge('boss');
        return;
    }

    const entity = entities.find(e => e.x === agent.gridX && e.y === agent.gridY);
    if (entity) {
        if (entity.type === NODE_TYPES.TOOL) {
            agent.tools.push("SEC_TOOL");
            document.getElementById('tools-val').innerText = agent.tools.length + " UNITS";
            entities = entities.filter(e => e.id !== entity.id);
        } else {
            triggerChallenge(entity.type, entity.id);
        }
    }
}

function triggerChallenge(type, id) {
    const cIdx = Math.floor(Math.random() * CHALLENGES[type].length);
    activeChallenge = { ...CHALLENGES[type][cIdx], id, type };

    document.getElementById('challenge-title').innerText = type.toUpperCase() + " DETECTED";
    document.getElementById('challenge-body').innerText = activeChallenge.q;
    const optsDiv = document.getElementById('challenge-options');
    optsDiv.innerHTML = '';
    activeChallenge.opts.forEach((o, i) => {
        const btn = document.createElement('button');
        btn.className = 'option-btn';
        btn.innerText = o;
        btn.onclick = () => submitChallenge(i);
        optsDiv.appendChild(btn);
    });
    document.getElementById('challenge-modal').classList.remove('hidden');
}

function submitChallenge(idx) {
    const correct = idx === activeChallenge.ans;
    if (!correct && activeChallenge.type === 'threat') breachTimer += 15;

    document.getElementById('challenge-modal').classList.add('hidden');

    if (activeChallenge.type === 'boss' && correct) {
        endGame('ROOT SERVER SECURED', true);
    } else if (correct && activeChallenge.type !== 'boss') {
        entities = entities.filter(e => e.id !== activeChallenge.id);
    }

    activeChallenge = null;
}

function gameLoop() {
    if (gameState === 'PLAYING') {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        for (let x = 0; x < GRID_SIZE; x++) {
            for (let y = 0; y < GRID_SIZE; y++) {
                networkGrid[x][y].draw();
            }
        }

        entities.forEach(e => {
            if (!networkGrid[e.x][e.y].discovered) return;
            ctx.fillStyle = COLORS[e.type] || '#fff';
            ctx.beginPath();
            ctx.arc((e.x + 0.5) * CELL_SIZE, (e.y + 0.5) * CELL_SIZE, CELL_SIZE * 0.25, 0, Math.PI * 2);
            ctx.fill();
            if (e.type === NODE_TYPES.GATE) {
                ctx.strokeStyle = '#fff'; ctx.lineWidth = 1; ctx.stroke();
            }
        });

        if (networkGrid[rootServer.x][rootServer.y].discovered) {
            ctx.fillStyle = COLORS.rootServer;
            ctx.shadowBlur = 10; ctx.shadowColor = COLORS.rootServer;
            ctx.fillRect((rootServer.x + 0.2) * CELL_SIZE, (rootServer.y + 0.2) * CELL_SIZE, CELL_SIZE * 0.6, CELL_SIZE * 0.6);
            ctx.shadowBlur = 0;
        }

        const targetX = agent.gridX * CELL_SIZE + CELL_SIZE / 2;
        const targetY = agent.gridY * CELL_SIZE + CELL_SIZE / 2;
        agent.x += (targetX - agent.x) * 0.25;
        agent.y += (targetY - agent.y) * 0.25;

        ctx.fillStyle = COLORS.agent;
        ctx.shadowBlur = 15; ctx.shadowColor = COLORS.agent;
        ctx.beginPath(); ctx.arc(agent.x, agent.y, CELL_SIZE * 0.35, 0, Math.PI * 2); ctx.fill();
        ctx.shadowBlur = 0;

        updateHUD();
    }
    requestAnimationFrame(gameLoop);
}

function updateHUD() {
    const str = `${Math.floor(breachTimer / 60).toString().padStart(2, '0')}:${(breachTimer % 60).toString().padStart(2, '0')}`;
    document.getElementById('timer-val').innerText = str;
    document.getElementById('hud-timer').innerText = str;
}

function endGame(status, win) {
    gameState = 'END';
    document.getElementById('end-overlay').classList.remove('hidden');
    document.getElementById('end-status').innerText = status;
    document.getElementById('end-details').innerText = win ? `Breach Neutralized in ${document.getElementById('hud-timer').innerText}` : `Network Infiltrated.`;
}

setInterval(() => { if (gameState === 'PLAYING' && !activeChallenge) breachTimer++; }, 1000);

document.getElementById('start-btn').onclick = () => {
    document.getElementById('game-overlay').classList.add('hidden');
    gameState = 'PLAYING';
    initNetwork();
    agent.x = CELL_SIZE / 2; agent.y = CELL_SIZE / 2;
};
document.getElementById('restart-btn').onclick = () => location.reload();

function resize() {
    const size = Math.min(window.innerWidth * 0.9, window.innerHeight * 0.6);
    canvas.width = size; canvas.height = size;
    CELL_SIZE = size / GRID_SIZE;
}

window.onresize = resize;
resize();
gameLoop();
