import re

html_content = """        <header class="page-header">
            <h1 class="page-title">CYBERSECURITY CAREER ROADMAP</h1>
            <p class="page-subtitle">Follow the learning journey from cybersecurity foundations to specialized career roles.</p>
        </header>

        <div class="roadmap-container">
            <!-- Ambient UI Orbs -->
            <div class="orb" style="top: 10%; left: 5%;"></div>
            <div class="orb" style="bottom: 10%; right: 5%; background: radial-gradient(circle, rgba(6, 182, 212, 0.08) 0%, transparent 70%);"></div>

            <!-- Absolute Roadmap SVG inside a structured content layout -->
            <svg class="roadmap-svg" viewBox="0 0 1200 1350" preserveAspectRatio="none">
                <!-- Row 1: Left to Right (150 -> 600 -> 1050 at y=150) -->
                <!-- Turn down: 1050,150 to 1050,450 -->
                <!-- Row 2: Right to Left (1050 -> 600 -> 150 at y=450) -->
                <!-- Turn down: 150,450 to 150,750 -->
                <!-- Row 3: Left to center (150 -> 600 at y=750) -->
                <path d="M 150,150 L 1050,150 C 1100,150 1100,200 1100,250 L 1100,350 C 1100,400 1100,450 1050,450 L 150,450 C 100,450 100,500 100,550 L 100,650 C 100,700 100,750 150,750 L 600,750" class="road-stroke" />
                <path d="M 150,150 L 1050,150 C 1100,150 1100,200 1100,250 L 1100,350 C 1100,400 1100,450 1050,450 L 150,450 C 100,450 100,500 100,550 L 100,650 C 100,700 100,750 150,750 L 600,750" class="road-pulse" style="stroke-width: 4;" />
                
                <!-- Branches from Node 6 (600, 750) to Careers (y=1050) -->
                <!-- SOC Analyst -->
                <path d="M 600,750 C 600,900 200,900 200,1050" style="fill:none; stroke:var(--green); stroke-width:4; opacity:0.6; stroke-dasharray:8,8;" />
                <path d="M 600,750 C 600,900 200,900 200,1050" class="road-pulse" style="stroke:var(--green); stroke-width:3; opacity:0.8; animation-duration:4s;" />
                
                <!-- Pentester -->
                <path d="M 600,750 L 600,1050" style="fill:none; stroke:var(--red); stroke-width:4; opacity:0.6; stroke-dasharray:8,8;" />
                <path d="M 600,750 L 600,1050" class="road-pulse" style="stroke:var(--red); stroke-width:3; opacity:0.8; animation-duration:4s;" />

                <!-- Cloud Security -->
                <path d="M 600,750 C 600,900 1000,900 1000,1050" style="fill:none; stroke:var(--purple-l); stroke-width:4; opacity:0.6; stroke-dasharray:8,8;" />
                <path d="M 600,750 C 600,900 1000,900 1000,1050" class="road-pulse" style="stroke:var(--purple-l); stroke-width:3; opacity:0.8; animation-duration:4s;" />

                <!-- Future Paths -->
                <path d="M 200,1180 L 400,1320" style="fill:none; stroke:#fff; stroke-width:2; opacity:0.2; stroke-dasharray:6,6;" />
                <path d="M 1000,1180 L 800,1320" style="fill:none; stroke:#fff; stroke-width:2; opacity:0.2; stroke-dasharray:6,6;" />
            </svg>

            <!-- Foundation Skills Section -->
            <div class="section-tag section-tag-foundation">FOUNDATION SKILLS</div>

            <!-- ROW 1 (y = 150) -->
            <div class="node step-node" style="top: 150px; left: 150px;">
                <div class="step-num">01</div>
                <i class="fas fa-power-off"></i>
                <div class="node-hud">
                    <h3>SYSTEM START</h3>
                    <p>Initialize your journey into cybersecurity.</p>
                </div>
            </div>

            <div class="node step-node" style="top: 150px; left: 600px;">
                <div class="step-num">02</div>
                <i class="fas fa-network-wired"></i>
                <div class="node-hud">
                    <h3>NETWORKING FUNDAMENTALS</h3>
                    <p>Learn OSI model, TCP/IP, and packet communication.</p>
                </div>
            </div>

            <div class="node step-node" style="top: 150px; left: 1050px;">
                <div class="step-num">03</div>
                <i class="fab fa-linux"></i>
                <div class="node-hud">
                    <h3>LINUX CORE</h3>
                    <p>Understand Linux commands, permissions, and system operations.</p>
                </div>
            </div>

            <!-- Core Security Knowledge Section -->
            <div class="section-tag section-tag-core">CORE SECURITY KNOWLEDGE</div>

            <!-- ROW 2 (y = 450) -->
            <div class="node step-node" style="top: 450px; left: 1050px;">
                <div class="step-num">04</div>
                <i class="fas fa-shield-halved"></i>
                <div class="node-hud">
                    <h3>SECURITY BASICS</h3>
                    <p>Learn cryptography, authentication, and security principles.</p>
                </div>
            </div>

            <div class="node step-node" style="top: 450px; left: 600px;">
                <div class="step-num">05</div>
                <i class="fas fa-brain"></i>
                <div class="node-hud">
                    <h3>CYBER LOGIC</h3>
                    <p>Develop attacker mindset and security analysis thinking.</p>
                </div>
            </div>

            <!-- Specialization Section -->
            <div class="section-tag section-tag-specialization">SPECIALIZATION</div>

            <!-- ROW 3 (y = 750) -->
            <div class="node step-node" id="choose-spec-node" style="top: 750px; left: 600px;">
                <div class="step-num">06</div>
                <i class="fas fa-code-branch"></i>
                <div class="node-hud">
                    <h3>CHOOSE SPECIALIZATION</h3>
                    <p>Select your cybersecurity career path.</p>
                </div>
            </div>

            <!-- Career Paths Section -->
            <div class="section-tag section-tag-careers">CAREER PATHS</div>

            <!-- ROW 4 flex row -->
            <div class="career-row">
                <!-- SOC ANALYST -->
                <div class="node career soc">
                    <i class="fas fa-user-shield"></i>
                    <div class="node-hud">
                        <h3>SOC ANALYST ✨</h3>
                        <p>Enterprise Defense Specialist</p>
                    </div>
                </div>

                <!-- PENTESTER -->
                <div class="node career pentest">
                    <i class="fas fa-user-ninja"></i>
                    <div class="node-hud">
                        <h3>PENTESTER ✨</h3>
                        <p>Offensive Operations Specialist</p>
                    </div>
                </div>

                <!-- CLOUD SECURITY -->
                <div class="node career cloud">
                    <i class="fas fa-cloud-lock"></i>
                    <div class="node-hud">
                        <h3>CLOUD SECURITY ENGINEER ✨</h3>
                        <p>Cloud Infrastructure Specialist</p>
                    </div>
                </div>
            </div>

            <!-- FUTURE PATHS -->
            <div class="future-row">
                <div class="node future-path">
                    <i class="fas fa-dna"></i>
                    <div class="node-hud">
                        <h3>MALWARE ANALYST</h3>
                        <p>Coming Soon</p>
                    </div>
                </div>

                <div class="node future-path">
                    <i class="fas fa-crosshairs"></i>
                    <div class="node-hud">
                        <h3>THREAT HUNTER</h3>
                        <p>Coming Soon</p>
                    </div>
                </div>
            </div>
        </div>"""

css = """        /* Fixed Timeline Layout Layout */
        .roadmap-container {
            position: relative;
            width: 100%;
            max-width: 1200px;
            margin: 0 auto;
            min-height: 1600px;
        }

        .roadmap-svg {
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            overflow: visible;
        }

        .road-stroke {
            fill: none;
            stroke: var(--cyan);
            stroke-width: 6;
            stroke-linecap: round;
            stroke-linejoin: round;
            filter: drop-shadow(0 0 10px rgba(6, 182, 212, 0.5));
            opacity: 0.5;
        }

        /* Update Node Circle Sizes */
        .node {
            width: 90px;
            height: 90px;
            background: rgba(15, 23, 42, 0.9);
            border: 3px solid var(--cyan);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 20;
            cursor: pointer;
            transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        }
        .node i {
            font-size: 32px;
            color: var(--cyan);
            transition: 0.4s;
        }
        .node:hover i {
            color: #fff;
            text-shadow: 0 0 15px #fff;
        }
        
        .step-num {
            position: absolute;
            top: -15px;
            left: -15px;
            background: var(--bg-deep);
            color: var(--cyan);
            border: 2px solid var(--cyan);
            border-radius: 50%;
            width: 38px;
            height: 38px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Orbitron';
            font-size: 18px;
            font-weight: bold;
            box-shadow: 0 0 10px var(--cyan);
            z-index: 30;
        }

        /* Career Destinations */
        .node.career {
            width: 140px;
            height: 140px;
            border-width: 3px;
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
            /* Reset absolute pos since we use flex container */
            position: relative;
            transform: none !important;
            top: auto !important; left: auto !important;
        }
        
        .node.career.soc { border-color: var(--green); box-shadow: 0 0 20px rgba(34, 197, 94, 0.5); filter: drop-shadow(0 0 15px var(--green)); }
        .node.career.soc i { color: var(--green); }
        .node.career.soc:hover { box-shadow: 0 0 45px var(--green); }
        
        .node.career.pentest { border-color: var(--red); box-shadow: 0 0 20px rgba(239, 68, 68, 0.5); filter: drop-shadow(0 0 15px var(--red));}
        .node.career.pentest i { color: var(--red); }
        .node.career.pentest:hover { box-shadow: 0 0 45px var(--red); }
        
        .node.career.cloud { border-color: var(--purple-l); box-shadow: 0 0 20px rgba(168, 85, 247, 0.5); filter: drop-shadow(0 0 15px var(--purple-l));}
        .node.career.cloud i { color: var(--purple-l); }
        .node.career.cloud:hover { box-shadow: 0 0 45px var(--purple-l); }
        
        .node.career i {
            font-size: 50px;
        }

        /* Hover Animation */
        .node.step-node:hover, .node.future-path:hover {
            transform: translate(-50%, -50%) scale(1.08) !important;
            box-shadow: 0 0 35px var(--cyan);
            border-color: #fff;
            z-index: 100;
        }
        .node.career:hover {
            transform: scale(1.08) !important;
            border-color: #fff;
            z-index: 100;
        }

        /* Fix Specialization Node */
        #choose-spec-node {
            width: 100px;
            height: 100px;
            animation: specPulse 2s infinite alternate;
        }
        @keyframes specPulse {
            0% { box-shadow: 0 0 10px var(--cyan); border-color: var(--cyan); }
            100% { box-shadow: 0 0 30px #fff; border-color: #fff; }
        }

        /* Clean Node HUD Text */
        .node-hud {
            position: absolute;
            top: 110px; /* Spacing below circle 90px (circle) + 20px margin */
            left: 50%;
            transform: translateX(-50%);
            width: 220px; /* Max width text 220px */
            max-width: 220px;
            text-align: center;
            pointer-events: none;
            margin: auto;
        }
        /* HUD alignment for flex items (careers) */
        .node.career .node-hud {
            top: 160px; /* Spacing below 140px circle */
            width: 280px;
            max-width: 280px;
        }
        /* HUD alignment for larger specialization box */
        #choose-spec-node .node-hud {
            top: 120px;
        }

        .node-hud h3 {
            font-family: 'Orbitron';
            font-size: 16px;
            color: #fff;
            margin-bottom: 8px;
            margin-top: 20px;
            line-height: 1.4;
            text-transform: uppercase;
        }

        .node-hud p {
            font-family: 'Rajdhani';
            font-size: 14px;
            font-weight: 500;
            color: var(--text-sub);
            line-height: 1.4;
            margin: 0;
        }

        /* Larger Career Labels */
        .node.career .node-hud h3 {
            font-size: 20px;
            font-weight: bold;
            margin-top: 10px;
        }
        .node.career .node-hud p {
            font-size: 14px;
            opacity: 0.8;
        }

        /* Section Titles Alignments */
        .section-tag {
            box-shadow: 0 0 20px rgba(6, 182, 212, 0.5);
            text-shadow: 0 0 10px var(--cyan);
            transform: translateX(-50%);
            position: absolute;
            font-family: 'Orbitron';
            font-size: 18px; /* Larger to act as dividers */
            font-weight: 800;
            color: var(--cyan);
            background: rgba(6, 182, 212, 0.1);
            padding: 8px 24px;
            border: 1px solid var(--cyan);
            border-radius: 4px;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 40px;
            margin-top: 60px; /* Set rule */
            z-index: 5;
        }
        /* Adjusted positioning to not overlap text, and maintain 120-160px spacing */
        .section-tag-foundation { top: 0px; left: 50%; margin-top: 0; }
        .section-tag-core { top: 320px; left: 50%; }
        .section-tag-specialization { top: 620px; left: 50%; }
        .section-tag-careers { top: 900px; left: 50%; background: rgba(6, 182, 212, 0.2); }

        /* Career Flex Container */
        .career-row {
            display: flex;
            justify-content: space-evenly;
            align-items: center;
            position: absolute;
            top: 1050px;
            left: 0;
            width: 100%;
            z-index: 20;
        }

        /* Future Path Flex Container */
        .future-row {
            display: flex;
            justify-content: space-evenly;
            align-items: center;
            position: absolute;
            top: 1350px;
            left: 20%;
            width: 60%;
            z-index: 20;
        }
        
        .future-path {
            position: relative;
            transform: none !important;
            top: auto !important; left: auto !important;
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
        
        .step-node {
            position: absolute;
            transform: translate(-50%, -50%);
        }
"""

with open("cyber-roadmap.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace main content
main_start = html.find('<header class="page-header">')
main_end = html.find('</main>', main_start)

if main_start != -1 and main_end != -1:
    html = html[:main_start] + html_content + "\n    " + html[main_end:]

# Add CSS before closing </style>
# Find the start of the roadmap specific CSS 
style_start = html.find('/* Cinematic Roadmap Path */')
style_end = html.find('</style>')

if style_start != -1 and style_end != -1:
    html = html[:style_start] + css + "\n    " + html[style_end:]

with open("cyber-roadmap.html", "w", encoding="utf-8") as f:
    f.write(html)
