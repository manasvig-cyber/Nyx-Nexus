import re

with open("cyber-roadmap.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Title and Subtitle
html = re.sub(
    r'<h1 class="page-title">.*?</h1>',
    r'<h1 class="page-title">CYBERSECURITY CAREER ROADMAP</h1>',
    html, flags=re.DOTALL
)

html = re.sub(
    r'<p class="page-subtitle">.*?</p>',
    r'<p class="page-subtitle">Follow the learning journey from cybersecurity foundations to specialized career roles.</p>',
    html, flags=re.DOTALL
)

# 2. Add Progress Indicator CSS and general animation enhancements
css_injection = """
        .progress-indicator {
            position: absolute;
            top: -30px;
            background: rgba(34, 197, 94, 0.2);
            color: var(--green);
            border: 1px solid var(--green);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 11px;
            font-family: 'Orbitron';
            font-weight: 700;
            letter-spacing: 1px;
            white-space: nowrap;
            text-transform: uppercase;
            box-shadow: 0 0 15px rgba(34, 197, 94, 0.4);
            animation: bounce 2s infinite;
        }

        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-5px); }
        }

        .star-point {
            transform: translate(-50%, -50%);
        }
        
        .section-separator {
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, transparent, rgba(6, 182, 212, 0.5), transparent);
            position: absolute;
            left: 0;
            opacity: 0.5;
        }
"""
html = html.replace('/* Custom Zig-Zag Positions */', css_injection + '\n        /* Custom Snake Positions */')

# Enhance Node labels by making font slightly larger in node-hud
html = html.replace('font-size: 14px;', 'font-size: 15px; font-weight: 500;')
html = html.replace('font-size: 16px;', 'font-size: 18px;')

# Replace CSS positions using slicing to avoid re.sub issues with backslashes
css_positions = """
        /* Custom Snake Positions */
        .tag-foundation { top: 10px; left: 50%; transform: translateX(-50%); box-shadow: 0 0 20px rgba(6, 182, 212, 0.5); text-shadow: 0 0 10px var(--cyan); }
        .tag-specialization { top: 310px; left: 50%; transform: translateX(-50%); box-shadow: 0 0 20px rgba(6, 182, 212, 0.5); text-shadow: 0 0 10px var(--cyan); }
        .tag-careers { top: 970px; left: 50%; transform: translateX(-50%); box-shadow: 0 0 20px rgba(6, 182, 212, 0.5); text-shadow: 0 0 10px var(--cyan); background: rgba(6, 182, 212, 0.2); }

        .n-start { top: 100px; left: 15%; transform: translateX(-50%); }
        .n-networking { top: 100px; left: 50%; transform: translateX(-50%); }
        .n-linux { top: 100px; left: 85%; transform: translateX(-50%); }

        .n-security { top: 400px; left: 85%; transform: translateX(-50%); }
        .n-logic { top: 400px; left: 50%; transform: translateX(-50%); }
        .n-branch { top: 600px; left: 50%; transform: translateX(-50%); }

        .n-soc { top: 1200px; left: 20%; transform: translateX(-50%); }
        .n-pentest { top: 1200px; left: 50%; transform: translateX(-50%); }
        .n-cloud { top: 1200px; left: 80%; transform: translateX(-50%); }

        .locked { opacity: 0.5; filter: grayscale(1); cursor: not-allowed !important; }
        .locked::after { content: 'COMING SOON \\A Future Learning Path'; position: absolute; bottom: -45px; font-family: 'Orbitron'; font-size: 11px; color: #94a3b8; letter-spacing: 1px; text-align: center; white-space: pre-wrap; line-height: 1.4; }

        .n-malware { top: 1450px; left: 35%; transform: translateX(-50%); }
        .n-threat { top: 1450px; left: 65%; transform: translateX(-50%); }
"""
start_idx = html.find('/* Custom Snake Positions */') # It might already be replaced from previous step due to string replacements
if start_idx == -1:
    start_idx = html.find('/* Custom Zig-Zag Positions */')

end_idx = html.find('/* Ambient Decoration */', start_idx)

if start_idx != -1 and end_idx != -1:
    html = html[:start_idx] + css_positions + '\n        ' + html[end_idx:]

# Add pulsing animation to stars and lines inside constellations
html = html.replace('.star-point::before {', '.star-point::before {\n            box-shadow: 0 0 15px rgba(255,255,255,0.5);')

# Replace the HTML content inside the roadmap-container
new_content = """        <div class="roadmap-container">
            <div class="orb" style="top: 10%; left: 5%;"></div>
            <div class="orb" style="bottom: 10%; right: 5%; background: radial-gradient(circle, rgba(6, 182, 212, 0.08) 0%, transparent 70%);"></div>

            <svg class="roadmap-svg" viewBox="0 0 1400 1800" preserveAspectRatio="none">
                <defs>
                    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--cyan)" />
                    </marker>
                    <marker id="arrow-green" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--green)" />
                    </marker>
                    <marker id="arrow-red" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--red)" />
                    </marker>
                    <marker id="arrow-purple" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--purple-l)" />
                    </marker>
                </defs>

                <!-- SECTION CONNECTORS DOWNWARD -->
                
                <!-- Main Path Solid Lines with Arrows for Direction -->
                <path d="M 270,160 L 620,160" class="road-stroke" marker-end="url(#arrow)" />
                <path d="M 760,160 L 1110,160" class="road-stroke" marker-end="url(#arrow)" />
                <path d="M 1190,220 L 1190,320" class="road-stroke" marker-end="url(#arrow)" />
                <path d="M 1110,460 L 780,460" class="road-stroke" marker-end="url(#arrow)" />
                <path d="M 700,520 L 700,560" class="road-stroke" marker-end="url(#arrow)" />

                <!-- Main Path Pulse (Continuous over the same path) -->
                <path d="M 210,160 L 700,160 L 1190,160 L 1190,460 L 700,460 L 700,600" class="road-pulse" style="stroke-width: 3; animation-duration: 8s;" />

                <!-- 3 CAREER BRANCHES -->
                
                <!-- Branch to SOC Analyst -->
                <path d="M 640,660 C 500,660 450,750 450,750 L 320,880 L 380,1020 L 280,1120" style="fill:none; stroke:var(--green); stroke-width:3; opacity:0.6; stroke-dasharray:6,6;" marker-end="url(#arrow-green)"/>
                <path d="M 640,660 C 500,660 450,750 450,750 L 320,880 L 380,1020 L 280,1120" class="road-pulse" style="stroke:var(--green); stroke-width:2; opacity:0.8; animation-duration:4s;" />
                
                <!-- Branch to Pentester -->
                <path d="M 700,700 L 650,800 L 750,950 L 700,1120" style="fill:none; stroke:var(--red); stroke-width:3; opacity:0.6; stroke-dasharray:6,6;" marker-end="url(#arrow-red)"/>
                <path d="M 700,700 L 650,800 L 750,950 L 700,1120" class="road-pulse" style="stroke:var(--red); stroke-width:2; opacity:0.8; animation-duration:4s;" />

                <!-- Branch to Cloud Security -->
                <path d="M 760,660 C 900,660 950,750 950,750 L 1080,880 L 1120,1120" style="fill:none; stroke:var(--purple-l); stroke-width:3; opacity:0.6; stroke-dasharray:6,6;" marker-end="url(#arrow-purple)"/>
                <path d="M 760,660 C 900,660 950,750 950,750 L 1080,880 L 1120,1120" class="road-pulse" style="stroke:var(--purple-l); stroke-width:2; opacity:0.8; animation-duration:4s;" />
                
                <!-- Future Paths -->
                <path d="M 280,1280 L 490,1430" style="fill:none; stroke:#fff; stroke-width:1; opacity:0.2; stroke-dasharray:4,4;" />
                <path d="M 1120,1280 L 910,1430" style="fill:none; stroke:#fff; stroke-width:1; opacity:0.2; stroke-dasharray:4,4;" />
            </svg>

            <!-- Foundation Section -->
            <div class="section-separator" style="top: 20px;"></div>
            <div class="section-tag tag-foundation">FOUNDATION SKILLS</div>

            <div class="node n-start">
                <div class="progress-indicator">You are here</div>
                <i class="fas fa-power-off"></i>
                <div class="node-hud">
                    <h3>SYSTEM START</h3>
                    <p>Initialize your journey into the world of cyber defense.</p>
                </div>
            </div>

            <div class="node n-networking">
                <i class="fas fa-network-wired"></i>
                <div class="node-hud">
                    <h3>NETWORKING</h3>
                    <p>Learn OSI layers, TCP/UDP, and how global data routing works.</p>
                </div>
            </div>

            <div class="node n-linux">
                <i class="fab fa-linux"></i>
                <div class="node-hud">
                    <h3>LINUX CORE</h3>
                    <p>Master the terminal, file systems, and server management.</p>
                </div>
            </div>

            <!-- Core Security Section -->
            <div class="section-separator" style="top: 320px;"></div>
            <div class="section-tag tag-specialization">CORE SECURITY KNOWLEDGE</div>

            <div class="node n-security">
                <i class="fas fa-shield-halved"></i>
                <div class="node-hud">
                    <h3>SECURITY BASICS</h3>
                    <p>Cryptography, access controls, and fundamental risk management.</p>
                </div>
            </div>

            <div class="node n-logic">
                <i class="fas fa-brain"></i>
                <div class="node-hud">
                    <h3>CYBER LOGIC</h3>
                    <p>Developing the hacker mindset: Analysis, logic, and detection.</p>
                </div>
            </div>

            <div class="node n-branch">
                <i class="fas fa-code-branch"></i>
                <div class="node-hud">
                    <h3>CHOOSE PATH</h3>
                    <p>The roadmap splits. Choose your ultimate career destination.</p>
                </div>
            </div>

            <!-- Career Destinations Section -->
            <div class="section-separator" style="top: 980px;"></div>
            <div class="section-tag tag-careers">CAREER DESTINATIONS</div>

            <!-- SOC CONSTELLATION -->
            <div class="star-cluster">
                <div class="section-tag-mini" style="top: 720px; left: 18%; border-left-color: var(--green);">SOC ANALYST PATH</div>

                <div class="star-point" style="top: 750px; left: 450px;">
                    <div class="star-info"><h3>LOG ANALYSIS</h3></div>
                </div>
                <div class="star-point" style="top: 880px; left: 320px;">
                    <div class="star-info"><h3>SIEM & ELK</h3></div>
                </div>
                <div class="star-point" style="top: 1020px; left: 380px;">
                    <div class="star-info"><h3>INCIDENT RESPONSE</h3></div>
                </div>

                <div class="node career soc n-soc">
                    <i class="fas fa-user-shield"></i>
                    <div class="node-hud" style="top: 170px;">
                        <h3>SOC ANALYST ✨</h3>
                        <p>Enterprise Defense Specialist</p>
                    </div>
                </div>
            </div>

            <!-- PENTEST CONSTELLATION -->
            <div class="star-cluster">
                <div class="section-tag-mini" style="top: 760px; left: 63%; border-left-color: var(--red);">PENTESTER PATH</div>

                <div class="star-point" style="top: 800px; left: 650px;">
                    <div class="star-info"><h3>WEB SECURITY</h3></div>
                </div>
                <div class="star-point" style="top: 950px; left: 750px;">
                    <div class="star-info"><h3>EXPLOITATION</h3></div>
                </div>

                <div class="node career pentest n-pentest">
                    <i class="fas fa-user-ninja"></i>
                    <div class="node-hud" style="top: 170px;">
                        <h3>PENTESTER ✨</h3>
                        <p>Offensive Operations Specialist</p>
                    </div>
                </div>
            </div>

            <!-- CLOUD CONSTELLATION -->
            <div class="star-cluster">
                <div class="section-tag-mini" style="top: 720px; left: 78%; border-left-color: var(--purple-l);">CLOUD SECURITY PATH</div>

                <div class="star-point" style="top: 750px; left: 950px;">
                    <div class="star-info"><h3>IAM & GOVERNANCE</h3></div>
                </div>
                <div class="star-point" style="top: 880px; left: 1080px;">
                    <div class="star-info"><h3>CONTAINER SECURITY</h3></div>
                </div>

                <div class="node career cloud n-cloud">
                    <i class="fas fa-cloud-lock"></i>
                    <div class="node-hud" style="top: 170px;">
                        <h3>CLOUD SECURITY ENGINEER ✨</h3>
                        <p>Cloud Infrastructure Specialist</p>
                    </div>
                </div>
            </div>

            <!-- FUTURE CONSTELLATIONS (LOCKED) -->
            <div class="star-cluster locked">
                <div class="section-tag-mini" style="top: 1390px; left: 28%;">FUTURE PATH</div>
                <div class="node n-malware" style="border-color: var(--blue);">
                    <i class="fas fa-dna"></i>
                    <div class="node-hud" style="top: 140px;">
                        <h3>MALWARE ANALYST</h3>
                    </div>
                </div>
            </div>

            <div class="star-cluster locked">
                <div class="section-tag-mini" style="top: 1390px; left: 58%;">FUTURE PATH</div>
                <div class="node n-threat" style="border-color: var(--gold);">
                    <i class="fas fa-crosshairs"></i>
                    <div class="node-hud" style="top: 140px;">
                        <h3>THREAT HUNTER</h3>
                    </div>
                </div>
            </div>

        </div>"""

start_idx = html.find('<div class="roadmap-container">')
end_idx = html.find('</main>', start_idx)

if start_idx != -1 and end_idx != -1:
    html = html[:start_idx] + new_content + '\n    ' + html[end_idx:]

with open("cyber-roadmap.html", "w", encoding="utf-8") as f:
    f.write(html)
