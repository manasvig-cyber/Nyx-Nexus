import re

html_content = """        <header class="page-header">
            <h1 class="page-title">CYBERSECURITY CAREER ROADMAP</h1>
            <p class="page-subtitle">Follow the learning journey from cybersecurity foundations to specialized career roles.</p>
        </header>

        <div class="roadmap-container">
            <div class="orb" style="top: 10%; left: 5%;"></div>
            <div class="orb" style="bottom: 10%; right: 5%; background: radial-gradient(circle, rgba(6, 182, 212, 0.08) 0%, transparent 70%);"></div>

            <svg class="roadmap-svg" viewBox="0 0 1400 1800" preserveAspectRatio="none">
                <!-- Main Zig-Zag Path -->
                <path d="M 150,150 L 1150,150 C 1250,150 1250,450 1150,450 L 150,450 C 50,450 50,750 150,750 L 650,750" class="road-stroke" />
                <path d="M 150,150 L 1150,150 C 1250,150 1250,450 1150,450 L 150,450 C 50,450 50,750 150,750 L 650,750" class="road-pulse" style="stroke-width: 4;" />
                
                <!-- Branches from Node 6 (650, 750) to Careers -->
                <!-- SOC Analyst -->
                <path d="M 650,750 C 650,900 250,900 250,1050" style="fill:none; stroke:var(--green); stroke-width:3; opacity:0.6; stroke-dasharray:6,6;" />
                <path d="M 650,750 C 650,900 250,900 250,1050" class="road-pulse" style="stroke:var(--green); stroke-width:2; opacity:0.8; animation-duration:4s;" />
                
                <!-- Pentester -->
                <path d="M 650,750 C 650,850 650,950 650,1050" style="fill:none; stroke:var(--red); stroke-width:3; opacity:0.6; stroke-dasharray:6,6;" />
                <path d="M 650,750 C 650,850 650,950 650,1050" class="road-pulse" style="stroke:var(--red); stroke-width:2; opacity:0.8; animation-duration:4s;" />

                <!-- Cloud Security -->
                <path d="M 650,750 C 650,900 1050,900 1050,1050" style="fill:none; stroke:var(--purple-l); stroke-width:3; opacity:0.6; stroke-dasharray:6,6;" />
                <path d="M 650,750 C 650,900 1050,900 1050,1050" class="road-pulse" style="stroke:var(--purple-l); stroke-width:2; opacity:0.8; animation-duration:4s;" />

                <!-- Future Paths -->
                <path d="M 250,1200 L 400,1400" style="fill:none; stroke:#fff; stroke-width:1; opacity:0.2; stroke-dasharray:4,4;" />
                <path d="M 1050,1200 L 900,1400" style="fill:none; stroke:#fff; stroke-width:1; opacity:0.2; stroke-dasharray:4,4;" />
            </svg>

            <!-- Foundation Skills Section -->
            <div class="section-tag section-tag-foundation">FOUNDATION SKILLS</div>

            <div class="node step-node" style="top: 150px; left: 150px;">
                <div class="step-num">01</div>
                <i class="fas fa-power-off"></i>
                <div class="node-hud" style="top: 130px; left: 50%; transform: translateX(-50%); position: absolute; width: 280px; text-align: center; pointer-events: none;">
                    <h3 style="font-family: 'Orbitron'; font-size: 18px; color: #fff; margin-bottom: 8px;">SYSTEM START</h3>
                    <p style="font-family: 'Rajdhani'; font-size: 15px; font-weight: 500; color: var(--text-sub);">Initialize your journey into cybersecurity.</p>
                </div>
            </div>

            <div class="node step-node" style="top: 150px; left: 650px;">
                <div class="step-num">02</div>
                <i class="fas fa-network-wired"></i>
                <div class="node-hud" style="top: 130px; left: 50%; transform: translateX(-50%); position: absolute; width: 280px; text-align: center; pointer-events: none;">
                    <h3 style="font-family: 'Orbitron'; font-size: 18px; color: #fff; margin-bottom: 8px;">NETWORKING FUNDAMENTALS</h3>
                    <p style="font-family: 'Rajdhani'; font-size: 15px; font-weight: 500; color: var(--text-sub);">Learn OSI model, TCP/IP, and packet communication.</p>
                </div>
            </div>

            <div class="node step-node" style="top: 150px; left: 1150px;">
                <div class="step-num">03</div>
                <i class="fab fa-linux"></i>
                <div class="node-hud" style="top: 130px; left: 50%; transform: translateX(-50%); position: absolute; width: 280px; text-align: center; pointer-events: none;">
                    <h3 style="font-family: 'Orbitron'; font-size: 18px; color: #fff; margin-bottom: 8px;">LINUX CORE</h3>
                    <p style="font-family: 'Rajdhani'; font-size: 15px; font-weight: 500; color: var(--text-sub);">Understand Linux commands, permissions, and system operations.</p>
                </div>
            </div>

            <!-- Core Security Knowledge Section -->
            <div class="section-tag section-tag-core">CORE SECURITY KNOWLEDGE</div>

            <div class="node step-node" style="top: 450px; left: 1150px;">
                <div class="step-num">04</div>
                <i class="fas fa-shield-halved"></i>
                <div class="node-hud" style="top: 130px; left: 50%; transform: translateX(-50%); position: absolute; width: 280px; text-align: center; pointer-events: none;">
                    <h3 style="font-family: 'Orbitron'; font-size: 18px; color: #fff; margin-bottom: 8px;">SECURITY BASICS</h3>
                    <p style="font-family: 'Rajdhani'; font-size: 15px; font-weight: 500; color: var(--text-sub);">Learn cryptography, authentication, and security principles.</p>
                </div>
            </div>

            <div class="node step-node" style="top: 450px; left: 650px;">
                <div class="step-num">05</div>
                <i class="fas fa-brain"></i>
                <div class="node-hud" style="top: 130px; left: 50%; transform: translateX(-50%); position: absolute; width: 280px; text-align: center; pointer-events: none;">
                    <h3 style="font-family: 'Orbitron'; font-size: 18px; color: #fff; margin-bottom: 8px;">CYBER LOGIC</h3>
                    <p style="font-family: 'Rajdhani'; font-size: 15px; font-weight: 500; color: var(--text-sub);">Develop attacker mindset and security analysis thinking.</p>
                </div>
            </div>

            <!-- Specialization Section -->
            <div class="section-tag section-tag-specialization">SPECIALIZATION</div>

            <div class="node step-node" style="top: 750px; left: 650px;">
                <div class="step-num">06</div>
                <i class="fas fa-code-branch"></i>
                <div class="node-hud" style="top: 130px; left: 50%; transform: translateX(-50%); position: absolute; width: 280px; text-align: center; pointer-events: none;">
                    <h3 style="font-family: 'Orbitron'; font-size: 18px; color: #fff; margin-bottom: 8px;">CHOOSE SPECIALIZATION</h3>
                    <p style="font-family: 'Rajdhani'; font-size: 15px; font-weight: 500; color: var(--text-sub);">Select your cybersecurity career path.</p>
                </div>
            </div>

            <!-- Career Paths Section -->
            <div class="section-tag section-tag-careers">CAREER PATHS</div>

            <!-- SOC ANALYST -->
            <div class="node career soc" style="top: 1050px; left: 250px;">
                <i class="fas fa-user-shield"></i>
                <div class="node-hud" style="top: 170px; left: 50%; transform: translateX(-50%); position: absolute; width: 280px; text-align: center; pointer-events: none;">
                    <h3 style="font-family: 'Orbitron'; font-size: 18px; color: #fff; margin-bottom: 8px;">SOC ANALYST ✨</h3>
                    <p style="font-family: 'Rajdhani'; font-size: 15px; font-weight: 500; color: var(--text-sub);">Enterprise Defense Specialist</p>
                </div>
            </div>

            <!-- PENTESTER -->
            <div class="node career pentest" style="top: 1050px; left: 650px;">
                <i class="fas fa-user-ninja"></i>
                <div class="node-hud" style="top: 170px; left: 50%; transform: translateX(-50%); position: absolute; width: 280px; text-align: center; pointer-events: none;">
                    <h3 style="font-family: 'Orbitron'; font-size: 18px; color: #fff; margin-bottom: 8px;">PENTESTER ✨</h3>
                    <p style="font-family: 'Rajdhani'; font-size: 15px; font-weight: 500; color: var(--text-sub);">Offensive Operations Specialist</p>
                </div>
            </div>

            <!-- CLOUD SECURITY -->
            <div class="node career cloud" style="top: 1050px; left: 1050px;">
                <i class="fas fa-cloud-lock"></i>
                <div class="node-hud" style="top: 170px; left: 50%; transform: translateX(-50%); position: absolute; width: 280px; text-align: center; pointer-events: none;">
                    <h3 style="font-family: 'Orbitron'; font-size: 18px; color: #fff; margin-bottom: 8px;">CLOUD SECURITY ENGINEER ✨</h3>
                    <p style="font-family: 'Rajdhani'; font-size: 15px; font-weight: 500; color: var(--text-sub);">Cloud Infrastructure Specialist</p>
                </div>
            </div>

            <!-- FUTURE PATHS -->
            <div class="node future-path" style="top: 1400px; left: 400px;">
                <i class="fas fa-dna"></i>
                <div class="node-hud" style="top: 140px; left: 50%; transform: translateX(-50%); position: absolute; width: 280px; text-align: center; pointer-events: none;">
                    <h3 style="font-family: 'Orbitron'; font-size: 18px; color: #fff; margin-bottom: 8px;">MALWARE ANALYST</h3>
                </div>
            </div>

            <div class="node future-path" style="top: 1400px; left: 900px;">
                <i class="fas fa-crosshairs"></i>
                <div class="node-hud" style="top: 140px; left: 50%; transform: translateX(-50%); position: absolute; width: 280px; text-align: center; pointer-events: none;">
                    <h3 style="font-family: 'Orbitron'; font-size: 18px; color: #fff; margin-bottom: 8px;">THREAT HUNTER</h3>
                </div>
            </div>
        </div>"""

css_content = """        /* Zig-Zag Specific CSS */
        .step-node {
            position: absolute;
            transform: translate(-50%, -50%);
        }
        .career {
            position: absolute;
            transform: translate(-50%, -50%);
        }
        .future-path {
            position: absolute;
            transform: translate(-50%, -50%);
            border-color: #64748b;
            background: rgba(15, 23, 42, 0.9);
            border-width: 3px;
            border-style: solid;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0.5;
            filter: grayscale(1);
            cursor: not-allowed;
            width: 120px;
            height: 120px;
            z-index: 20;
        }
        .future-path::after {
            content: 'COMING SOON';
            position: absolute;
            bottom: -30px;
            font-family: 'Orbitron';
            font-size: 11px;
            color: #94a3b8;
            letter-spacing: 1px;
            text-align: center;
            white-space: pre-wrap;
            line-height: 1.4;
        }
        .future-path i { color: #64748b; font-size: 42px; }
        .step-num {
            position: absolute;
            top: -15px;
            left: -15px;
            background: var(--bg-deep);
            color: var(--cyan);
            border: 2px solid var(--cyan);
            border-radius: 50%;
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Orbitron';
            font-size: 12px;
            font-weight: 800;
            box-shadow: 0 0 10px var(--cyan);
            z-index: 30;
        }
        .section-tag {
            box-shadow: 0 0 20px rgba(6, 182, 212, 0.5);
            text-shadow: 0 0 10px var(--cyan);
            transform: translateX(-50%);
            position: absolute;
            font-family: 'Orbitron';
            font-size: 14px;
            font-weight: 800;
            color: var(--cyan);
            background: rgba(6, 182, 212, 0.1);
            padding: 8px 20px;
            border: 1px solid var(--cyan);
            border-radius: 4px;
            text-transform: uppercase;
            letter-spacing: 2px;
            z-index: 5;
        }
        .section-tag-foundation { top: 30px; left: 50%; }
        .section-tag-core { top: 330px; left: 50%; }
        .section-tag-specialization { top: 630px; left: 50%; }
        .section-tag-careers { top: 880px; left: 50%; background: rgba(6, 182, 212, 0.2); }
"""

with open("cyber-roadmap.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace main content
main_start = html.find('<header class="page-header">')
main_end = html.find('</main>', main_start)

if main_start != -1 and main_end != -1:
    html = html[:main_start] + html_content + "\n    " + html[main_end:]

# Add CSS before closing </style>
style_end = html.find('</style>')
if style_end != -1:
    html = html[:style_end] + css_content + "\n    " + html[style_end:]

with open("cyber-roadmap.html", "w", encoding="utf-8") as f:
    f.write(html)
