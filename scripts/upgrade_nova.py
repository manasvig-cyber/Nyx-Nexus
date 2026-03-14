import re

with open("cyber-roadmap.html", "r", encoding="utf-8") as f:
    html = f.read()

# Make sidebar button clickable if not already 
html = re.sub(
    r'<div class="nav-item" style="--i: #8b5cf6; --j: #ec4899;">\s*<i class="fas fa-robot"></i>\s*<span class="nav-label">Nova AI</span>\s*</div>',
    '<div class="nav-item" style="--i: #8b5cf6; --j: #ec4899;" onclick="toggleNova()">\n                <i class="fas fa-robot"></i>\n                <span class="nav-label">Nova AI</span>\n            </div>',
    html
)

# Strip old NOVA stuff
html = re.sub(r'\s*/\*\s*NOVA AI Widget CSS\s*\*/.*?(?=</style>)', '', html, flags=re.DOTALL)
html = re.sub(r'\s*<!-- NOVA AI Floating Widget -->.*?(?=</main>)', '', html, flags=re.DOTALL)
html = re.sub(r'\s*// NOVA AI Chat Logic.*?(?=</script>)', '', html, flags=re.DOTALL)

# Clean just in case
html = re.sub(r'\s*<!-- MR NOVA.*?</div>\s*</div>', '', html, flags=re.DOTALL)

# Insert new CSS
css_code = """
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
            width: 65px;
            height: 65px;
            border-radius: 50%;
            background: rgba(15, 23, 42, 0.9);
            border: 2px solid var(--blue);
            color: var(--cyan);
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 28px;
            cursor: pointer;
            box-shadow: 0 0 20px rgba(6, 182, 212, 0.6);
            transition: all 0.3s ease;
            float: right;
            position: relative;
        }
        
        .nova-trigger.listening {
            animation: pulseMic 1.5s infinite;
            background: rgba(6, 182, 212, 0.3);
            border-color: #fff;
            color: #fff;
        }
        
        .nova-trigger:hover {
            transform: scale(1.1);
            box-shadow: 0 0 30px rgba(6, 182, 212, 0.9);
        }

        @keyframes pulseMic {
            0% { transform: scale(1); box-shadow: 0 0 20px rgba(6, 182, 212, 0.6); }
            50% { transform: scale(1.2); box-shadow: 0 0 40px rgba(6, 182, 212, 1); }
            100% { transform: scale(1); box-shadow: 0 0 20px rgba(6, 182, 212, 0.6); }
        }

        .nova-chat-panel {
            position: absolute;
            bottom: 85px;
            right: 0;
            width: 420px;
            height: 520px;
            background: rgba(15, 23, 42, 0.95);
            border: 1px solid var(--cyan);
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.8), 0 0 20px rgba(6, 182, 212, 0.2);
            display: none;
            flex-direction: column;
            overflow: hidden;
            backdrop-filter: blur(10px);
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.4s ease, transform 0.4s ease;
            padding: 0;
        }
        
        .nova-chat-panel.show {
            display: flex;
            opacity: 1;
            transform: translateY(0);
        }

        .nova-header {
            background: rgba(6, 182, 212, 0.15);
            padding: 16px;
            border-bottom: 1px solid rgba(6, 182, 212, 0.3);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .nova-header-info {
            display: flex;
            flex-direction: column;
        }
        .nova-header-title {
            font-family: 'Orbitron', sans-serif;
            color: var(--cyan);
            font-size: 18px;
            font-weight: bold;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .nova-header-subtitle {
            font-size: 12px;
            color: var(--text-sub);
            margin-top: 4px;
            font-family: 'Rajdhani', sans-serif;
        }
        
        .nova-suggestions {
            padding: 10px 16px;
            background: rgba(0, 0, 0, 0.2);
            border-bottom: 1px solid rgba(255,255,255,0.05);
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .nova-suggestions-title {
            font-size: 12px;
            color: var(--text-sub);
            font-weight: bold;
            text-transform: uppercase;
        }
        .nova-suggestions-list {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }
        .nova-suggestion-btn {
            background: rgba(6, 182, 212, 0.1);
            border: 1px solid rgba(6, 182, 212, 0.3);
            color: var(--cyan);
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 12px;
            cursor: pointer;
            transition: 0.2s;
            font-family: 'Rajdhani', sans-serif;
        }
        .nova-suggestion-btn:hover {
            background: rgba(6, 182, 212, 0.3);
            color: #fff;
        }

        .nova-body {
            padding: 16px;
            flex: 1;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        
        .chat-msg {
            padding: 12px 16px;
            border-radius: 12px;
            font-size: 15px;
            line-height: 1.5;
            max-width: 85%;
            word-wrap: break-word;
            animation: fadeInMsg 0.3s ease;
        }
        
        @keyframes fadeInMsg {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .user-msg {
            background: rgba(139, 92, 246, 0.2);
            border: 1px solid var(--purple-l);
            color: #fff;
            align-self: flex-end;
            border-bottom-right-radius: 0;
        }
        .nova-msg {
            background: rgba(6, 182, 212, 0.1);
            border: 1px solid rgba(6, 182, 212, 0.4);
            color: var(--cyan);
            align-self: flex-start;
            border-bottom-left-radius: 0;
            box-shadow: 0 0 10px rgba(6, 182, 212, 0.1);
            font-family: 'Rajdhani', sans-serif;
        }
        
        .nova-input-container {
            display: flex;
            padding: 16px;
            border-top: 1px solid rgba(6, 182, 212, 0.3);
            background: rgba(0,0,0,0.3);
            gap: 10px;
            align-items: center;
        }
        
        .nova-input-container input {
            flex: 1;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            color: #fff;
            padding: 10px 14px;
            border-radius: 6px;
            font-family: 'Rajdhani', sans-serif;
            font-size: 15px;
            outline: none;
            transition: 0.3s;
        }
        .nova-input-container input:focus {
            border-color: var(--cyan);
            box-shadow: 0 0 10px rgba(6, 182, 212, 0.2);
        }
        
        .nova-action-btn {
            background: var(--cyan);
            border: none;
            color: #000;
            width: 42px;
            height: 42px;
            border-radius: 50%;
            cursor: pointer;
            transition: 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
        }
        .nova-action-btn:hover {
            background: var(--blue-l);
            color: #fff;
            box-shadow: 0 0 15px var(--blue-l);
        }
        
        .mic-btn {
            background: transparent;
            border: 1px solid var(--cyan);
            color: var(--cyan);
        }
        .mic-btn:hover {
            background: rgba(6, 182, 212, 0.2);
            color: #fff;
        }
        .mic-btn.active {
            animation: pulseMic 1.5s infinite;
            background: rgba(6, 182, 212, 0.4);
            color: #fff;
            border-color: #fff;
        }

        .typing-indicator span {
            display: inline-block;
            width: 6px;
            height: 6px;
            background: var(--cyan);
            border-radius: 50%;
            margin: 0 2px;
            animation: typing 1.4s infinite ease-in-out both;
        }
        .typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
        .typing-indicator span:nth-child(2) { animation-delay: -0.16s; }
        @keyframes typing {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1); }
        }
"""
html = html.replace("</style>", css_code + "\n    </style>")

# HTML Insert
html_code = """
    <!-- MR NOVA AI Floating Widget -->
    <div class="nova-widget">
        <div class="nova-chat-panel" id="nova-chat-panel">
            <div class="nova-header">
                <div class="nova-header-info">
                    <div class="nova-header-title">🤖 MR NOVA AI &mdash; Cyber Assistant</div>
                    <div class="nova-header-subtitle">Ask me anything about this platform</div>
                </div>
                <i class="fas fa-times" style="cursor:pointer; color: var(--cyan); font-size: 18px;" onclick="toggleNova()"></i>
            </div>
            
            <div class="nova-suggestions">
                <div class="nova-suggestions-title">Try asking:</div>
                <div class="nova-suggestions-list">
                    <div class="nova-suggestion-btn" onclick="prefillNova('Explain this page')">Explain this page</div>
                    <div class="nova-suggestion-btn" onclick="prefillNova('Help with CTF')">Help with CTF</div>
                    <div class="nova-suggestion-btn" onclick="prefillNova('What should I learn next')">What should I learn next</div>
                    <div class="nova-suggestion-btn" onclick="prefillNova('Explain networking')">Explain networking</div>
                </div>
            </div>

            <div class="nova-body" id="nova-body">
                <div class="chat-msg nova-msg">Hello! I am MR NOVA. How can I assist you today? Try asking me to "Explain this page".</div>
            </div>
            
            <div class="nova-input-container">
                <button class="nova-action-btn mic-btn" id="nova-mic-btn" onclick="toggleNovaVoice()"><i class="fas fa-microphone"></i></button>
                <input type="text" id="nova-input-field" placeholder="Ask MR NOVA..." onkeypress="handleNovaKey(event)">
                <button class="nova-action-btn" onclick="sendNovaMessage()"><i class="fas fa-paper-plane"></i></button>
            </div>
        </div>
        
        <div class="nova-trigger" id="nova-trigger-btn" onclick="toggleNova()">
            <i class="fas fa-microphone"></i>
        </div>
    </div>
"""
# Find the LAST index of </main> in case there's another.
main_idx = html.rfind("</main>")
html = html[:main_idx] + html_code + "\n    </main>" + html[main_idx+7:]


# JS Insert
js_code = """
        // MR NOVA AI Smart Logic
        let novaVoiceActive = false;
        let recognition = null;

        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            
            recognition.onstart = function() {
                novaVoiceActive = true;
                const micBtn = document.getElementById('nova-mic-btn');
                const triggerBtn = document.getElementById('nova-trigger-btn');
                if(micBtn) micBtn.classList.add('active');
                if(triggerBtn) triggerBtn.classList.add('listening');
            };
            
            recognition.onresult = function(event) {
                const transcript = event.results[0][0].transcript;
                document.getElementById('nova-input-field').value = transcript;
                sendNovaMessage();
            };
            
            recognition.onerror = function(event) {
                console.error("Speech recognition error", event.error);
                stopNovaVoice();
            };
            
            recognition.onend = function() {
                stopNovaVoice();
            };
        }

        function toggleNovaVoice() {
            if (!recognition) {
                alert("Voice recognition is not supported in this browser.");
                return;
            }
            // Auto open panel if currently closed when user clicks global mic
            const panel = document.getElementById('nova-chat-panel');
            if (!panel.classList.contains('show')) {
                toggleNova();
            }

            if (novaVoiceActive) {
                recognition.stop();
            } else {
                recognition.start();
            }
        }
        
        function stopNovaVoice() {
            novaVoiceActive = false;
            const micBtn = document.getElementById('nova-mic-btn');
            const triggerBtn = document.getElementById('nova-trigger-btn');
            if(micBtn) micBtn.classList.remove('active');
            if(triggerBtn) triggerBtn.classList.remove('listening');
        }

        function toggleNova() {
            const panel = document.getElementById('nova-chat-panel');
            if (panel.classList.contains('show')) {
                panel.classList.remove('show');
                setTimeout(() => panel.style.display = 'none', 400); // wait for anim
            } else {
                panel.style.display = 'flex';
                // trigger reflow
                void panel.offsetWidth;
                panel.classList.add('show');
                document.getElementById('nova-input-field').focus();
            }
        }

        function prefillNova(text) {
            document.getElementById('nova-input-field').value = text;
            sendNovaMessage();
        }

        function handleNovaKey(e) {
            if (e.key === 'Enter') {
                sendNovaMessage();
            }
        }

        function getContextAwareResponse(text) {
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
                
                // Fallback for current page
                return "This section is designed to help you improve your cybersecurity skills. You are currently exploring the " + (document.title || "platform") + ".";
            }

            return "I am MR NOVA, your context-aware cyber assistant. Try asking me 'Explain this page' or 'What should I learn next'.";
        }

        function speakText(text) {
            if ('speechSynthesis' in window) {
                // Cancel any ongoing speech
                window.speechSynthesis.cancel();
                
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.rate = 1.0;
                utterance.pitch = 1.0;
                window.speechSynthesis.speak(utterance);
            }
        }

        function typeMessage(element, text, callback) {
            element.innerText = '';
            let i = 0;
            element.style.color = 'var(--cyan)'; 
            
            const interval = setInterval(() => {
                element.innerText += text.charAt(i);
                
                const body = document.getElementById('nova-body');
                body.scrollTop = body.scrollHeight;
                
                i++;
                if (i >= text.length) {
                    clearInterval(interval);
                    if (callback) callback();
                }
            }, 30);
        }

        function sendNovaMessage() {
            const input = document.getElementById('nova-input-field');
            const text = input.value.trim();
            if(!text) return;
            
            const body = document.getElementById('nova-body');
            
            // Add user message
            const userMsg = document.createElement('div');
            userMsg.className = 'chat-msg user-msg';
            userMsg.innerText = text;
            body.appendChild(userMsg);
            input.value = '';
            
            // Scroll to bottom
            body.scrollTop = body.scrollHeight;

            // Show typing indicator
            const typingMsg = document.createElement('div');
            typingMsg.className = 'chat-msg nova-msg typing-indicator';
            typingMsg.id = 'temp-typing';
            typingMsg.innerHTML = 'MR NOVA is thinking<span></span><span></span><span></span>';
            body.appendChild(typingMsg);
            body.scrollTop = body.scrollHeight;

            // Generate Response
            const responseText = getContextAwareResponse(text);

            setTimeout(() => {
                const temp = document.getElementById('temp-typing');
                if(temp) temp.remove();
                
                const responseMsg = document.createElement('div');
                responseMsg.className = 'chat-msg nova-msg';
                body.appendChild(responseMsg);
                
                // Type it out
                typeMessage(responseMsg, responseText, () => {
                    // Speak it out after typing finishes (or could do simultaneously)
                    speakText(responseText);
                });
                
            }, 800 + Math.random() * 500); // realistic think time
        }
"""
html = html.replace("</script>", js_code + "\n    </script>")

with open("cyber-roadmap.html", "w", encoding="utf-8") as f:
    f.write(html)
