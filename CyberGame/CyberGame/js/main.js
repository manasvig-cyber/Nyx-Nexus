import GameEngine from './GameEngine.js';
import { initStars } from './stars.js';

// type="module" scripts are deferred by default, meaning the DOM is already parsed when this runs.
if (window.lucide) {
    window.lucide.createIcons();
}

// Parse episode from URL (e.g., ?ep=2)
const urlParams = new URLSearchParams(window.location.search);
const episodeId = urlParams.get('ep') || "1";

// Start game engine with Episode
const engine = new GameEngine(episodeId);

// Make engine available globally (optional, good for debugging)
window.CyberGameEngine = engine;

// Initialize cyber background effect
initStars();
