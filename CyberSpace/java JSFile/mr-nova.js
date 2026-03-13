document.addEventListener("DOMContentLoaded", function () {
    // 1. Inject CSS
    const style = document.createElement('style');
    style.innerHTML = `
        /* MR NOVA AI Widget CSS */
        .nova-widget {
            position: fixed;
            bottom: 30px;
            right: 30px;
            z-index: 9999;
            font-family: 'Rajdhani', sans-serif;
        }
        
        /* Floating Voice Orb */
        .nova-trigger {
            width: 70px;
            height: 70px;
            border-radius: 50%;
            background: rgba(15, 23, 42, 0.8);
            border: 2px solid var(--cyan);
            color: var(--cyan);
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 30px;
            cursor: pointer;
            box-shadow: 0 0 20px rgba(6, 182, 212, 0.4), inset 0 0 15px rgba(6, 182, 212, 0.2);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            float: right;
            position: relative;
            backdrop-filter: blur(5px);
        }
        
        .nova-trigger.listening {
            animation: pulseMic 1.5s infinite;
            background: rgba(6, 182, 212, 0.2);
            border-color: #fff;
            color: #fff;
        }
        
        .nova-trigger:hover {
            transform: scale(1.1) rotate(5deg);
            box-shadow: 0 0 35px rgba(6, 182, 212, 0.8), 0 0 15px rgba(168, 85, 247, 0.5);
            border-color: var(--purple-l);
        }

        .nova-robot-icon {
            width: 50px;
            height: 50px;
            object-fit: contain;
            filter: drop-shadow(0 0 5px var(--cyan));
        }

        @keyframes pulseMic {
            0% { transform: scale(1); box-shadow: 0 0 20px rgba(6, 182, 212, 0.6); }
            50% { transform: scale(1.15); box-shadow: 0 0 40px rgba(6, 182, 212, 1), 0 0 20px rgba(168, 85, 247, 0.6); }
            100% { transform: scale(1); box-shadow: 0 0 20px rgba(6, 182, 212, 0.6); }
        }

        .nova-chat-panel {
            position: absolute;
            bottom: 90px;
            right: 0;
            width: 430px;
            height: 550px;
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.9), rgba(30, 17, 54, 0.9));
            border: 1px solid rgba(6, 182, 212, 0.4);
            border-radius: 20px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.9), 0 0 30px rgba(6, 182, 212, 0.2), inset 0 0 20px rgba(255,255,255,0.02);
            display: none;
            flex-direction: column;
            overflow: hidden;
            backdrop-filter: blur(20px);
            opacity: 0;
            transform: translateY(30px) scale(0.95);
            transition: all 0.5s cubic-bezier(0.165, 0.84, 0.44, 1);
            padding: 0;
            text-align: left;
            z-index: 10000;
        }
        
        .nova-chat-panel.show {
            display: flex;
            opacity: 1;
            transform: translateY(0) scale(1);
        }

        .nova-header {
            background: linear-gradient(90deg, rgba(6, 182, 212, 0.25), rgba(168, 85, 247, 0.25));
            padding: 20px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: relative;
        }

        .nova-header::after {
            content: '';
            position: absolute;
            bottom: -1px;
            left: 0;
            width: 100%;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--cyan), var(--purple-l), transparent);
        }

        .nova-header-info {
            display: flex;
            flex-direction: column;
        }
        .nova-header-title {
            font-family: 'Orbitron', sans-serif;
            color: #fff;
            font-size: 18px;
            font-weight: 800;
            display: flex;
            align-items: center;
            gap: 10px;
            text-shadow: 0 0 10px rgba(6, 182, 212, 0.8);
            letter-spacing: 1px;
        }
        .nova-header-subtitle {
            font-size: 11px;
            color: var(--text-sub);
            margin-top: 4px;
            font-family: 'Rajdhani', sans-serif;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        .nova-suggestions {
            padding: 12px 20px;
            background: rgba(0, 0, 0, 0.3);
            border-bottom: 1px solid rgba(255,255,255,0.05);
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .nova-suggestions-title {
            font-size: 10px;
            color: rgba(255,255,255,0.5);
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 1.5px;
        }
        .nova-suggestions-list {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }
        .nova-suggestion-btn {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(6, 182, 212, 0.3);
            color: var(--cyan);
            padding: 6px 14px;
            border-radius: 8px;
            font-size: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: 'Rajdhani', sans-serif;
            font-weight: 600;
        }
        .nova-suggestion-btn:hover {
            background: rgba(6, 182, 212, 0.2);
            border-color: var(--cyan);
            color: #fff;
            box-shadow: 0 0 15px rgba(6, 182, 212, 0.3);
            transform: translateY(-2px);
        }

        .nova-body {
            padding: 20px;
            flex: 1;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 20px;
            background: radial-gradient(circle at center, rgba(30, 17, 54, 0.2) 0%, transparent 70%);
        }

        /* Custom Scrollbar */
        .nova-body::-webkit-scrollbar {
            width: 4px;
        }
        .nova-body::-webkit-scrollbar-track {
            background: rgba(0,0,0,0.1);
        }
        .nova-body::-webkit-scrollbar-thumb {
            background: rgba(6, 182, 212, 0.3);
            border-radius: 10px;
        }
        
        .chat-msg {
            padding: 14px 18px;
            border-radius: 15px;
            font-size: 14px;
            line-height: 1.6;
            max-width: 88%;
            position: relative;
            animation: fadeInMsg 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            white-space: pre-wrap;
        }
        
        @keyframes fadeInMsg {
            from { opacity: 0; transform: translateY(15px) scale(0.9); }
            to { opacity: 1; transform: translateY(0) scale(1); }
        }

        .user-msg {
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.3), rgba(139, 92, 246, 0.1));
            border: 1px solid rgba(168, 85, 247, 0.4);
            color: #fff;
            align-self: flex-end;
            border-bottom-right-radius: 2px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2), 0 0 10px rgba(168, 85, 247, 0.1);
        }
        .nova-msg {
            background: linear-gradient(135deg, rgba(6, 182, 212, 0.15), rgba(6, 182, 212, 0.05));
            border: 1px solid rgba(6, 182, 212, 0.3);
            color: var(--text-main);
            align-self: flex-start;
            border-bottom-left-radius: 2px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2), 0 0 10px rgba(6, 182, 212, 0.1);
            font-family: 'Rajdhani', sans-serif;
            font-weight: 500;
        }
        
        .nova-input-container {
            display: flex;
            padding: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            background: rgba(0,0,0,0.4);
            gap: 12px;
            align-items: center;
        }
        
        .nova-input-container input {
            flex: 1;
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.1);
            color: #fff;
            padding: 12px 16px;
            border-radius: 12px;
            font-family: 'Rajdhani', sans-serif;
            font-size: 15px;
            outline: none;
            transition: all 0.3s ease;
        }
        .nova-input-container input:focus {
            border-color: var(--cyan);
            background: rgba(6, 182, 212, 0.05);
            box-shadow: 0 0 20px rgba(6, 182, 212, 0.15);
        }
        
        .nova-action-btn {
            background: linear-gradient(135deg, var(--cyan), var(--blue));
            border: none;
            color: #000;
            width: 45px;
            height: 45px;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            box-shadow: 0 4px 15px rgba(6, 182, 212, 0.3);
        }
        .nova-action-btn:hover {
            transform: translateY(-2px) scale(1.05);
            box-shadow: 0 6px 20px rgba(6, 182, 212, 0.5);
            filter: brightness(1.2);
        }
        
        .mic-btn {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(6, 182, 212, 0.4);
            color: var(--cyan);
            box-shadow: none;
        }
        .mic-btn:hover {
            background: rgba(6, 182, 212, 0.2);
            color: #fff;
            border-color: var(--cyan);
        }
        .mic-btn.active {
            animation: pulseMicSmall 1.5s infinite;
            background: var(--cyan);
            color: #000;
            border-color: #fff;
        }

        @keyframes pulseMicSmall {
            0% { box-shadow: 0 0 0 0 rgba(6, 182, 212, 0.7); }
            70% { box-shadow: 0 0 0 10px rgba(6, 182, 212, 0); }
            100% { box-shadow: 0 0 0 0 rgba(6, 182, 212, 0); }
        }

        .typing-indicator {
            padding: 10px 15px;
            font-style: italic;
            font-size: 12px;
            color: var(--cyan);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .typing-indicator span {
            display: inline-block;
            width: 5px;
            height: 5px;
            background: var(--cyan);
            border-radius: 50%;
            animation: typing 1.4s infinite ease-in-out both;
            box-shadow: 0 0 5px var(--cyan);
        }
        .typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
        .typing-indicator span:nth-child(2) { animation-delay: -0.16s; }
        @keyframes typing {
            0%, 80%, 100% { transform: scale(0); opacity: 0.3; }
            40% { transform: scale(1.2); opacity: 1; }
        }
    `;
    document.head.appendChild(style);

    // 2. Inject HTML
    const novaHTML = `
        <div class="nova-chat-panel" id="nova-chat-panel">
            <div class="nova-header">
                <div class="nova-header-info">
                    <div class="nova-header-title">
                        <i class="fas fa-microchip"></i> MR NOVA AI
                    </div>
                    <div class="nova-header-subtitle">Advanced Cyber Intelligence</div>
                </div>
                <div style="display: flex; gap: 15px; align-items: center;">
                    <i class="fas fa-circle" style="font-size: 8px; color: var(--green); filter: drop-shadow(0 0 5px var(--green));"></i>
                    <i class="fas fa-times" style="cursor:pointer; color: rgba(255,255,255,0.5); font-size: 18px; transition: 0.3s;" onmouseover="this.style.color='var(--cyan)'" onmouseout="this.style.color='rgba(255,255,255,0.5)'" onclick="window.toggleNova()"></i>
                </div>
            </div>
            
            <div class="nova-suggestions">
                <div class="nova-suggestions-title">Quick Queries</div>
                <div class="nova-suggestions-list">
                    <div class="nova-suggestion-btn" onclick="window.prefillNova('Explain this page')">Surface Analysis</div>
                    <div class="nova-suggestion-btn" onclick="window.prefillNova('Help with CTF')">CTF Protocols</div>
                    <div class="nova-suggestion-btn" onclick="window.prefillNova('What should I learn next')">Growth Path</div>
                    <div class="nova-suggestion-btn" onclick="window.prefillNova('Explain networking')">Network Core</div>
                </div>
            </div>

            <div class="nova-body" id="nova-body">
                <div class="chat-msg nova-msg">System initialized. I am **MR NOVA**, your dedicated cyber assistant. How can I help you navigate the Nexus today?</div>
            </div>
            
            <div class="nova-input-container">
                <button class="nova-action-btn mic-btn" id="nova-mic-btn" title="Voice Input" onclick="window.toggleNovaVoice()">
                    <i class="fas fa-microphone"></i>
                </button>
                <input type="text" id="nova-input-field" placeholder="Input command..." onkeypress="window.handleNovaKey(event)">
                <button class="nova-action-btn" title="Send Message" onclick="window.sendNovaMessage()">
                    <i class="fas fa-paper-plane"></i>
                </button>
            </div>
        </div>
        
        <div class="nova-trigger" id="nova-trigger-btn" onclick="window.toggleNova()">
            <img src="mr nova.png" class="nova-robot-icon" alt="MR NOVA">
        </div>
    `;
    const novaContainer = document.createElement('div');
    novaContainer.className = 'nova-widget';
    novaContainer.innerHTML = novaHTML;
    document.body.appendChild(novaContainer);

    // Sidebar navigation link hook
    const sidebarNovaBtn = document.querySelector('.nav-item i.fa-robot');
    if (sidebarNovaBtn && sidebarNovaBtn.parentElement) {
        sidebarNovaBtn.parentElement.onclick = window.toggleNova;
    }
});

// MR NOVA AI Smart Logic attached to window
window.novaVoiceActive = false;
window.recognitionObj = null;

if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    window.recognitionObj = new SpeechRecognition();
    window.recognitionObj.continuous = false;
    window.recognitionObj.interimResults = false;

    window.recognitionObj.onstart = function () {
        window.novaVoiceActive = true;
        const micBtn = document.getElementById('nova-mic-btn');
        const triggerBtn = document.getElementById('nova-trigger-btn');
        if (micBtn) micBtn.classList.add('active');
        if (triggerBtn) triggerBtn.classList.add('listening');
    };

    window.recognitionObj.onresult = function (event) {
        const transcript = event.results[0][0].transcript;
        document.getElementById('nova-input-field').value = transcript;
        window.sendNovaMessage();
    };

    window.recognitionObj.onerror = function (event) {
        console.error("Speech recognition error", event.error);
        window.stopNovaVoice();
    };

    window.recognitionObj.onend = function () {
        window.stopNovaVoice();
    };
}

window.toggleNovaVoice = function () {
    if (!window.recognitionObj) {
        alert("Voice recognition is not supported in this browser.");
        return;
    }
    const panel = document.getElementById('nova-chat-panel');
    if (!panel.classList.contains('show')) {
        window.toggleNova();
    }

    if (window.novaVoiceActive) {
        window.recognitionObj.stop();
    } else {
        window.recognitionObj.start();
    }
};

window.stopNovaVoice = function () {
    window.novaVoiceActive = false;
    const micBtn = document.getElementById('nova-mic-btn');
    const triggerBtn = document.getElementById('nova-trigger-btn');
    if (micBtn) micBtn.classList.remove('active');
    if (triggerBtn) triggerBtn.classList.remove('listening');
};

window.toggleNova = function () {
    const panel = document.getElementById('nova-chat-panel');
    if (!panel) return;
    if (panel.classList.contains('show')) {
        panel.classList.remove('show');
        setTimeout(() => panel.style.display = 'none', 400);
    } else {
        panel.style.display = 'flex';
        void panel.offsetWidth;
        panel.classList.add('show');
        document.getElementById('nova-input-field').focus();
    }
};

window.prefillNova = function (text) {
    document.getElementById('nova-input-field').value = text;
    window.sendNovaMessage();
};

window.handleNovaKey = function (e) {
    if (e.key === 'Enter') {
        window.sendNovaMessage();
    }
};

window.getContextAwareResponse = function (text) {
    const lowerText = text.toLowerCase();
    const path = window.location.pathname.toLowerCase();
    const title = document.title.toLowerCase();

    // General Knowledge
    if (lowerText.includes('explain networking') || lowerText.includes('what is networking')) {
        return "Networking is the practice of transporting and exchanging data between nodes over a shared medium in an information system. Key concepts include the OSI model, TCP/IP, and packet flow.";
    }
    if (lowerText.includes('what does a soc analyst do') || lowerText.includes('soc analyst')) {
        return "A SOC (Security Operations Center) Analyst monitors an organization's IT infrastructure, detects security events, and responds to cybersecurity incidents in real-time.";
    }
    if (lowerText.includes('what should i learn next')) {
        return "Based on the roadmap, if you have finished Networking and Linux basics, your next step is Security Basics, applying concepts like cryptography and authentication.";
    }
    if (lowerText.includes('help with ctf') || lowerText.includes('ctf')) {
        return "For CTF (Capture The Flag) challenges, start by analyzing the given context. If it's crypto, look for base64 or common ciphers. If it's a web challenge, check the source code and try basic injections.";
    }

    // Context-Aware Explanations
    if (lowerText.includes('explain this page') || lowerText.includes('explain this room') || lowerText.includes('what is this section') || lowerText.includes('explain') || lowerText.includes('what is this room')) {

        if (path.includes('roadmap') || title.includes('roadmap')) {
            return "This page shows the cybersecurity learning roadmap. You start with foundational skills like networking and Linux, then move toward security fundamentals and finally choose a specialization like SOC Analyst, Pentester, or Cloud Security Engineer.";
        }
        if (path.includes('ctf') || title.includes('ctf')) {
            return "This page contains Capture The Flag challenges designed to test cybersecurity skills such as decoding, packet analysis, and hidden flag discovery.";
        }
        if (path.includes('network') || title.includes('network')) {
            return "This room teaches networking fundamentals including OSI layers, TCP/IP communication, and packet flow analysis.";
        }
        if (path.includes('home') || path.includes('dashboard') || path.includes('index') || title.includes('dashboard')) {
            return "Welcome to Nyx Nexus. This platform gamifies cybersecurity learning through interactive labs, challenges, and career roadmaps.";
        }

        return "This section is designed to help you improve your cybersecurity skills. You are currently exploring the platform.";
    }

    return "I am MR NOVA, your context-aware cyber assistant. Try asking me 'Explain this page' or 'What should I learn next'.";
};

window.speakText = function (text) {
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1.0;
        utterance.pitch = 1.0;
        utterance.volume = 1.0;
        window.speechSynthesis.speak(utterance);
    }
};

window.typeMessage = function (element, text, callback) {
    element.textContent = ''; // Fixed spacing issue
    let i = 0;
    element.style.color = 'var(--cyan)';

    // IMPORTANT Fix: using textContent preserves spaces, also no trim.
    const interval = setInterval(() => {
        element.textContent += text.charAt(i);

        const body = document.getElementById('nova-body');
        body.scrollTop = body.scrollHeight;

        i++;
        if (i >= text.length) {
            clearInterval(interval);
            if (callback) callback();
        }
    }, 30);
};

// ==============================
// MR NOVA AI (Ollama Integration)
// ==============================
let novaProcessing = false;
window.getAIResponse = async function (message) {

    try {

        const response = await fetch("http://localhost:8000/nova-ai", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        if (data && data.reply && data.reply.trim().length > 0) {
            return data.reply;
        }

    } catch (error) {
        console.warn("AI unavailable, using local Nova logic.");
    }

    return null;

};

window.sendNovaMessage = async function () {

    // Prevent duplicate triggers
    if (novaProcessing) return;
    novaProcessing = true;

    const input = document.getElementById('nova-input-field');
    const text = input.value;

    if (!text.trim()) {
        novaProcessing = false;
        return;
    }

    const body = document.getElementById('nova-body');

    const userMsg = document.createElement('div');
    userMsg.className = 'chat-msg user-msg';
    userMsg.textContent = text;
    body.appendChild(userMsg);

    input.value = '';
    body.scrollTop = body.scrollHeight;

    const typingMsg = document.createElement('div');
    typingMsg.className = 'chat-msg nova-msg typing-indicator';
    typingMsg.id = 'temp-typing';
    typingMsg.innerHTML = 'MR NOVA is thinking<span></span><span></span><span></span>';
    body.appendChild(typingMsg);

    body.scrollTop = body.scrollHeight;

    // Try AI first
    let responseText = await window.getAIResponse(text);

    // Fallback to existing Nova responses
    if (!responseText) {
        responseText = window.getContextAwareResponse(text);
    }

    setTimeout(() => {

        const temp = document.getElementById('temp-typing');
        if (temp) temp.remove();

        const responseMsg = document.createElement('div');
        responseMsg.className = 'chat-msg nova-msg';
        body.appendChild(responseMsg);

      // Start speech immediately
window.speakText(responseText);

// Start typing animation
window.typeMessage(responseMsg, responseText, () => {
    novaProcessing = false;
});

    }, 800 + Math.random() * 500);

};