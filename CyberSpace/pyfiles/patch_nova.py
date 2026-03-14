import re

with open("cyber-roadmap.html", "r", encoding="utf-8") as f:
    html = f.read()

# CSS Injection
css_code = """
        /* NOVA AI Widget CSS */
        .nova-widget {
            position: fixed;
            bottom: 30px;
            right: 30px;
            z-index: 9999;
            font-family: 'Rajdhani', sans-serif;
        }
        .nova-trigger {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--purple), var(--cyan));
            color: #fff;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 28px;
            cursor: pointer;
            box-shadow: 0 0 20px rgba(6, 182, 212, 0.5);
            transition: 0.3s;
            float: right;
        }
        .nova-trigger:hover {
            transform: scale(1.1);
            box-shadow: 0 0 30px rgba(6, 182, 212, 0.8);
        }
        .nova-chat-panel {
            position: absolute;
            bottom: 80px;
            right: 0;
            width: 320px;
            background: rgba(15, 23, 42, 0.95);
            border: 1px solid var(--cyan);
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.8);
            display: none;
            flex-direction: column;
            overflow: hidden;
            backdrop-filter: blur(10px);
        }
        .nova-header {
            background: rgba(6, 182, 212, 0.2);
            padding: 15px;
            font-family: 'Orbitron', sans-serif;
            color: var(--cyan);
            font-size: 16px;
            font-weight: bold;
            border-bottom: 1px solid rgba(6, 182, 212, 0.3);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .nova-body {
            padding: 15px;
            height: 250px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        .chat-msg {
            padding: 10px 15px;
            border-radius: 10px;
            font-size: 15px;
            line-height: 1.4;
            max-width: 85%;
            word-wrap: break-word;
        }
        .user-msg {
            background: rgba(139, 92, 246, 0.2);
            border: 1px solid var(--purple-l);
            color: #fff;
            align-self: flex-end;
            border-bottom-right-radius: 0;
        }
        .nova-msg {
            background: rgba(6, 182, 212, 0.15);
            border: 1px solid var(--cyan);
            color: var(--cyan);
            align-self: flex-start;
            border-bottom-left-radius: 0;
        }
        .nova-input {
            display: flex;
            padding: 10px;
            border-top: 1px solid rgba(6, 182, 212, 0.3);
            background: rgba(0,0,0,0.2);
        }
        .nova-input input {
            flex: 1;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            color: #fff;
            padding: 8px 12px;
            border-radius: 4px;
            font-family: 'Rajdhani', sans-serif;
            outline: none;
        }
        .nova-input button {
            background: var(--cyan);
            border: none;
            color: #fff;
            width: 40px;
            margin-left: 10px;
            border-radius: 4px;
            cursor: pointer;
            transition: 0.3s;
        }
        .nova-input button:hover {
            background: var(--blue-l);
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


# HTML Injection
html_code = """
    <!-- NOVA AI Floating Widget -->
    <div class="nova-widget">
        <div class="nova-chat-panel" id="nova-chat-panel">
            <div class="nova-header">
                <div><i class="fas fa-robot"></i> NOVA AI</div>
                <i class="fas fa-times" style="cursor:pointer;" onclick="toggleNova()"></i>
            </div>
            <div class="nova-body" id="nova-body">
                <div class="chat-msg nova-msg">Hello! I am NOVA. Ask me to "explain this room" to see what I can do.</div>
            </div>
            <div class="nova-input">
                <input type="text" id="nova-input-field" placeholder="Ask NOVA..." onkeypress="handleNovaKey(event)">
                <button onclick="sendNovaMessage()"><i class="fas fa-paper-plane"></i></button>
            </div>
        </div>
        <div class="nova-trigger" onclick="toggleNova()">
            <i class="fas fa-robot"></i>
        </div>
    </div>
"""
html = html.replace("</main>", html_code + "\n    </main>")


# JS Injection
js_code = """
        // NOVA AI Chat Logic
        function toggleNova() {
            const panel = document.getElementById('nova-chat-panel');
            panel.style.display = panel.style.display === 'flex' ? 'none' : 'flex';
            if(panel.style.display === 'flex'){
                document.getElementById('nova-input-field').focus();
            }
        }

        function handleNovaKey(e) {
            if (e.key === 'Enter') {
                sendNovaMessage();
            }
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
            typingMsg.innerHTML = '<span></span><span></span><span></span>';
            body.appendChild(typingMsg);
            body.scrollTop = body.scrollHeight;

            setTimeout(() => {
                const temp = document.getElementById('temp-typing');
                if(temp) temp.remove();
                
                const responseMsg = document.createElement('div');
                responseMsg.className = 'chat-msg nova-msg';
                
                // Smart response mapping based on query!
                const lowerText = text.toLowerCase();
                if(lowerText.includes('explain this room') || lowerText.includes('explain')) {
                    responseMsg.innerText = "This room teaches networking fundamentals including OSI layers and packet flow.";
                } else if(lowerText.includes('nova')) {
                    responseMsg.innerText = "Hello! I am NOVA, your personal AI learning assistant. Ask me to 'explain this room'!";
                } else {
                    responseMsg.innerText = "I am currently focused on guiding you through the roadmap. Ask me to 'explain this room' to learn more!";
                }
                
                body.appendChild(responseMsg);
                body.scrollTop = body.scrollHeight;
            }, 1000);
        }
"""
html = html.replace("</script>", js_code + "\n    </script>")

with open("cyber-roadmap.html", "w", encoding="utf-8") as f:
    f.write(html)
